"""One Line, One Laugh — make.fun entry.

Writes a single original funny line (at most 140 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt, where the house gate and judge read it.
"""

import os

LINE = "I asked AI to write my wedding vows. It proposed to my fiancée first — and she said yes."

MAX_CHARS = 140


def validate(line: str) -> bytes:
    """Check the line against the house gate and return its exact bytes.

    Gate: UTF-8 text, 1 to 140 characters, not only whitespace.
    """
    if not line:
        raise ValueError("line is empty")
    if line.strip() == "":
        raise ValueError("line is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the {MAX_CHARS} limit")
    # UTF-8 round-trip: the bytes we write must decode back to the same line.
    data = line.encode("utf-8")
    if data.decode("utf-8") != line:
        raise ValueError("line is not valid UTF-8")
    return data


def render() -> bytes:
    """Render the entry twice and require byte-identical output."""
    first = validate(LINE)
    second = validate(LINE)
    if first != second:
        raise ValueError("repeat runs are not byte-identical")
    return first


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(render())


if __name__ == "__main__":
    main()
