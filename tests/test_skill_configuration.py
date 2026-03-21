# Responsible file: SKILL.md and agents/openai.yaml
# Purpose: ensure the skill stays single-agent for implementation and does not instruct parallel workers.

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text()
OPENAI_YAML = (ROOT / "agents" / "openai.yaml").read_text()
EVALS = json.loads((ROOT / "evals" / "evals.json").read_text())


def test_skill_forbids_parallel_workers() -> None:
    assert "Do not spawn parallel workers" in SKILL
    assert "Context scout" not in SKILL
    assert "Test scout" not in SKILL
    assert "Implementation scout" not in SKILL
    assert "Use explorers for read-heavy sidecars." not in SKILL


def test_ui_metadata_does_not_advertise_parallel_agents() -> None:
    assert "parallel agents" not in OPENAI_YAML
    assert "monitor agent" in OPENAI_YAML


def test_evals_do_not_reward_parallel_orchestration() -> None:
    serialized = json.dumps(EVALS)
    assert "parallel agents" not in serialized
    assert "minimum sidecars" not in serialized
    assert "duplicate implementers" not in serialized
