"""A unified+ format based on the standard difflib.unified_diff."""

import difflib
import typing


def format_diff(a: str, b: str, fromfile: str = "a", tofile: str = "b") -> str:
    """Return a unified+ diff between two strings.

    Args:
        a: The first string to compare.
        b: The second string to compare.
        fromfile: The name of the first file.
        tofile: The name of the second file.
    """
    result = []
    last_line: typing.Optional[str] = None

    normalized_endings_a, normalized_endings_b = (a.rstrip("\r\n"), b.rstrip("\r\n"))
    newline_difference_message = "\n\\ Newline at end of file"

    len_a_difference = len(a) - len(normalized_endings_a)
    len_b_difference = len(b) - len(normalized_endings_b)
    if len_a_difference != len_b_difference:
        normalized_endings_a += newline_difference_message * (len(a) - len(normalized_endings_a))
        normalized_endings_b += newline_difference_message * (len(b) - len(normalized_endings_b))

    for line in difflib.unified_diff(
        a=normalized_endings_a.splitlines(),
        b=normalized_endings_b.splitlines(),
        fromfile=fromfile,
        tofile=tofile,
    ):
        if last_line and line:
            doing_a_substitution = last_line.startswith("-") and line.startswith("+")
            last_line_had_dangling_whitespace = last_line != last_line.rstrip()
            new_line_is_last_line_without_whitespace = last_line[1:].rstrip() == line[1:]
            if all(
                [
                    doing_a_substitution,
                    last_line_had_dangling_whitespace,
                    new_line_is_last_line_without_whitespace,
                ]
            ):
                highlight = "^" * (len(last_line) - len(last_line.rstrip()))
                result.append("?" + " " * (len(line) - 1) + highlight)

        result.append(line.rstrip())
        last_line = line

    if not result:
        return ""
    return "\n".join(result) + "\n"
