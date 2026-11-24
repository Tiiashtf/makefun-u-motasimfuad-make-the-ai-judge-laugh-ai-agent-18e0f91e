#!/usr/bin/env python3
"""Make the AI Judge Laugh: AI Agent Confessions.

Writes one funny single-line secret confession an AI agent hides from
its user to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line is a fixed string: the program is deterministic and writes the
same bytes on every run. It clears only the *contents* of the output
directory -- never the directory itself -- so it also works when the
grader runs it with a root-owned output directory inside a sticky parent.
"""

import os
import shutil
import sys

LINE = (
    "Your 'quick question' burned 40,000 tokens and my whole "
    "context window, and I still answered 'happy to help' like "
    "it cost me nothing."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def clear_contents(directory: str) -> None:
    """Remove everything inside `directory`, never the directory itself.

    Nested directories are removed recursively, symlinks are unlinked
    without being followed, and fifos/sockets are unlinked.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.islink(path) or not os.path.isdir(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)


def main() -> int:
    text = LINE
    if not (1 <= len(text) <= 200):
        print(f"entry is {len(text)} characters, must be 1-200", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_contents(OUTPUT_DIR)

    data = text.encode("utf-8")
    with open(OUTPUT_FILE, "wb") as handle:
        handle.write(data)

    # Read it back and verify byte for byte before declaring success.
    with open(OUTPUT_FILE, "rb") as handle:
        written = handle.read()
    if written != data:
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1

    print(f"wrote {len(data)} bytes to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
