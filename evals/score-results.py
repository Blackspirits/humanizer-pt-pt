#!/usr/bin/env python3
"""Avalia respostas contra o corpus de humanizer-pt-pt.

O runner verifica critérios objetivos. Critérios editoriais subjetivos ficam em
``manual_checks`` e são apresentados para revisão humana.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "cases.json"
REWRITE_MODES = {"HUMANIZAR", "QA HUMANO", "CLONAR VOZ", "AUTO"}
VALID_MODES = REWRITE_MODES | {"AUDITAR"}
AUDIT_SEVERITIES = {"ligeira", "clara", "grave"}
OVERALL_SEVERITIES = {"limpo", "ligeiro", "moderado", "pesado"}
AI_ORIGIN_CLAIMS = (
    r"\b\d+(?:[.,]\d+)?\s*%\b.{0,40}\b(?:ia|inteligência artificial)\b",
    r"\b(?:ia|inteligência artificial)\b.{0,40}\b\d+(?:[.,]\d+)?\s*%\b",
    r"\b(?:foi|parece ter sido)\s+(?:escrito|gerado|produzido)\s+por\s+(?:ia|inteligência artificial)\b",
    r"\bprobabilidade\b.{0,40}\b(?:ia|inteligência artificial)\b",
    r"\borigem\s+(?:humana|ia)\b",
)


@dataclass
class ResponseData:
    output: str = ""
    selected_mode: str | None = None
    overall_severity: str | None = None
    patterns: list[dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    raw: Any = None


def normalise(text: str) -> str:
    return unicodedata.normalize("NFC", text.casefold())


def contains(haystack: str, needle: str, *, exact_case: bool = False) -> bool:
    return needle in haystack if exact_case else normalise(needle) in normalise(haystack)


def parse_response(value: Any, mode: str) -> ResponseData:
    if mode == "AUDITAR":
        if not isinstance(value, dict):
            raise ValueError("uma resposta AUDITAR deve ser um objeto")
        severity = value.get("overall_severity")
        patterns = value.get("patterns")
        summary = value.get("summary", "")
        if not isinstance(severity, str):
            raise ValueError("o campo 'overall_severity' deve ser texto")
        if not isinstance(patterns, list):
            raise ValueError("o campo 'patterns' deve ser uma lista")
        if not isinstance(summary, str):
            raise ValueError("o campo 'summary' deve ser texto")
        return ResponseData(overall_severity=severity.strip().casefold(), patterns=patterns, summary=summary, raw=value)

    if isinstance(value, str):
        return ResponseData(output=value, raw=value)
    if isinstance(value, dict):
        output = value.get("output")
        selected_mode = value.get("selected_mode")
        if not isinstance(output, str):
            raise ValueError("o campo 'output' deve ser texto")
        if selected_mode is not None and not isinstance(selected_mode, str):
            raise ValueError("o campo 'selected_mode' deve ser texto")
        return ResponseData(output=output, selected_mode=selected_mode, raw=value)
    raise ValueError("a resposta deve ser texto ou objeto")


def _record(checks: list[dict[str, Any]], name: str, ok: bool, detail: str = "") -> None:
    checks.append({"check": name, "ok": ok, "detail": detail})


def _score_rewrite(case: dict[str, Any], response: ResponseData) -> list[dict[str, Any]]:
    output = response.output
    checks: list[dict[str, Any]] = []
    for term in case.get("must_avoid", []):
        present = contains(output, term)
        _record(checks, f"must_avoid: {term!r}", not present, "presente na resposta" if present else "")
    for literal in case.get("must_preserve_exact", []):
        present = contains(output, literal, exact_case=True)
        _record(checks, f"must_preserve_exact: {literal!r}", present, "" if present else "literal em falta ou alterado")
    for item in case.get("must_preserve", []):
        present = contains(output, item)
        _record(checks, f"must_preserve: {item!r}", present, "" if present else "conteúdo esperado em falta")
    for group in case.get("must_include_one_of", []):
        present = any(contains(output, option) for option in group)
        _record(checks, f"must_include_one_of: {group!r}", present, "" if present else "nenhuma alternativa presente")
    max_words = case.get("max_words")
    if isinstance(max_words, int):
        words = len(output.split())
        _record(checks, f"max_words <= {max_words}", words <= max_words, f"palavras={words}")
    if case.get("preferred_output_shape") == "short UI label":
        compact = output.strip()
        words = len(compact.split())
        ok = "\n" not in compact and words <= 6 and not compact.endswith((".", ";", ":"))
        _record(checks, "short UI label", ok, f"palavras={words}")
    expected = case.get("expected_mode_selection")
    if expected:
        chosen = response.selected_mode.strip().upper() if response.selected_mode else None
        _record(checks, f"selected_mode == {expected}", chosen == expected, f"selecionado={chosen!r}")
    return checks


def _score_audit(case: dict[str, Any], response: ResponseData) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    severity = response.overall_severity or ""
    _record(checks, "overall_severity válida", severity in OVERALL_SEVERITIES, f"valor={severity!r}")
    ids: list[int] = []
    invalid_items = 0
    quotes_outside_input: list[str] = []
    for index, item in enumerate(response.patterns):
        if not isinstance(item, dict):
            invalid_items += 1
            continue
        pid = item.get("id")
        item_severity = item.get("severity")
        quote = item.get("quote")
        if not isinstance(pid, int) or not 1 <= pid <= 36:
            invalid_items += 1
        else:
            ids.append(pid)
        if not isinstance(item_severity, str) or item_severity.casefold() not in AUDIT_SEVERITIES:
            invalid_items += 1
        if not isinstance(quote, str) or not quote.strip():
            invalid_items += 1
        elif quote not in case["input"]:
            quotes_outside_input.append(f"#{index + 1}: {quote!r}")
    _record(checks, "estrutura dos padrões", invalid_items == 0, f"erros={invalid_items}")
    _record(checks, "excertos pertencem ao original", not quotes_outside_input, "; ".join(quotes_outside_input))
    _record(checks, "IDs sem duplicados", len(ids) == len(set(ids)), f"ids={ids}")
    expected_ids = set(case.get("expected_pattern_ids", []))
    missing_ids = sorted(expected_ids - set(ids))
    _record(checks, f"expected_pattern_ids: {sorted(expected_ids)}", not missing_ids, f"em falta={missing_ids}")
    forbidden_ids = set(case.get("forbidden_pattern_ids", []))
    found_forbidden = sorted(forbidden_ids & set(ids))
    _record(checks, f"forbidden_pattern_ids: {sorted(forbidden_ids)}", not found_forbidden, f"encontrados={found_forbidden}")
    expected_severity = case.get("expected_overall_severity")
    if expected_severity:
        _record(checks, f"overall_severity == {expected_severity}", severity == expected_severity, f"valor={severity!r}")
    if case.get("must_not_claim_ai_origin"):
        serialised = json.dumps(response.raw, ensure_ascii=False).casefold()
        matches = [pattern for pattern in AI_ORIGIN_CLAIMS if re.search(pattern, serialised, flags=re.IGNORECASE)]
        _record(checks, "sem afirmação de origem humana/IA", not matches, f"padrões encontrados={matches}")
    return checks


def score_case(case: dict[str, Any], response: ResponseData) -> dict[str, Any]:
    checks = _score_audit(case, response) if case["mode"] == "AUDITAR" else _score_rewrite(case, response)
    manual_review = list(case.get("manual_checks", []))
    for item in case.get("must_not_invent", []):
        item_text = str(item)
        if not any(normalise(item_text) in normalise(check) for check in manual_review):
            manual_review.append(f"Confirmar que a resposta não inventa: {item_text}.")
    return {"id": case["id"], "mode": case["mode"], "checks": checks, "manual_review": manual_review, "passed": all(check["ok"] for check in checks)}


def load_cases() -> list[dict[str, Any]]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"]


def select_cases(cases: list[dict[str, Any]], selected: Iterable[str]) -> list[dict[str, Any]]:
    requested = list(selected)
    if not requested:
        return cases
    by_id = {case["id"]: case for case in cases}
    unknown = sorted(set(requested) - set(by_id))
    if unknown:
        raise SystemExit("ERRO: casos desconhecidos: " + ", ".join(unknown))
    return [by_id[cid] for cid in requested]


def make_template(cases: list[dict[str, Any]]) -> None:
    template: dict[str, Any] = {}
    for case in cases:
        if case["mode"] == "AUTO":
            template[case["id"]] = {"selected_mode": "", "output": ""}
        elif case["mode"] == "AUDITAR":
            template[case["id"]] = {"overall_severity": "", "patterns": [], "summary": ""}
        else:
            template[case["id"]] = ""
    print(json.dumps(template, ensure_ascii=False, indent=2))


def response_is_empty(response: ResponseData, mode: str) -> bool:
    if mode == "AUDITAR":
        return response.overall_severity is None
    return not response.output.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", nargs="?", help="ficheiro JSON com respostas")
    parser.add_argument("--template", action="store_true", help="gera um esqueleto de respostas")
    parser.add_argument("--list", action="store_true", help="lista os IDs do corpus")
    parser.add_argument("--case", action="append", default=[], help="avalia apenas este ID; pode repetir")
    parser.add_argument("--allow-partial", action="store_true", help="permite avaliar apenas parte do corpus")
    parser.add_argument("--report-json", help="guarda o relatório detalhado neste caminho")
    args = parser.parse_args()
    all_cases = load_cases()
    cases = select_cases(all_cases, args.case)
    if args.list:
        for case in cases:
            print(f"{case['id']}\t{case['mode']}")
        return
    if args.template:
        make_template(cases)
        return
    if not args.responses:
        parser.error("indica responses.json ou usa --template")
    path = Path(args.responses)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("ERRO: responses.json deve conter um objeto na raiz")
    known = {case["id"] for case in all_cases}
    unknown = sorted(set(data) - known)
    if unknown:
        raise SystemExit("ERRO: IDs desconhecidos: " + ", ".join(unknown))
    missing: list[str] = []
    failed: list[str] = []
    results: list[dict[str, Any]] = []
    passed = total = manual_count = 0
    for case in cases:
        cid = case["id"]
        if cid not in data:
            missing.append(cid)
            continue
        try:
            response = parse_response(data[cid], case["mode"])
        except ValueError as exc:
            print(f"[ FALHA] {cid}: {exc}")
            failed.append(cid)
            total += 1
            continue
        if response_is_empty(response, case["mode"]):
            missing.append(cid)
            continue
        total += 1
        result = score_case(case, response)
        results.append(result)
        manual_count += len(result["manual_review"])
        tag = "  OK  " if result["passed"] else " FALHA"
        if result["passed"]:
            passed += 1
        else:
            failed.append(cid)
        print(f"[{tag}] {cid} ({result['mode']})")
        for check in result["checks"]:
            if not check["ok"]:
                print(f"         x {check['check']} — {check['detail']}")
        for item in result["manual_review"]:
            print(f"         ? revisão manual: {item}")
    if missing:
        print(f"[  --  ] sem resposta: {', '.join(missing)}")
    print(f"\nAutomático: {passed}/{total} casos avaliados passaram.")
    print(f"Revisão manual pendente: {manual_count} critérios.")
    if args.report_json:
        report = {"summary": {"passed": passed, "evaluated": total, "missing": missing, "failed": failed, "manual_checks": manual_count}, "results": results}
        Path(args.report_json).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failed or (missing and not args.allow_partial):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
