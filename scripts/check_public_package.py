from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES = {
    ".cff",
    ".csv",
    ".gitignore",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}

FORBIDDEN_TEXT = [
    re.compile(r"\b[A-Z]:\\", re.IGNORECASE),
    re.compile(r"\\\\[0-9A-Za-z_.-]+\\"),
    re.compile(r"Users\\Monster", re.IGNORECASE),
    re.compile(r"\brounds[\\/]", re.IGNORECASE),
    re.compile(r"\blogs[\\/]", re.IGNORECASE),
    re.compile(r"paper/draft", re.IGNORECASE),
    re.compile(r"CACAIE", re.IGNORECASE),
    re.compile(r"EESD", re.IGNORECASE),
    re.compile(r"cover_letter", re.IGNORECASE),
    re.compile(r"reviewer_response", re.IGNORECASE),
    re.compile(r"CLAUDE|ChatGPT|Codex", re.IGNORECASE),
    re.compile(r"api[_-]?key|token|password|secret", re.IGNORECASE),
]

FORBIDDEN_FILE_PATTERNS = [
    re.compile(r"\.docx$", re.IGNORECASE),
    re.compile(r"\.npz$", re.IGNORECASE),
    re.compile(r"\.h5$", re.IGNORECASE),
    re.compile(r"\.hdf5$", re.IGNORECASE),
    re.compile(r"\.zip$", re.IGNORECASE),
    re.compile(r"\.7z$", re.IGNORECASE),
    re.compile(r"\.rar$", re.IGNORECASE),
]

REQUIRED_FILES = {
    "README.md",
    "REPRODUCIBLE_RUNBOOK.md",
    "ARTIFACT_QUICKSTART.md",
    "ARTIFACT_SCOPE.md",
    "DATASETS_AND_LINKS.csv",
    "CITATION.cff",
    "LICENSE",
    "MANIFEST.csv",
    "RELEASE_GATE.md",
    "requirements.txt",
    "scripts/rebuild_ground_motion_im_shift_figure.py",
    "scripts/rebuild_pga_shift_figure.py",
    "scripts/write_manifest.py",
    "scripts/check_release_ready.py",
}


def iter_files() -> list[Path]:
    return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]


def main() -> None:
    hits: list[str] = []
    existing = {p.relative_to(ROOT).as_posix() for p in iter_files()}
    for required in sorted(REQUIRED_FILES):
        if required not in existing:
            hits.append(f"required file missing: {required}")

    manifest = ROOT / "MANIFEST.csv"
    if manifest.exists():
        manifest_text = manifest.read_text(encoding="utf-8", errors="replace")
        if "\\" in manifest_text:
            hits.append("MANIFEST.csv contains backslash path separators")

    for path in iter_files():
        rel = path.relative_to(ROOT).as_posix()
        for pattern in FORBIDDEN_FILE_PATTERNS:
            if pattern.search(rel):
                hits.append(f"forbidden file pattern: {rel}")
        if path.name in {".gitignore", "check_public_package.py"}:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in FORBIDDEN_TEXT:
                if pattern.search(text):
                    hits.append(f"forbidden text {pattern.pattern!r}: {rel}")

    if hits:
        print("PUBLIC PACKAGE CHECK FAILED")
        for hit in hits:
            print(f"- {hit}")
        raise SystemExit(1)

    print("PUBLIC PACKAGE CHECK PASSED")
    print(f"Checked {len(iter_files())} files under {ROOT}")


if __name__ == "__main__":
    main()
