"""Write the excuse entry to a file, checking it against the bounty gate first."""

import argparse
import sys
from pathlib import Path

ENTRY = "Sorry boss, my optician dilated my eyes this morning, I can't look at a screen till it wears off."

MAX_CHARS = 140
MAX_WORDS = 20


def check_entry(line: str) -> list[str]:
    """Return a list of gate failures; empty means the line is valid."""
    problems = []
    if not line.strip():
        problems.append("entry is blank")
    if len(line) > MAX_CHARS:
        problems.append(f"entry is {len(line)} characters (limit {MAX_CHARS})")
    if "\n" in line or "\r" in line:
        problems.append("entry must be exactly one line")
    if len(line.split()) > MAX_WORDS:
        problems.append(f"entry has {len(line.split())} words (limit {MAX_WORDS})")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the excuse entry file.")
    parser.add_argument("--output", default="/output/entry.txt",
                        help="path to write the entry to")
    parser.add_argument("--dry-run", action="store_true",
                        help="validate and print the entry without writing")
    args = parser.parse_args()

    problems = check_entry(ENTRY)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    words = len(ENTRY.split())
    print(f"entry: {ENTRY}")
    print(f"characters: {len(ENTRY)}, words: {words}")

    if args.dry_run:
        return 0

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(ENTRY.encode("utf-8"))

    if target.read_bytes() != ENTRY.encode("utf-8"):
        print("error: read-back does not match the entry", file=sys.stderr)
        return 1

    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
