from __future__ import annotations

import unittest

from humanizer_support.semantic import (
    change_ratio,
    extract_semantic_anchors,
    missing_semantic_anchors,
)


class SemanticSafetyTests(unittest.TestCase):
    def test_extracts_high_risk_anchors_without_nested_duplicates(self) -> None:
        text = (
            'A versão 2.4.1 baixou 37% em 2026-09-13. '
            'Ver https://example.com/docs e escrever para qa@example.com. '
            'Mantém `response_time` e “Não publicar”.'
        )
        anchors = extract_semantic_anchors(text)
        values = [anchor.value for anchor in anchors]

        self.assertIn("2.4.1", values)
        self.assertIn("37%", values)
        self.assertIn("2026-09-13", values)
        self.assertIn("https://example.com/docs", values)
        self.assertIn("qa@example.com", values)
        self.assertIn("`response_time`", values)
        self.assertIn("“Não publicar”", values)
        self.assertNotIn("37", values)

    def test_reports_missing_anchor(self) -> None:
        missing = missing_semantic_anchors(
            "O desconto é 30% até 2026-10-01.",
            "O desconto mantém-se até 2026-10-01.",
        )
        self.assertEqual([item.value for item in missing], ["30%"])

    def test_change_ratio_is_zero_for_whitespace_only_changes(self) -> None:
        self.assertEqual(change_ratio("Um   texto\ncurto.", "Um texto curto."), 0.0)

    def test_change_ratio_detects_large_rewrite(self) -> None:
        ratio = change_ratio(
            "O relatório está pronto.",
            "Concluímos a análise e apresentamos agora as principais conclusões do estudo.",
        )
        self.assertGreater(ratio, 0.5)


if __name__ == "__main__":
    unittest.main()
