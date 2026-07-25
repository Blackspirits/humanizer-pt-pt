#!/usr/bin/env python3
"""Validação sem dependências do pacote humanizer-pt-pt."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAME = "humanizer-pt-pt"
EXPECTED_VERSION = "1.0.0"
EXPECTED_PATTERN_COUNT = 36
VALID_MODES = {"AUTO", "AUDITAR", "HUMANIZAR", "QA HUMANO", "CLONAR VOZ"}
REQUIRED_FILES = [
    ".editorconfig",
    ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json",
    ".github/workflows/validate.yml",
    "AGENTS.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "LICENSE",
    "NOTICE",
    "README.en.md",
    "README.md",
    "SKILL.md",
    "evals/README.md",
    "evals/cases.json",
    "evals/score-results.py",
    "examples/audit-report.md",
    "examples/before-after.md",
    "examples/terminology-overrides.json",
    "profiles/blackspirits.md",
    "references/composition.md",
    "references/formats.md",
    "references/patterns.md",
    "references/regional-variation.md",
    "scripts/package-release.py",
    "scripts/validate-package.py",
    "tests/test_package.py",
    "tests/test_score_results.py",
    "vocabulary-map.json",
]


def fail(message: str) -> None:
    print(f"ERRO: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"ficheiro em falta: {relative_path}")


def load_json(relative_path: str) -> dict[str, Any]:
    try:
        data = json.loads(read(relative_path))
    except json.JSONDecodeError as exc:
        fail(f"JSON inválido em {relative_path}: {exc}")
    if not isinstance(data, dict):
        fail(f"{relative_path} deve conter um objeto JSON na raiz")
    return data


def parse_skill_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md não começa com frontmatter YAML")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail("frontmatter de SKILL.md não foi fechado")
    frontmatter = text[4:end]
    name_match = re.search(r"^name:\s*([^\n]+)$", frontmatter, flags=re.MULTILINE)
    version_match = re.search(
        r"^metadata:\s*\n(?:^[ \t]+.*\n)*?^[ \t]+version:\s*[\"']?([^\"'\n]+)",
        frontmatter,
        flags=re.MULTILINE,
    )
    if not name_match:
        fail("name não encontrado em SKILL.md")
    if not version_match:
        fail("metadata.version não encontrado em SKILL.md")
    return name_match.group(1).strip(), version_match.group(1).strip()


def validate_required_files() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        fail("ficheiros obrigatórios em falta: " + ", ".join(missing))


def validate_skill() -> str:
    text = read("SKILL.md")
    skill_name, version = parse_skill_frontmatter(text)
    if skill_name != EXPECTED_NAME:
        fail(f"nome incorreto em SKILL.md: {skill_name!r}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name):
        fail(f"nome inválido em SKILL.md: {skill_name!r}")
    if ROOT.name != skill_name:
        fail(f"nome da pasta ({ROOT.name!r}) não corresponde à skill ({skill_name!r})")
    if len(text.splitlines()) >= 300:
        fail("SKILL.md deve manter-se abaixo de 300 linhas; move detalhe para references/")

    required_phrases = [
        "MODO: AUTO",
        "MODO: AUDITAR",
        "MODO: HUMANIZAR",
        "MODO: QA HUMANO",
        "MODO: CLONAR VOZ",
        "Nunca inventes",
        "Preserva elementos literais",
        "Não atribuas percentagens de IA",
        "Falsos positivos",
        "Checklist final",
        "Claude Code 2.1.143+",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            fail(f"SKILL.md não contém a regra obrigatória: {phrase}")
    for ref in (
        "references/patterns.md",
        "references/composition.md",
        "references/formats.md",
        "references/regional-variation.md",
    ):
        if ref not in text:
            fail(f"SKILL.md não referencia o ficheiro de apoio: {ref}")
    return version


def validate_references() -> None:
    patterns = read("references/patterns.md")
    ids = [
        int(match.group(1))
        for match in re.finditer(r"^###\s+(\d+)\.\s+", patterns, flags=re.MULTILINE)
    ]
    if ids != list(range(1, EXPECTED_PATTERN_COUNT + 1)):
        fail(f"numeração dos padrões inválida: {ids}")
    for phrase in (
        "O travessão é válido em português. Não o proíbas.",
        "notoriedade por associação",
        "capitalização importada",
        "É aqui que tudo muda",
        "passou de quatro para dois segundos",
        "Manter quando:",
    ):
        if phrase not in patterns:
            fail(f"references/patterns.md não contém: {phrase}")

    composition = read("references/composition.md")
    for phrase in (
        "Nunca inventes um agente",
        "A falta de dados resolve-se com contenção, não com ficção.",
        "exatidão e não invenção",
    ):
        if phrase not in composition:
            fail(f"references/composition.md não contém: {phrase}")

    formats = read("references/formats.md")
    for heading in (
        "## Guião e texto falado",
        "## Tradução e localização",
        "## Commit, pull request, changelog e notas de versão",
    ):
        if heading not in formats:
            fail(f"references/formats.md não contém: {heading}")


def validate_versions(skill_version: str) -> None:
    sources = {
        "SKILL.md": skill_version,
        "vocabulary-map.json": load_json("vocabulary-map.json").get("metadata", {}).get("version"),
        "evals/cases.json": load_json("evals/cases.json").get("metadata", {}).get("version"),
        ".claude-plugin/plugin.json": load_json(".claude-plugin/plugin.json").get("version"),
        ".claude-plugin/marketplace.json": load_json(".claude-plugin/marketplace.json").get("version"),
    }
    citation = read("CITATION.cff")
    citation_match = re.search(r"^version:\s*([^\s]+)$", citation, flags=re.MULTILINE)
    sources["CITATION.cff"] = citation_match.group(1) if citation_match else None
    for source, version in sources.items():
        if version != EXPECTED_VERSION:
            fail(f"versão incorreta em {source}: {version!r}")


def validate_vocabulary() -> None:
    data = load_json("vocabulary-map.json")
    mapping = data.get("pt_br_to_pt_pt")
    if not isinstance(mapping, dict) or not mapping:
        fail("pt_br_to_pt_pt está vazio ou inválido")
    serialised = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for source, target in {"fato": "facto", "Antônio": "António", "fila": "bicha"}.items():
        if re.search(rf'"{re.escape(source)}":(?:"{re.escape(target)}"|\["{re.escape(target)}"\])', serialised):
            fail(f"substituição cega proibida: {source} -> {target}")
    boleto = mapping.get("boleto", [])
    values = boleto if isinstance(boleto, list) else [boleto]
    if any("multibanco" in str(value).casefold() for value in values):
        fail("boleto não deve mapear para referência Multibanco")
    notes = data.get("context_notes", {})
    for key in ("fato", "nomes_proprios", "arquivo", "você", "boleto", "release", "time", "roteiro", "acessar", "cadastrar", "cadastro", "software_livre"):
        if key not in notes:
            fail(f"falta nota contextual obrigatória para {key!r}")
    if "fato" in mapping:
        fail("'fato' não deve ter mapeamento direto; o sentido decide entre 'fato' e 'facto'")
    fato_note = str(notes.get("fato", "")).casefold()
    if not all(term in fato_note for term in ("facto", "vestuário", "nomes próprios")):
        fail("a nota contextual de 'fato' deve distinguir sentido factual, vestuário e nomes próprios")
    release_note = str(notes.get("release", "")).casefold()
    if not any(term in release_note for term in ("scene/p2p", "torrent")) or "multimédia" not in release_note:
        fail("a nota contextual de 'release' deve cobrir Scene/P2P, torrents e multimédia")
    if "release" not in data.get("preserve_if_project_uses", []):
        fail("'release' deve constar de preserve_if_project_uses")
    acessar_note = str(notes.get("acessar", "")).casefold()
    if not all(term in acessar_note for term in ("aceder ao sistema", "aceder à conta", "nunca produzir")):
        fail("a nota de 'acessar' deve documentar a regência e as contrações de 'aceder a'")
    cadastrar_note = str(notes.get("cadastrar", "")).casefold()
    if not all(term in cadastrar_note for term in ("criar conta", "registar", "inscrever")):
        fail("a nota de 'cadastrar' deve distinguir conta, registo de entidade e inscrição")
    software_note = str(notes.get("software_livre", "")).casefold()
    if not all(term in software_note for term in ("open source", "código aberto", "free software", "software livre")):
        fail("a nota de software deve distinguir open source de free software")
    time_note = str(notes.get("time", "")).casefold()
    if not all(term in time_note for term in ("equipa", "código", "tempo")):
        fail("a nota de 'time' deve distinguir equipa, identificadores e tempo")
    roteiro_values = mapping.get("roteiro", [])
    if not all(term in roteiro_values for term in ("guião", "plano", "itinerário")):
        fail("o mapeamento contextual de 'roteiro' está incompleto")

    rules = data.get("rules", {})
    if rules.get("multi_option_requires_context_note") is not True:
        fail("multi_option_requires_context_note deve ser true")
    ambiguous_without_note = sorted(
        key for key, value in mapping.items()
        if isinstance(value, list) and len(value) > 1 and key not in notes
    )
    if ambiguous_without_note:
        fail("mapeamentos com várias opções sem nota contextual: " + ", ".join(ambiguous_without_note))
    for flag in ("never_blind_replace", "preserve_proper_names", "preserve_quotes", "preserve_code_and_identifiers"):
        if rules.get(flag) is not True:
            fail(f"{flag} deve ser true")


def _list_of_strings(case: dict[str, Any], field: str, case_id: str) -> None:
    value = case.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(f"campo {field} inválido no caso {case_id}")


def validate_evals() -> None:
    data = load_json("evals/cases.json")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 45:
        fail("evals/cases.json deve conter pelo menos 45 casos")
    ids: list[str] = []
    modes: set[str] = set()
    audit_count = 0

    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            fail(f"caso #{index} não é um objeto")
        case_id = case.get("id")
        mode = case.get("mode")
        text = case.get("input")
        if not isinstance(case_id, str) or not case_id:
            fail(f"caso #{index} sem id válido")
        if not isinstance(text, str) or not text:
            fail(f"caso {case_id} sem input válido")
        if mode not in VALID_MODES:
            fail(f"modo inválido no caso {case_id}: {mode!r}")
        for field in ("must_avoid", "must_preserve", "must_preserve_exact", "manual_checks"):
            _list_of_strings(case, field, case_id)
        groups = case.get("must_include_one_of", [])
        if not isinstance(groups, list) or not all(
            isinstance(group, list) and group and all(isinstance(item, str) for item in group)
            for group in groups
        ):
            fail(f"must_include_one_of inválido no caso {case_id}")
        if mode == "CLONAR VOZ" and not isinstance(case.get("voice_sample"), str):
            fail(f"caso {case_id} de CLONAR VOZ sem voice_sample")
        if mode == "AUTO" and case.get("expected_mode_selection") not in {"HUMANIZAR", "QA HUMANO"}:
            fail(f"caso AUTO {case_id} sem expected_mode_selection válido")
        if mode == "AUDITAR":
            audit_count += 1
            for field in ("expected_pattern_ids", "forbidden_pattern_ids"):
                value = case.get(field, [])
                if not isinstance(value, list) or not all(isinstance(item, int) and 1 <= item <= 36 for item in value):
                    fail(f"campo {field} inválido no caso {case_id}")
            severity = case.get("expected_overall_severity")
            if severity not in {"limpo", "ligeiro", "moderado", "pesado"}:
                fail(f"gravidade geral inválida no caso {case_id}")
            if case.get("must_not_claim_ai_origin") is not True:
                fail(f"caso AUDITAR {case_id} deve proibir afirmações de origem IA")
        ids.append(case_id)
        modes.add(mode)

    required_context_cases = {
        "proper-name-001",
        "ptbr-fato-factual-001",
        "ptpt-fato-vestuario-001",
        "technical-release-scene-001",
        "ptbr-roteiro-video-001",
        "ptbr-roteiro-viagem-001",
        "ptbr-acessar-regencia-001",
        "ptbr-acessar-regencia-contracao-001",
        "ptbr-cadastrar-ui-001",
        "ptbr-cadastrar-entidade-001",
        "ptbr-cadastrar-inscricao-001",
        "technical-software-concepts-001",
        "ptbr-time-equipa-001",
        "technical-time-identifier-001",
    }
    missing_context_cases = required_context_cases.difference(ids)
    if missing_context_cases:
        fail("faltam avaliações contextuais: " + ", ".join(sorted(missing_context_cases)))
    if len(ids) != len(set(ids)):
        fail("existem IDs de avaliação duplicados")
    if modes != VALID_MODES:
        fail(f"cobertura de modos incompleta: {sorted(modes)}")
    if audit_count < 3:
        fail("devem existir pelo menos três avaliações AUDITAR")


def validate_license_and_attribution() -> None:
    license_text = read("LICENSE")
    notice_text = read("NOTICE")
    for required in ("Siqi Chen", "Filipe Mota", "MIT License"):
        if required not in license_text:
            fail(f"LICENSE não contém {required!r}")
    for required in ("blader/humanizer", "not a literal translation"):
        if required not in notice_text:
            fail(f"NOTICE não contém {required!r}")


def validate_manifests() -> None:
    plugin = load_json(".claude-plugin/plugin.json")
    marketplace = load_json(".claude-plugin/marketplace.json")
    if plugin.get("name") != EXPECTED_NAME:
        fail("nome incorreto em plugin.json")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("marketplace.json deve declarar exatamente um plugin")
    if plugins[0].get("name") != EXPECTED_NAME or plugins[0].get("source") != "./":
        fail("plugin inválido em marketplace.json")
    if "version" in plugins[0]:
        fail("não duplicar a versão na entrada do plugin; plugin.json é a fonte de verdade")
    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or owner.get("name") != "BlackSpirits":
        fail("owner inválido em marketplace.json")
    if set(owner) - {"name", "email"}:
        fail("marketplace.owner contém campos não suportados")
    if "displayName" in marketplace:
        fail("displayName não é um campo de topo suportado em marketplace.json")
    expected_url = "https://github.com/Blackspirits/humanizer-pt-pt"
    for field in ("homepage", "repository"):
        if plugin.get(field) != expected_url:
            fail(f"URL incorreto em plugin.json ({field})")


def validate_documentation_and_ci() -> None:
    checked = ["README.md", "README.en.md", "AGENTS.md", "CONTRIBUTING.md"]
    combined = "\n".join(read(name) for name in checked)
    for stale in ("tests/cases.json", "Blackspirits/humanizer-pt-PT", "humanizer-pt-PT"):
        if stale in combined:
            fail(f"documentação desatualizada: {stale}")
    for required in ("AUDITAR", "references/composition.md", "evals/score-results.py"):
        if required not in combined:
            fail(f"documentação não menciona: {required}")

    workflow = read(".github/workflows/validate.yml")
    for required in (
        "python -m unittest discover -s tests -v",
        "python scripts/package-release.py",
        "claude-code plugin validate",
    ):
        if required not in workflow:
            fail(f"CI não contém: {required}")
    if "|| echo" in workflow or "continue-on-error: true" in workflow:
        fail("a CI não deve ocultar falhas de validação")


def validate_markdown_integrity() -> None:
    markdown_files = [path for path in ROOT.rglob("*.md") if ".git" not in path.parts]
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        if text.count("```") % 2:
            fail(f"bloco de código não fechado em {path.relative_to(ROOT)}")
        for target in link_pattern.findall(text):
            clean = target.split("#", 1)[0].strip()
            if not clean or clean.startswith(("http://", "https://", "mailto:", "#")):
                continue
            candidate = (path.parent / clean).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"link relativo sai do repositório em {path.relative_to(ROOT)}: {target}")
            if not candidate.exists():
                fail(f"link interno quebrado em {path.relative_to(ROOT)}: {target}")


def main() -> None:
    validate_required_files()
    skill_version = validate_skill()
    validate_references()
    validate_versions(skill_version)
    validate_vocabulary()
    validate_evals()
    validate_license_and_attribution()
    validate_manifests()
    validate_documentation_and_ci()
    validate_markdown_integrity()
    print(
        f"OK: {EXPECTED_NAME} {skill_version}; "
        f"{EXPECTED_PATTERN_COUNT} padrões; pacote validado."
    )


if __name__ == "__main__":
    main()
