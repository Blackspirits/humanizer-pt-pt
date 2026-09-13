from __future__ import annotations

import re
from pathlib import Path

VALID_MODES = {"AUTO", "AUDITAR", "HUMANIZAR", "QA HUMANO", "CLONAR VOZ"}
REWRITE_MODES = {"AUTO", "HUMANIZAR", "QA HUMANO", "CLONAR VOZ"}
AUDIT_SEVERITIES = {"ligeira", "clara", "grave"}
OVERALL_SEVERITIES = {"limpo", "ligeiro", "moderado", "pesado"}


def skill_version(root: Path) -> str:
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(
        r"^metadata:\s*\n(?:^[ \t]+.*\n)*?^[ \t]+version:\s*[\"']?([^\"'\n]+)",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        raise ValueError("metadata.version não encontrado em SKILL.md")
    return match.group(1).strip()


def pattern_ids(root: Path) -> list[int]:
    text = (root / "references" / "patterns.md").read_text(encoding="utf-8")
    ids = [
        int(value)
        for value in re.findall(r"^###\s+(\d+)\.\s+", text, flags=re.MULTILINE)
    ]
    if not ids:
        raise ValueError("nenhum padrão encontrado")
    expected = list(range(1, len(ids) + 1))
    if ids != expected:
        raise ValueError(f"IDs de padrões não contíguos: {ids}")
    return ids
