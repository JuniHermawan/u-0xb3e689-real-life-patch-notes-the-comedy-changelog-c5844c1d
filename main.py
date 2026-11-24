#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog — entry program.

Writes one patch-note line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Python 3.13 standard library only.
Deterministic: the same bytes on every run.

Version history:
- v1: picked line (see NOTES.md calibration) + gate self-check
  (1-160 chars, single line, non-whitespace, UTF-8).
- v2: added trailing-whitespace guard + read-back check that the
  bytes on disk equal the entry exactly (no trailing newline added).
"""

import os

# The entry: calibrated pick c30 — hand rubric 24/25, proxy screen
# 0.883 vs controls, best combined head-to-head mean 0.669/1.0
# (beats c19 0.85/0.80, ties c04 0.50/0.50, beats c18 and c01 on avg).
ENTRY = (
    "v4.0.9: fixed a bug where the brain saved the wifi password "
    "but forgot the birthday of its own mother."
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = ENTRY
    # Gate self-check, mirroring the sealed scorer: UTF-8 text of
    # 1 to 160 characters, not only white space, single line.
    encoded = text.encode("utf-8")
    assert 1 <= len(text) <= 160, f"entry is {len(text)} chars, must be 1-160"
    assert text.strip() != "", "entry must not be only white space"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert encoded.decode("utf-8") == text, "entry must be valid UTF-8"
    assert text == text.strip(), "entry must not start/end with whitespace"
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Read-back gate: the bytes on disk must equal the entry exactly.
    with open(path, "rb") as f:
        assert f.read() == encoded, "entry.txt bytes differ from entry"
    print(f"wrote {len(text)} chars to {path}")


if __name__ == "__main__":
    main()
