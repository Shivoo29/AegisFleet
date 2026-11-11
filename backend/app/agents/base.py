"""Agent runtime interface (M9). Frozen — A owns the impl, interface frozen."""
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from app.gateway.gateway import call as gateway_call
from app.ledger import find as ledger_find
from app.llm import complete as llm_complete
from app.models import Decision, LedgerEntry

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def load_prompt(agent: str) -> str:
    path = PROMPTS_DIR / f"{agent}.md"
    if not path.exists():
        return f"version: 0\n# {agent} prompt (stub)"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class AgentContext:
    def __init__(self, agent: str, run_id: str | None = None):
        self.agent = agent
        self.run_id = run_id
        self.steps: list[dict] = []

    def act(self, tool: str, args: dict, reason: str) -> Decision:
        dec = gateway_call(self.agent, tool, args, reason)
        self.log("tool", f"{self.agent}.{tool} -> {dec.outcome}: {dec.reason}")
        return dec

    def plan(self, tool: str, args: dict, reason: str, title: str, due_at) -> str:
        """Schedule a future action. It runs through the gateway when due; the seller can move or cancel it."""
        from app import plans
        pid = plans.add(self.agent, tool, args, reason, title, due_at)
        self.log("note", f"{self.agent} planned '{title}' for {due_at:%d %b %H:%M} UTC")
        return pid

    def llm(self, system: str, user: str, schema: type[BaseModel]) -> BaseModel:
        result = llm_complete(system, user, schema)
        self.log("llm", f"{schema.__name__}")
        return result

    def ledger_find(self, **filters) -> list[LedgerEntry]:
        return ledger_find(**filters)

    def log(self, kind: Literal["llm", "tool", "note"], summary: str) -> None:
        self.steps.append({"kind": kind, "summary": summary})