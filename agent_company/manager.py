from __future__ import annotations

from .agents import SpecialistAgent, default_agents
from .models import Assignment, CompanyGoal, ManagerReport, Priority, utc_now


class GeneralManager:
    """Supervises the agent company for one goal at a time."""

    def __init__(self, agents: dict[str, SpecialistAgent] | None = None) -> None:
        self.agents = agents or default_agents()

    def run(self, goal: CompanyGoal) -> ManagerReport:
        assignments = self.plan(goal)
        outputs = []
        for assignment in assignments:
            agent = self.agents[assignment.agent_key]
            outputs.append(agent.work(goal, assignment))

        audit = self.audit(assignments)
        return ManagerReport(
            objective=goal.objective,
            created_at=utc_now(),
            operating_principles=self.operating_principles(goal),
            assignments=assignments,
            outputs=outputs,
            audit=audit,
            executive_summary=self.summarize(goal, outputs_count=len(outputs)),
            recommended_next_actions=self.next_actions(goal),
        )

    def operating_principles(self, goal: CompanyGoal) -> list[str]:
        principles = [
            "总经理负责拆解、排优先级、检查风险，岗位 agent 负责产出专业意见。",
            "任何涉及真实金钱、外部发送、生产系统和法律承诺的动作都需要老板确认。",
            "先交付能跑通闭环的 MVP，再增加记忆、工具权限和真实模型执行。",
        ]
        if goal.constraints:
            principles.append("本轮额外限制：" + "；".join(goal.constraints))
        return principles

    def plan(self, goal: CompanyGoal) -> list[Assignment]:
        objective = goal.objective.strip()
        return [
            Assignment(
                agent_key="researcher",
                title="验证机会和对象",
                brief=f"判断「{objective}」面向谁、替代方案是什么、机会在哪里。",
                expected_output="用户画像、竞品维度、需要验证的假设",
                priority=Priority.HIGH,
            ),
            Assignment(
                agent_key="product",
                title="定义 MVP 和验收标准",
                brief=f"把「{objective}」压缩成第一版能交付的流程。",
                expected_output="MVP 范围、用户流程、验收标准",
                priority=Priority.HIGH,
            ),
            Assignment(
                agent_key="engineer",
                title="设计实现路径",
                brief="选择最小技术方案，列出模块、接口、测试方式和后续扩展点。",
                expected_output="技术方案、数据模型、测试计划",
                priority=Priority.HIGH,
            ),
            Assignment(
                agent_key="designer",
                title="整理使用体验",
                brief="设计老板和总经理之间的交互方式，让终端输出可读、可决策。",
                expected_output="交互原则、信息层级、输出模板建议",
                priority=Priority.MEDIUM,
            ),
            Assignment(
                agent_key="operator",
                title="规划启动运营",
                brief="设计第一批用户验证和持续运营动作。",
                expected_output="渠道、话术、指标、实验计划",
                priority=Priority.MEDIUM,
            ),
            Assignment(
                agent_key="finance_legal",
                title="建立边界和审批",
                brief="列出成本、权限、合规和人工审批边界。",
                expected_output="预算分类、审批规则、风险提示",
                priority=Priority.HIGH,
            ),
        ]

    def audit(self, assignments: list[Assignment]) -> list[str]:
        assigned = {assignment.agent_key for assignment in assignments}
        expected = set(self.agents)
        missing = sorted(expected - assigned)
        audit = [
            f"已安排 {len(assignments)} 个任务，覆盖 {len(assigned)} 个岗位。",
            "所有高风险动作先进入审批，不允许 agent 自行付款、发外部承诺或改生产系统。",
        ]
        if missing:
            audit.append("未安排岗位：" + "、".join(missing))
        else:
            audit.append("岗位覆盖完整：研究、产品、工程、设计、运营、财务法务均已参与。")
        return audit

    def summarize(self, goal: CompanyGoal, outputs_count: int) -> str:
        return (
            f"总经理已围绕「{goal.objective}」完成第一轮组织安排，"
            f"收到 {outputs_count} 个岗位的结构化产出。建议先把高优先级事项做成一周内可验证的闭环。"
        )

    def next_actions(self, goal: CompanyGoal) -> list[str]:
        return [
            "老板确认：这家公司第一阶段最重要的业务目标是什么。",
            "总经理把确认后的目标拆成 3 个里程碑，每个里程碑只保留一个验收标准。",
            "工程师接入真实 LLM API 或本地模型前，先冻结 Assignment 和 AgentOutput 协议。",
            "财务法务建立审批清单，明确哪些动作可自动做、哪些必须人工确认。",
        ]
