import json
import subprocess
import sys
import unittest

from agent_company import GeneralManager
from agent_company.models import CompanyGoal


class AgentCompanyTests(unittest.TestCase):
    def test_general_manager_assigns_all_default_agents(self) -> None:
        report = GeneralManager().run(CompanyGoal("办一个由多个 agent 干活的公司"))

        self.assertEqual(len(report.assignments), 6)
        self.assertEqual(len(report.outputs), 6)
        self.assertIn("总经理", report.executive_summary)
        self.assertTrue(any("岗位覆盖完整" in item for item in report.audit))

    def test_cli_json_output_is_machine_readable(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agent_company", "--json", "做一个 AI 自动化咨询公司"],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["objective"], "做一个 AI 自动化咨询公司")
        self.assertEqual(len(payload["outputs"]), 6)
        self.assertIn("recommended_next_actions", payload)


if __name__ == "__main__":
    unittest.main()
