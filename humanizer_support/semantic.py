from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable


@dataclass(frozen=True)
class SemanticAnchor:
    kind: str
    value: str
    start: int
    end: int


_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("url", re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)),
    ("email", re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.IGNORECASE)),
    ("inline_code", re.compile(r"`[^`\n]+`")),
    ("quote_curly", re.compile(r"“[^”\n]+”")),
    ("quote_angle", re.compile(r"«[^»\n]+»")),
    ("quote_ascii", re.compile(r'"[^"\n]+"')),
    ("iso_date", re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")),
    ("slash_date", re.compile(r"(?<!\d)\d{1,2}/\d{1,2}/\d{2,4}(?!\d)")),
    ("percentage", re.compile(r"(?<![\w])\d+(?:[.,]\d+)?\s*%(?!\w)")),
    ("currency_suffix", re.compile(r"(?<![\w])\d+(?:[.,]\d+)?\s*(?:€|EUR|USD|GBP)(?!\w)", re.IGNORECASE)),
    ("currency_prefix", re.compile(r"(?<![\w])(?:€|\$|£)\s*\d+(?:[.,]\d+)?(?!\w)")),
    ("version", re.compile(r"(?<![\w])v?\d+(?:\.\d+){2,}(?![\w])", re.IGNORECASE)),
    ("windows_path", re.compile(r"(?<![\w])(?:[A-Za-z]:\\(?:[^\s\\]+\\)*[^\s\\]+)")),
    ("posix_path", re.compile(r"(?<![\w])/(?:[^\s/]+/)*[^\s/]+")),
    ("number", re.compile(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])")),
)


def _normalise_space(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def extract_semantic_anchors(text: str) -> list[SemanticAnchor]:
    candidates: list[SemanticAnchor] = []
    for kind, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            candidates.append(
                SemanticAnchor(
                    kind=kind,
                    value=match.group(0),
                    start=match.start(),
                    end=match.end(),
                )
            )

    # Prefer the longest anchor at the same/overlapping position. This prevents
    # e.g. the number inside "37%" or "2.4.1" from becoming a second anchor.
    candidates.sort(key=lambda item: (item.start, -(item.end - item.start), item.kind))
    selected: list[SemanticAnchor] = []
    occupied: list[tuple[int, int]] = []
    for item in candidates:
        if any(item.start < end and item.end > start for start, end in occupied):
            continue
        selected.append(item)
        occupied.append((item.start, item.end))

    return sorted(selected, key=lambda item: item.start)


def missing_semantic_anchors(
    original: str,
    output: str,
    *,
    exceptions: Iterable[str] = (),
) -> list[SemanticAnchor]:
    ignored = set(exceptions)
    return [
        anchor
        for anchor in extract_semantic_anchors(original)
        if anchor.value not in ignored and anchor.value not in output
    ]


def change_ratio(original: str, output: str) -> float:
    before = _normalise_space(original)
    after = _normalise_space(output)
    if before == after:
        return 0.0
    if not before and not after:
        return 0.0
    return 1.0 - SequenceMatcher(None, before, after, autojunk=False).ratio()
