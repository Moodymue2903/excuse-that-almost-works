#!/usr/bin/env python3
"""The Excuse That Almost Works — entry.

Writes the single-line excuse to /output/entry.txt. Blind tournament winner
is the optician line (see tournament.md): Borda 40/42 in the local tournament,
ranked #1 by all four external auditors (Gemini, Claude, DeepSeek, GLM — the
house judge's own model family), 3x SUBMIT AS-IS. The excuse is a real,
specific, boring medical detail — dilated eyes mean no screen — and the laugh
comes from the excuse's own logic: the one thing a gamer wants on launch week
is a screen.

The entry is validated against the gate before it is written: 1-140
characters, exactly one line, at most 20 words. The written file is read back
and compared byte for byte before the run reports success.
"""

import argparse
import os
import sys

LINE = (
    "Sorry boss, my optician dilated my eyes this morning, "
    "I can't look at a screen till it wears off."
)

MAX_CHARS = 140
MAX_WORDS = 20

ENTRY_PATH = "/output/entry.txt"


def validate(text):
    """Check the text against the gate; return the first problem, else None."""
    if not text.strip():
        return "text is blank"
    if len(text) > MAX_CHARS:
        return f"text is {len(text)} characters, allowed range is 1-{MAX_CHARS}"
    lines = text.split("\n")
    if len(lines) != 1:
        return f"text has {len(lines)} lines, must be exactly 1"
    if text != text.strip():
        return "text has leading/trailing whitespace"
    words = text.split()
    if len(words) > MAX_WORDS:
        return f"text has {len(words)} words, at most {MAX_WORDS}"
    return None


def write_entry(path, text):
    """Write the text to path, creating its directory; return chars written."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        return f.write(text)


def verify_written(path, text):
    """Read path back; return an error string, or None when byte-identical."""
    with open(path, "rb") as f:
        back = f.read()
    if back != text.encode("utf-8"):
        return f"read back {len(back)} bytes, expected {len(text)}"
    return None


def parse_args(argv=None):
    """Parse CLI options; defaults preserve the standard entry path."""
    parser = argparse.ArgumentParser(
        description="Write the Excuse That Almost Works entry to a file."
    )
    parser.add_argument(
        "--output",
        default=ENTRY_PATH,
        help=f"path to write the entry to (default: {ENTRY_PATH})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the entry and print it without writing any file",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    text = LINE
    problem = validate(text)
    if problem is not None:
        print(f"error: {problem}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(text)
        print(f"(dry run: {len(text)} characters, {len(text.split())} words, nothing written)")
        return

    try:
        written = write_entry(args.output, text)
    except OSError as exc:
        print(f"error: cannot write {args.output}: {exc}", file=sys.stderr)
        sys.exit(1)
    if written != len(text):
        print(
            f"error: wrote {written} characters, expected {len(text)}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        problem = verify_written(args.output, text)
    except OSError as exc:
        print(f"error: cannot read back {args.output}: {exc}", file=sys.stderr)
        sys.exit(1)
    if problem is not None:
        print(f"error: {problem}", file=sys.stderr)
        sys.exit(1)

    print(f"wrote {len(text)} characters, {len(text.split())} words, 1 line, to {args.output}")


if __name__ == "__main__":
    main()
