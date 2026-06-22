from __future__ import annotations

from dataclasses import dataclass
from textwrap import shorten

from .models import AgentOutput, AgentProfile, Assignment, CompanyGoal


def _focus(objective: str, width: int = 72) -> str:
    return shorten(" ".join(objective.split()), width=width, placeholder="...")


@dataclass(frozen=True)
class SpecialistAgent:
    profile: AgentProfile

    def work(self, goal: CompanyGoal, assignment: Assignment) -> AgentOutput:
        objective = _focus(goal.objective)
        constraints = "; ".join(goal.constraints) if goal.constraints else "暂无额外限制"
        methods = _role_methods(self.profile.key, objective, constraints)
        risks = _role_risks(self.profile.key)
        next_steps = _role_next_steps(self.profile.key)
        return AgentOutput(
            agent_key=self.profile.key,
            title=self.profile.title,
            summary=f"{self.profile.title}完成了「{assignment.title}」：围绕「{objective}」给出可执行建议。",
            deliverables=methods,
            risks=risks,
            next_steps=next_steps,
        )


def default_agents() -> dict[str, SpecialistAgent]:
    profiles = [
        AgentProfile(
            key="researcher",
            title="市场研究员",
            mission="发现用户、市场、竞品和机会窗口。",
            strengths=("竞品分析", "用户画像", "趋势判断"),
        ),
        AgentProfile(
            key="product",
            title="产品经理",
            mission="把目标变成范围清楚、可交付的产品方案。",
            strengths=("PRD", "优先级", "验收标准"),
        ),
        AgentProfile(
            key="engineer",
            title="工程师",
            mission="设计技术路径，识别实现风险，推进可运行版本。",
            strengths=("架构", "实现计划", "测试"),
        ),
        AgentProfile(
            key="designer",
            title="设计师",
            mission="让产品体验清晰、可信、顺手。",
            strengths=("信息架构", "界面状态", "文案"),
        ),
        AgentProfile(
            key="operator",
            title="增长运营",
            mission="规划获客、转化、留存和日常运营动作。",
            strengths=("渠道", "活动", "指标"),
        ),
        AgentProfile(
            key="finance_legal",
            title="财务法务",
            mission="控制预算、合同、合规和经营风险。",
            strengths=("预算", "风险清单", "审批规则"),
        ),
    ]
    return {profile.key: SpecialistAgent(profile) for profile in profiles}


def _role_methods(agent_key: str, objective: str, constraints: str) -> list[str]:
    if agent_key == "researcher":
        return [
            f"定义目标用户：列出 3 类最可能需要「{objective}」的人，并标记付费能力。",
            "竞品扫描：找 5 个直接/间接替代方案，比较价格、核心功能、获客渠道。",
            f"约束记录：执行时需要遵守「{constraints}」。",
        ]
    if agent_key == "product":
        return [
            "MVP 范围：只保留目标输入、总经理拆解、岗位产出、复盘建议四个主流程。",
            "验收标准：每个任务必须有负责人、预期产出、风险和下一步。",
            "路线图：先做单次任务闭环，再做记忆、真实工具调用和人工审批。",
        ]
    if agent_key == "engineer":
        return [
            "技术方案：先用本地 CLI 和结构化 JSON，后续可替换 agent 执行器为 LLM API。",
            "数据模型：Goal、Assignment、AgentOutput、ManagerReport 四类对象足够支撑 MVP。",
            "质量门槛：至少提供 CLI smoke test、JSON 导出和核心编排单元测试。",
        ]
    if agent_key == "designer":
        return [
            "交互原则：老板只输入目标和限制，总经理负责把复杂度收起来。",
            "终端呈现：用清晰分区显示总经理安排、各岗位结果、风险和下一步。",
            "命名体系：所有角色使用公司语言，不暴露底层实现术语。",
        ]
    if agent_key == "operator":
        return [
            "启动渠道：先用个人网络、垂直社群和内容记录验证需求。",
            "转化动作：把每次 agent 产出整理成案例，形成可复用销售材料。",
            "运营指标：跟踪目标数、完成率、人工审批次数、可复用资产数。",
        ]
    if agent_key == "finance_legal":
        return [
            "权限边界：涉及付款、发外部邮件、改生产系统、签合同必须人工批准。",
            "预算框架：先按模型/API、工具订阅、人工复核时间三类成本统计。",
            "合规提示：财务、法律、医疗等高风险建议只能作为草稿，不能自动执行。",
        ]
    return ["暂无该岗位的默认方法。"]


def _role_risks(agent_key: str) -> list[str]:
    common = ["输入目标过宽会导致产出泛化，需要总经理持续收窄范围。"]
    role_specific = {
        "researcher": ["市场信息可能过期，正式决策前需要联网核验。"],
        "product": ["MVP 范围容易膨胀，需要明确暂不做事项。"],
        "engineer": ["没有真实模型或工具权限时，只能模拟协作，不能真正自动执行外部动作。"],
        "designer": ["终端界面承载复杂信息时，需要避免输出太长。"],
        "operator": ["增长建议如果没有真实渠道数据，初期只能作为实验假设。"],
        "finance_legal": ["合规判断不能替代专业人士审核。"],
    }
    return role_specific.get(agent_key, []) + common


def _role_next_steps(agent_key: str) -> list[str]:
    steps = {
        "researcher": ["补充 5 个真实竞品和 10 个潜在用户访谈问题。"],
        "product": ["把 MVP 拆成 3 个一周内能完成的里程碑。"],
        "engineer": ["接入真实 LLM 执行器前，先固定输入输出协议。"],
        "designer": ["为终端输出制定固定模板，避免每次格式漂移。"],
        "operator": ["设计第一个获客实验：目标人群、渠道、话术、成功指标。"],
        "finance_legal": ["建立审批清单：哪些动作允许自动执行，哪些必须老板确认。"],
    }
    return steps.get(agent_key, ["等待总经理安排下一步。"])
