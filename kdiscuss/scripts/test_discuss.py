"""Focused tests for CLI conversation continuity and failed delivery handling."""

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import discuss


class DiscussionTests(unittest.TestCase):
    def state(self, agent, session=None):
        return {
            "agent": agent, "cwd": str(Path.cwd().resolve()),
            "session_id": session, "claude_id": "test-session",
            "turns": 0, "status": "ready", "messages": [],
        }

    def output(self, agent, session="test-session", text="Status: agree"):
        if agent == "claude":
            return json.dumps({
                "subtype": "success", "session_id": session, "result": text,
                "is_error": False,
            })
        if agent == "codex":
            events = [
                {"type": "thread.started", "thread_id": session},
                {"type": "item.completed", "item": {
                    "type": "agent_message", "phase": "commentary", "text": "Checking",
                }},
                {"type": "item.completed", "item": {
                    "type": "agent_message", "phase": "final_answer", "text": text,
                }},
                {"type": "turn.completed"},
            ]
        else:
            events = [
                {"type": "text", "sessionID": session, "part": {"text": text}},
                {"type": "step_finish", "sessionID": session, "part": {"reason": "stop"}},
            ]
        return "\n".join(json.dumps(event) for event in events)

    def invoke(self, args, message):
        with patch("sys.argv", ["discuss.py", *args]), patch("sys.stdin", io.StringIO(message)):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return discuss.main()

    def test_start_resume_and_limit_for_each_agent(self):
        for agent in discuss.MODELS:
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "session.json"
                calls = []

                def launch(command, **kwargs):
                    process = unittest.mock.Mock()
                    process.returncode = 0

                    def communicate(message, timeout):
                        calls.append((command, message, kwargs))
                        if agent == "claude":
                            flag = "--resume" if "--resume" in command else "--session-id"
                            session = command[command.index(flag) + 1]
                        else:
                            session = "test-session"
                        return self.output(agent, session), ""

                    process.communicate.side_effect = communicate
                    return process

                with patch("discuss.shutil.which", return_value="/bin/agent"), patch("discuss.subprocess.Popen", side_effect=launch):
                    for turn in range(discuss.MAX_TURNS):
                        args = ["--state", str(path)] + (["--agent", agent] if turn == 0 else [])
                        self.assertEqual(self.invoke(args, f"Message {turn}"), 0)
                    with self.assertRaises(SystemExit):
                        self.invoke(["--state", str(path)], "One too many")
                self.assertEqual(len(calls), discuss.MAX_TURNS)
                self.assertIn("# Discussion rules", calls[0][1])
                self.assertNotIn("# Discussion rules", calls[1][1])
                self.assertIn("This is the final reply", calls[-1][1])
                resume_command = calls[1][0]
                if agent == "claude":
                    self.assertIn("--resume", resume_command)
                    self.assertNotIn("--session-id", resume_command)
                elif agent == "codex":
                    self.assertEqual(resume_command[:3], ["codex", "exec", "resume"])
                else:
                    self.assertIn("--session", resume_command)
                saved = json.loads(path.read_text())
                self.assertIn(saved["session_id"], resume_command)
                self.assertEqual(saved["turns"], discuss.MAX_TURNS)
                self.assertEqual(len(saved["messages"]), discuss.MAX_TURNS * 2)
                self.assertEqual(saved["status"], "ready")

    def test_failed_turn_cannot_be_resent(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            with patch("discuss.shutil.which", return_value="/bin/agent"), patch("discuss.run_turn", side_effect=ValueError("Delivery uncertain")) as run:
                self.assertEqual(self.invoke(["--agent", "codex", "--state", str(path)], "Opening"), 1)
                with self.assertRaises(SystemExit):
                    self.invoke(["--state", str(path)], "Retry")
                self.assertEqual(run.call_count, 1)
                self.assertEqual(json.loads(path.read_text())["status"], "failed")

    def test_pending_turn_cannot_be_resent(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            state = self.state("codex", "test-session")
            state["status"] = "pending"
            discuss.save(path, state)
            with patch("discuss.run_turn") as run, self.assertRaises(SystemExit):
                self.invoke(["--state", str(path)], "Retry")
            run.assert_not_called()

    def test_different_session_is_rejected(self):
        for agent in discuss.MODELS:
            with self.subTest(agent=agent), self.assertRaises(ValueError):
                discuss.parse_reply(agent, self.output(agent, "wrong-session"), self.state(agent, "test-session"))

    def test_partial_reply_and_reported_error_are_rejected(self):
        for agent in ("codex", "opencode"):
            output = self.output(agent)
            with self.subTest(agent=agent):
                with self.assertRaises(ValueError):
                    discuss.parse_reply(agent, output.rsplit("\n", 1)[0], self.state(agent))
                with self.assertRaises(ValueError):
                    discuss.parse_reply(agent, output + '\n{"type":"error","message":"Unavailable"}', self.state(agent))
        with self.assertRaises(ValueError):
            discuss.parse_reply("claude", '{"subtype":"error_max_turns","is_error":true}', self.state("claude"))

    def test_opencode_runtime_overrides_preserve_unrelated_config(self):
        original = {"theme": "custom", "agent": {"other": {"mode": "primary"}}, "share": "auto"}
        with patch.dict(os.environ, {"OPENCODE_CONFIG_CONTENT": json.dumps(original)}):
            config = json.loads(discuss.environment("opencode")["OPENCODE_CONFIG_CONTENT"])
        self.assertEqual(config["theme"], "custom")
        self.assertEqual(config["agent"]["other"], original["agent"]["other"])
        self.assertEqual(config["share"], "disabled")
        self.assertEqual(config["agent"]["kdiscuss"]["permission"], {"*": "deny"})

    def test_cli_failure_retains_diagnostic(self):
        process = unittest.mock.Mock(returncode=1)
        process.communicate.return_value = ("", "Authentication required")
        args = unittest.mock.Mock(timeout=10)
        with patch("discuss.subprocess.Popen", return_value=process):
            with self.assertRaisesRegex(ValueError, "Authentication required"):
                discuss.run_turn(args, self.state("codex"), "Opening")


if __name__ == "__main__":
    unittest.main()
