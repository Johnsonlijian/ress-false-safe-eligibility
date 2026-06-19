from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


BLOCKING_PATTERNS = [
    (ROOT / "CITATION.cff", re.compile(r"Author metadata to be completed", re.IGNORECASE), "CITATION.cff still contains author-metadata placeholder"),
    (ROOT / "CITATION.cff", re.compile(r"\[.*?\]"), "CITATION.cff contains bracketed placeholder text"),
]


def main() -> int:
    errors: list[str] = []
    for path, pattern, message in BLOCKING_PATTERNS:
        if not path.exists():
            errors.append(f"missing release file: {path.relative_to(ROOT).as_posix()}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if pattern.search(text):
            errors.append(message)

    if errors:
        print("RELEASE READY CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RELEASE READY CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
