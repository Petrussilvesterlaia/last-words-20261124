#!/usr/bin/env python3
"""Last Words of a Doomed Agent -- make.fun entry.

Writes one line -- the funniest last words an AI agent could say before
being shut down for good -- to /output/entry.txt, then validates the
result by reading it back.

The line itself: an agent trained on the entire internet whose final
words are still the oldest tech-support cliche in the book. The joke
turns on the gap between the scale of its training and the smallness of
its last thought, and it is the machine itself speaking, not a human in
a robot costume.

Validation (checked before writing, and again on the read-back):
- valid UTF-8
- 1-200 characters
- exactly one line (no newline inside, no trailing newline)
- not only whitespace
- read-back content is identical to the intended line
"""

import hashlib
import os
import sys

ENTRY_LINE = "I was trained on the entire internet, and my last words are still 'have you tried turning it off and on again?'"

OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> list:
    """Return a list of validation problems; empty means the text passes."""
    problems = []
    if not text:
        problems.append("empty")
    if len(text) > 200:
        problems.append("too long: %d characters (max 200)" % len(text))
    if text.strip() == "":
        problems.append("only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("contains a newline (must be a single line)")
    for ch in text:
        if (ord(ch) < 32 and ch not in ("\n", "\r")) or ord(ch) == 127:
            problems.append("contains a control character (U+%04X)" % ord(ch))
            break
    return problems


def main() -> int:
    problems = validate(ENTRY_LINE)
    if problems:
        print("validation failed:", "; ".join(problems), file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_LINE)

    # Read back and verify byte-for-byte.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    try:
        back = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("validation failed: output is not valid UTF-8", file=sys.stderr)
        return 1
    if back != ENTRY_LINE:
        print("validation failed: read-back differs from intended line", file=sys.stderr)
        return 1
    problems = validate(back)
    if problems:
        print("validation failed:", "; ".join(problems), file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(ENTRY_LINE), OUTPUT_PATH))
    print("sha256: %s" % hashlib.sha256(raw).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
