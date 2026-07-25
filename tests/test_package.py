from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_validator_passes(self) -> None:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate-package.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_skill_is_compact_and_has_all_modes(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(text.splitlines()), 300)
        for mode in ("AUTO", "AUDITAR", "HUMANIZAR", "QA HUMANO", "CLONAR VOZ"):
            self.assertIn(f"MODO: {mode}", text)

    def test_pattern_ids_are_contiguous(self) -> None:
        text = (ROOT / "references" / "patterns.md").read_text(encoding="utf-8")
        ids = [int(value) for value in re.findall(r"^###\s+(\d+)\.\s+", text, flags=re.MULTILINE)]
        self.assertEqual(ids, list(range(1, 37)))

    def test_docs_are_free_of_ptbr_terms(self) -> None:
        """A documentação da skill não deve conter brasileirismos.

        Excluem-se os ficheiros onde os termos pt-BR são o próprio objeto de
        estudo: o mapa terminológico, o corpus de avaliação e os exemplos
        antes/depois.
        """
        forbidden = (
            r"\broteiro\b",
            r"\busuári[oa]s?\b",
            r"\barquivos? de vídeo\b",
            r"\btela do (?:computador|telemóvel|celular|dispositivo|aplicativo|sistema)\b",
            r"\bcelulares?\b",
            r"\bsalvar (?:o |um |este |esse )?(?:ficheiro|arquivo|documento|projeto|configurações|definições)\b",
            r"\bsenha (?:de acesso|do utilizador|do usuário|da conta)\b",
            r"\baplicativos?\b",
            r"\bgerenciar\b",
            r"\ba equipe (?:de|do|da|responsável|técnica)\b",
            r"\bônibus\b",
            r"\bbaixar (?:um |o |os |um)?arquivos?\b",
            r"\bdeletar\b",
        )
        valid_ptpt_examples = (
            "A tela do pintor está exposta.",
            "O bombeiro conseguiu salvar a vítima.",
            "É preciso tirar uma senha no balcão.",
            "Convém que a empresa equipe os veículos.",
        )
        for example in valid_ptpt_examples:
            self.assertFalse(
                any(re.search(pattern, example.lower()) for pattern in forbidden),
                f"falso positivo em pt-PT válido: {example}",
            )

        exempt = {
            "vocabulary-map.json",
            "evals/cases.json",
            "examples/before-after.md",
            "examples/terminology-overrides.json",
            "references/patterns.md",
            "examples/audit-report.md",
            # O CHANGELOG documenta decisões terminológicas e precisa de nomear
            # os termos que foram corrigidos.
            "CHANGELOG.md",
        }
        offenders: list[str] = []
        for path in sorted(ROOT.rglob("*")):
            # Este teste analisa documentação e dados editoriais; código Python é
            # validado pelos testes próprios e não entra neste varrimento lexical.
            if not path.is_file() or path.suffix not in {".md", ".json", ".yml", ".cff"}:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in exempt or "__pycache__" in rel or rel.startswith("tests/"):
                continue
            lowered = path.read_text(encoding="utf-8").lower()
            for pattern in forbidden:
                if re.search(pattern, lowered):
                    offenders.append(f"{rel}: {pattern}")
        self.assertEqual(offenders, [], f"brasileirismos na documentação: {offenders}")

    def test_contextual_vocabulary_contract(self) -> None:
        data = json.loads((ROOT / "vocabulary-map.json").read_text(encoding="utf-8"))
        mapping = data["pt_br_to_pt_pt"]
        notes = data["context_notes"]
        self.assertNotIn("fato", mapping)
        self.assertIn("nomes_proprios", notes)
        self.assertNotIn("nomes", notes)
        for token in ("facto", "vestuário", "nomes próprios"):
            self.assertIn(token, notes["fato"].lower())
        for token in ("scene/p2p", "torrents", "multimédia"):
            self.assertIn(token, notes["release"].lower())
        self.assertIn("release", data["preserve_if_project_uses"])
        for token in ("aceder ao sistema", "aceder à conta", "nunca produzir"):
            self.assertIn(token, notes["acessar"].lower())
        for token in ("criar conta", "registar", "inscrever"):
            self.assertIn(token, notes["cadastrar"].lower())
        for token in ("open source", "código aberto", "free software", "software livre"):
            self.assertIn(token, notes["software_livre"].lower())
        for token in ("equipa", "código", "tempo"):
            self.assertIn(token, notes["time"].lower())
        self.assertTrue(data["rules"]["multi_option_requires_context_note"])
        self.assertTrue(data["rules"]["single_option_requires_context_note_if_polysemous"])
        for key in ("salvar", "senha", "controle", "equipe", "registro"):
            self.assertIn(key, notes)
        missing = [
            key for key, values in mapping.items()
            if isinstance(values, list) and len(values) > 1 and key not in notes
        ]
        self.assertEqual(missing, [])

    def test_regency_and_software_evals_exist(self) -> None:
        data = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in data["cases"]}
        required = {
            "ptbr-acessar-regencia-001",
            "ptbr-acessar-regencia-contracao-001",
            "ptbr-cadastrar-ui-001",
            "ptbr-cadastrar-entidade-001",
            "ptbr-cadastrar-inscricao-001",
            "technical-software-concepts-001",
            "ptbr-time-equipa-001",
            "technical-time-identifier-001",
        }
        self.assertTrue(required.issubset(ids))

    def test_audit_overall_severity_has_full_coverage(self) -> None:
        data = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        severities = {
            case.get("expected_overall_severity")
            for case in data["cases"]
            if case.get("mode") == "AUDITAR"
        }
        self.assertTrue({"limpo", "ligeiro", "moderado", "pesado"}.issubset(severities))

    def test_pattern_examples_preserve_information_and_show_false_positives(self) -> None:
        text = (ROOT / "references" / "patterns.md").read_text(encoding="utf-8")
        self.assertIn("passou de quatro para dois segundos", text)
        self.assertIn("Manter quando:", text)
        self.assertIn("preserva todos os factos concretos", text)

    def test_release_archives_have_identical_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "package-release.py"), "--output", tmp],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            zip_path = next(Path(tmp).glob("*.zip"))
            tar_path = next(Path(tmp).glob("*.tar.gz"))
            self.assertTrue((Path(tmp) / "SHA256SUMS").is_file())
            with zipfile.ZipFile(zip_path) as zf:
                zip_data = {name: zf.read(name) for name in zf.namelist() if not name.endswith("/")}
            with tarfile.open(tar_path, "r:gz") as tf:
                tar_data = {
                    member.name: tf.extractfile(member).read()
                    for member in tf.getmembers()
                    if member.isfile()
                }
            self.assertEqual(zip_data, tar_data)


if __name__ == "__main__":
    unittest.main()
