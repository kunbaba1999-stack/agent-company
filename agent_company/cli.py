from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import fill

from .manager import GeneralManager
from .models import CompanyGoal, ManagerReport


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-company",
        description="Run a terminal-only multi-agent company with a supervising General Manager.",
    )
    parser.add_argument(
        "objective",
        nargs="*",
        help="Company goal for the General Manager to arrange. Example: 做一个自动化内容工作室",
    )
    parser.add_argument(
        "-c",
        "--constraint",
        action="append",
        default=[],
        help="Constraint the General Manager must respect. Can be repeated.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the full report as JSON.",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Save the full JSON report to this path.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    objective = " ".join(args.objective).strip()
    if not objective:
        parser.error("请给公司一个目标，例如：python -m agent_company 帮我做一个 AI 自动化咨询公司")

    goal = CompanyGoal(objective=objective, constraints=args.constraint)
    report = GeneralManager().run(goal)

    if args.save:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        args.save.write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_report(report))

    if args.save:
        print(f"\n已保存完整报告：{args.save}")
    return 0


def render_report(report: ManagerReport) -> str:
    lines: list[str] = []
    lines.append("AGENT COMPANY / 总经理控制台")
    lines.append("=" * 34)
    lines.append(f"目标：{report.objective}")
    lines.append(f"时间：{report.created_at}")
    lines.append("")

    lines.append("总经理原则")
    lines.append("-" * 34)
    for item in report.operating_principles:
        lines.append(f"- {wrap(item)}")
    lines.append("")

    lines.append("任务安排")
    lines.append("-" * 34)
    for assignment in report.assignments:
        lines.append(f"[{assignment.priority.value.upper()}] {assignment.title} -> {assignment.agent_key}")
        lines.append(f"  brief: {wrap(assignment.brief, indent='  ')}")
        lines.append(f"  output: {wrap(assignment.expected_output, indent='  ')}")
    lines.append("")

    lines.append("岗位产出")
    lines.append("-" * 34)
    for output in report.outputs:
        lines.append(f"{output.title}")
        lines.append(f"  {wrap(output.summary, indent='  ')}")
        lines.append("  交付物：")
        for item in output.deliverables:
            lines.append(f"  - {wrap(item, indent='    ')}")
        lines.append("  风险：")
        for item in output.risks:
            lines.append(f"  - {wrap(item, indent='    ')}")
        lines.append("  下一步：")
        for item in output.next_steps:
            lines.append(f"  - {wrap(item, indent='    ')}")
        lines.append("")

    lines.append("总经理复盘")
    lines.append("-" * 34)
    lines.append(wrap(report.executive_summary))
    for item in report.audit:
        lines.append(f"- {wrap(item)}")
    lines.append("")

    lines.append("建议下一步")
    lines.append("-" * 34)
    for index, item in enumerate(report.recommended_next_actions, start=1):
        lines.append(f"{index}. {wrap(item)}")
    return "\n".join(lines)


def wrap(text: str, indent: str = "", width: int = 96) -> str:
    return fill(
        text,
        width=width,
        initial_indent=indent,
        subsequent_indent=indent,
        break_long_words=False,
        break_on_hyphens=False,
    )
