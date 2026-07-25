#!/usr/bin/env python3
"""Cria ficheiros de distribuição determinísticos para humanizer-pt-pt."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import re
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "dist", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def read_version() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"^[ \t]+version:\s*[\"']?([^\"'\n]+)", text, flags=re.MULTILINE)
    if not match:
        raise SystemExit("ERRO: versão não encontrada em SKILL.md")
    return match.group(1).strip()


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def create_zip(target: Path, files: list[Path]) -> None:
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            rel = Path(ROOT.name) / path.relative_to(ROOT)
            info = zipfile.ZipInfo(rel.as_posix(), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.stat().st_mode & 0o111 else 0o644) << 16
            archive.writestr(info, path.read_bytes())


def create_tar_gz(target: Path, files: list[Path]) -> None:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for path in files:
            rel = Path(ROOT.name) / path.relative_to(ROOT)
            data = path.read_bytes()
            info = tarfile.TarInfo(rel.as_posix())
            info.size = len(data)
            info.mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            archive.addfile(info, io.BytesIO(data))
    with target.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0, compresslevel=9) as gz:
            gz.write(raw.getvalue())


def archive_entries(path: Path) -> dict[str, bytes]:
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            return {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
    with tarfile.open(path, "r:gz") as archive:
        return {
            member.name: archive.extractfile(member).read()
            for member in archive.getmembers()
            if member.isfile()
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(ROOT / "dist"), help="pasta de destino")
    parser.add_argument("--skip-validation", action="store_true", help="não executa o validador")
    args = parser.parse_args()

    if not args.skip_validation:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "validate-package.py")], cwd=ROOT, check=True)

    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    version = read_version()
    files = iter_files()
    zip_path = output / f"humanizer-pt-pt-v{version}.zip"
    tar_path = output / f"humanizer-pt-pt-v{version}.tar.gz"
    create_zip(zip_path, files)
    create_tar_gz(tar_path, files)

    if archive_entries(zip_path) != archive_entries(tar_path):
        raise SystemExit("ERRO: ZIP e TAR.GZ não contêm os mesmos ficheiros")

    sums = []
    for archive_path in (zip_path, tar_path):
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        sums.append(f"{digest}  {archive_path.name}")
    sums_path = output / "SHA256SUMS"
    sums_path.write_text("\n".join(sums) + "\n", encoding="utf-8")

    print(f"OK: {zip_path}")
    print(f"OK: {tar_path}")
    print(f"OK: {sums_path}")
    print(f"Ficheiros: {len(files)}")


if __name__ == "__main__":
    main()
