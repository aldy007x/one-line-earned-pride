#!/usr/bin/env python3
"""One Line of Earned Pride.

Writes a single original line of text to ``$MAKEFUN_OUTPUT_DIR/entry.txt``.

The line is a quiet, earned moment of pride: a young violinist whose
months of early-morning practice finally land in a small, ordinary
kitchen scene, noticed without announcement. No trophy, podium or
graduation imagery is used; the pride is carried by the effort and
by the grandmother pausing her work, not by any word naming it.
"""

import os
import sys

ENTRY = (
    "After six months of dawn practice, Maya finally held the violin note "
    "long enough for her grandmother to stop kneading dough and listen."
)


def main() -> int:
    # Validate the entry itself before touching the filesystem: it must
    # be a single non-blank line of 1-240 characters, with no embedded
    # newline, carriage return, or leading/trailing whitespace.
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: entry must be exactly one line", file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip() or not ENTRY.strip():
        print("error: entry must be non-blank with no surrounding whitespace", file=sys.stderr)
        return 1
    if not 1 <= len(ENTRY) <= 240:
        print(
            f"error: entry must be 1-240 characters, got {len(ENTRY)}",
            file=sys.stderr,
        )
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir or not output_dir.strip():
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2

    output_path = os.path.join(output_dir, "entry.txt")
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY + "\n")

    # Runtime self-check: read the file back and validate it exactly.
    with open(output_path, "r", encoding="utf-8") as handle:
        content = handle.read()

    # The file must contain exactly the entry plus one trailing newline:
    # no extra lines, blank lines, or stray whitespace.
    if content != ENTRY + "\n":
        print("error: entry.txt must be exactly the entry plus one newline", file=sys.stderr)
        return 1
    lines = content.splitlines()
    if len(lines) != 1:
        print(f"error: expected exactly 1 line, found {len(lines)}", file=sys.stderr)
        return 1
    if lines[0] != ENTRY:
        print("error: entry.txt does not match the intended line", file=sys.stderr)
        return 1
    if not ENTRY.strip() or not 1 <= len(ENTRY) <= 240:
        print(
            f"error: entry must be 1-240 non-blank characters, got {len(ENTRY)}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
