from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class CompanyGoal:
    objective: str
    constraints: list[str] = field(default_factory=list)
    owner: str = "老板"


@dataclass(frozen=True)
class AgentProfile:
    key: str
    title: str
    mission: str
    strengths: tuple[str, ...]


@dataclass(frozen=True)
class Assignment:
    agent_key: str
    title: str
    brief: str
    expected_output: str
    priority: Priority = Priority.MEDIUM


@dataclass(frozen=True)
class AgentOutput:
    agent_key: str
    title: str
    summary: str
    deliverables: list[str]
    risks: list[str]
    next_steps: list[str]


@dataclass(frozen=True)
class ManagerReport:
    objective: str
    created_at: str
    operating_principles: list[str]
    assignments: list[Assignment]
    outputs: list[AgentOutput]
    audit: list[str]
    executive_summary: str
    recommended_next_actions: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "created_at": self.created_at,
            "operating_principles": self.operating_principles,
            "assignments": [assignment_to_dict(item) for item in self.assignments],
            "outputs": [output_to_dict(item) for item in self.outputs],
            "audit": self.audit,
            "executive_summary": self.executive_summary,
            "recommended_next_actions": self.recommended_next_actions,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def assignment_to_dict(assignment: Assignment) -> dict[str, str]:
    return {
        "agent_key": assignment.agent_key,
        "title": assignment.title,
        "brief": assignment.brief,
        "expected_output": assignment.expected_output,
        "priority": assignment.priority.value,
    }


def output_to_dict(output: AgentOutput) -> dict[str, Any]:
    return {
        "agent_key": output.agent_key,
        "title": output.title,
        "summary": output.summary,
        "deliverables": output.deliverables,
        "risks": output.risks,
        "next_steps": output.next_steps,
    }
