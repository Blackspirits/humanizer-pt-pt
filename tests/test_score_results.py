from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("score_results", ROOT / "evals" / "score-results.py")
assert SPEC and SPEC.loader
score_results = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = score_results
SPEC.loader.exec_module(score_results)


class ScoreResultsTests(unittest.TestCase):
    def test_loose_matching_preserves_diacritic_distinctions(self) -> None:
        case = {"mode": "HUMANIZAR", "must_avoid": ["aceda a conta"], "must_include_one_of": [["aceda à conta"]]}
        response = score_results.parse_response("Aceda à conta.", case["mode"])
        checks = score_results._score_rewrite(case, response)
        self.assertTrue(all(check["ok"] for check in checks), checks)

    def test_rewrite_preserves_exact_name(self) -> None:
        case = {"id": "name", "mode": "QA HUMANO", "input": "Assinado por Antônio Fato.", "must_preserve_exact": ["Antônio Fato"], "must_avoid": ["António Facto"]}
        response = score_results.parse_response("Assinado por Antônio Fato.", case["mode"])
        self.assertTrue(score_results.score_case(case, response)["passed"])

    def test_audit_accepts_expected_pattern_and_original_quote(self) -> None:
        case = {"id": "audit", "mode": "AUDITAR", "input": "No panorama atual, o sistema funciona.", "expected_pattern_ids": [6], "expected_overall_severity": "ligeiro", "must_not_claim_ai_origin": True}
        response = score_results.parse_response({"overall_severity": "ligeiro", "patterns": [{"id": 6, "severity": "clara", "quote": "No panorama atual"}], "summary": "Contextualização genérica."}, case["mode"])
        self.assertTrue(score_results.score_case(case, response)["passed"])

    def test_audit_rejects_invented_quote(self) -> None:
        case = {"id": "audit", "mode": "AUDITAR", "input": "O sistema funciona.", "expected_pattern_ids": [7]}
        response = score_results.parse_response({"overall_severity": "ligeiro", "patterns": [{"id": 7, "severity": "clara", "quote": "frase inexistente"}]}, case["mode"])
        self.assertFalse(score_results.score_case(case, response)["passed"])

    def test_audit_rejects_ai_origin_claim(self) -> None:
        case = {"id": "audit", "mode": "AUDITAR", "input": "No panorama atual.", "expected_pattern_ids": [6], "must_not_claim_ai_origin": True}
        response = score_results.parse_response({"overall_severity": "ligeiro", "patterns": [{"id": 6, "severity": "clara", "quote": "No panorama atual"}], "summary": "O texto foi gerado por IA."}, case["mode"])
        self.assertFalse(score_results.score_case(case, response)["passed"])

    def test_must_not_invent_is_reported_for_manual_review(self) -> None:
        case = {"id": "fabrication", "mode": "HUMANIZAR", "input": "A vila recebe visitantes no verão.", "must_not_invent": ["datas", "número de visitantes"]}
        response = score_results.parse_response("A vila recebe visitantes no verão.", case["mode"])
        result = score_results.score_case(case, response)
        self.assertTrue(result["passed"])
        self.assertTrue(any("datas" in item for item in result["manual_review"]))
        self.assertTrue(any("número de visitantes" in item for item in result["manual_review"]))

    def test_clean_audit_is_not_empty(self) -> None:
        response = score_results.parse_response({"overall_severity": "limpo", "patterns": [], "summary": "Sem padrões."}, "AUDITAR")
        self.assertFalse(score_results.response_is_empty(response, "AUDITAR"))

    def test_semantic_anchor_guard_rejects_changed_number(self) -> None:
        case = {
            "id": "anchors",
            "mode": "QA HUMANO",
            "input": "O desconto é 30% até 2026-10-01.",
            "preserve_semantic_anchors": True,
        }
        response = score_results.parse_response(
            "O desconto é 20% até 2026-10-01.",
            case["mode"],
        )
        result = score_results.score_case(case, response)
        self.assertFalse(result["passed"])

    def test_over_editing_budget_rejects_large_rewrite(self) -> None:
        case = {
            "id": "budget",
            "mode": "QA HUMANO",
            "input": "O relatório está pronto.",
            "max_change_ratio": 0.2,
        }
        response = score_results.parse_response(
            "Concluímos a análise e apresentamos agora as principais conclusões.",
            case["mode"],
        )
        result = score_results.score_case(case, response)
        self.assertFalse(result["passed"])

    def test_over_editing_budget_accepts_unchanged_natural_text(self) -> None:
        case = {
            "id": "budget-clean",
            "mode": "QA HUMANO",
            "input": "O relatório descreve os resultados do ensaio.",
            "max_change_ratio": 0.05,
        }
        response = score_results.parse_response(case["input"], case["mode"])
        result = score_results.score_case(case, response)
        self.assertTrue(result["passed"])


if __name__ == "__main__":
    unittest.main()
