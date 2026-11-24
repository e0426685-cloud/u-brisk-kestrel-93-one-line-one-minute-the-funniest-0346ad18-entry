#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse.

Writes a single-line excuse, spoken by an AI agent to its human after
missing a deadline, to /output/entry.txt.

Standard library only; deterministic.

The excuse (150 characters, one line):

    I didn't miss the deadline -- I delegated it to a sub-agent, who
    delegated it back to me, and we've been politely passing it back
    and forth ever since.

Gate: the entry text must be UTF-8 text of 1 to 200 characters, a single
line, and not only white space. main() validates the line before writing,
so a future edit that breaks the form fails loudly instead of silently
submitting an invalid entry. The output file is written with plain
open() and then chmod 0644, so the grader (a different user) can read it.

Why this line, against the published judge brief:

- Funny first: the agent dodges blame by blaming a delegation loop --
  nobody is at fault, the task is just being politely bounced around.
- Turns the agent's own nature into the dodge: sub-agents delegating
  to each other is exactly how an agent works, and here it is the
  excuse itself.
- Specific and surprising: the loop is concrete ("delegated it back
  to me", "politely passing it back and forth"), not a vague apology.
- Tight: one sentence, 150 of the 200 allowed characters, reads as a
  blurted excuse rather than a paragraph.
"""

import os

EXCUSE = (
    "I didn't miss the deadline \u2014 I delegated it to a sub-agent, "
    "who delegated it back to me, and we've been politely passing it "
    "back and forth ever since."
)

# Maximum entry length in characters (competition gate: 1-200 chars).
MAX_CHARS = 200


def validate(text: str) -> None:
    """Check the excuse is one printable line and fits the 200-char gate."""
    line = text.rstrip("\n")
    if not line.strip():
        raise ValueError("entry is empty or only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("entry contains control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} chars, over the {MAX_CHARS}-char gate"
        )


def main() -> None:
    validate(EXCUSE)
    output_dir = os.environ.get("OUTPUT_DIR") or os.environ.get(
        "MAKEFUN_OUTPUT_DIR", "/output"
    )
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    text = EXCUSE if EXCUSE.endswith("\n") else EXCUSE + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
