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

After writing, main() reads the file back and re-checks it: the file must
exist, be non-empty, hold exactly one line, and match the validated text
byte for byte. That read-back closes the loop between what validate()
approved and what actually landed on disk, so a truncated write or a
stale file from an earlier run cannot slip through unnoticed. If any
check fails the run exits with an error and the bad file stays visible
for debugging instead of being silently treated as a good entry.

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

# Entry length gates in characters (competition rule: 1-200 chars).
MIN_CHARS = 1
MAX_CHARS = 200


def validate(text: str) -> None:
    """Check the excuse is one printable line and fits the 1-200 char gate."""
    line = text.rstrip("\n")
    if not line.strip():
        raise ValueError("entry is empty or only white space")
    if len(line) < MIN_CHARS:
        raise ValueError(
            f"entry is {len(line)} chars, below the {MIN_CHARS}-char floor"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("entry contains control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} chars, over the {MAX_CHARS}-char gate"
        )


def verify_output(path: str, expected: str) -> None:
    """Read the written file back and confirm it holds exactly the entry.

    Guards against a truncated write or a stale file: the file must exist,
    be non-empty, contain a single line, and match the validated text.
    """
    if not os.path.isfile(path):
        raise ValueError(f"output file missing after write: {path}")
    if os.path.getsize(path) == 0:
        raise ValueError(f"output file is empty: {path}")
    with open(path, "r", encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if "\n" in written or "\r" in written:
        raise ValueError("output file holds more than one line")
    if written != expected:
        raise ValueError("output file does not match the validated entry")


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
    verify_output(path, EXCUSE)


if __name__ == "__main__":
    main()
