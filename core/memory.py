"""
Agent Memory Module
Manages episodic scratchpads, intermediate observations, and reasoning history.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
import time

@dataclass
class StepRecord:
    step_number: int
    thought: str
    tool_name: str
    tool_input: Dict[str, Any]
    observation: str
    reflection: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class AgentMemory:
    """
    Episodic memory tracking agent goals, execution steps, and learned context.
    """
    def __init__(self, goal: str = ""):
        self.goal = goal
        self.plan: List[str] = []
        self.steps: List[StepRecord] = []
        self.findings: List[str] = []
        self.metadata: Dict[str, Any] = {}

    def set_goal(self, goal: str):
        self.goal = goal

    def set_plan(self, plan: List[str]):
        self.plan = plan

    def record_step(
        self,
        thought: str,
        tool_name: str,
        tool_input: Dict[str, Any],
        observation: str,
        reflection: str = ""
    ) -> StepRecord:
        step_number = len(self.steps) + 1
        record = StepRecord(
            step_number=step_number,
            thought=thought,
            tool_name=tool_name,
            tool_input=tool_input,
            observation=observation,
            reflection=reflection
        )
        self.steps.append(record)
        return record

    def add_finding(self, finding: str):
        if finding and finding not in self.findings:
            self.findings.append(finding)

    def format_scratchpad(self) -> str:
        """
        Formats all past steps into a prompt-friendly scratchpad.
        """
        if not self.steps:
            return "No previous steps taken."
        
        lines = []
        for s in self.steps:
            lines.append(f"Step {s.step_number}:")
            lines.append(f"  Thought: {s.thought}")
            lines.append(f"  Action: {s.tool_name}({json.dumps(s.tool_input, ensure_ascii=False)})")
            lines.append(f"  Observation: {s.observation}")
            if s.reflection:
                lines.append(f"  Reflection: {s.reflection}")
        return "\n".join(lines)

    def clear(self):
        self.plan.clear()
        self.steps.clear()
        self.findings.clear()
        self.metadata.clear()
