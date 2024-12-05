import textwrap
import typing

import pytest

from better_diff import unified_plus


class _UnitDiffCase(typing.NamedTuple):
    a: str
    b: str
    expected: str


@pytest.mark.parametrize(
    ["a", "b", "expected"],
    [
        pytest.param(*_UnitDiffCase(a="a\nb\n", b="a\nb\n", expected=""), id="no diff"),
        pytest.param(
            *_UnitDiffCase(
                a="a\n1234\n",
                b="a\n456\n",
                expected="--- a\n+++ b\n@@ -1,2 +1,2 @@\n a\n-1234\n+456\n",
            ),
            id="line-subst",
        ),
        pytest.param(
            *_UnitDiffCase(
                a="a\na string with trailing whitespace  \n",
                b="a\na string with trailing whitespace\n",
                expected=textwrap.dedent(
                    """\
                --- a
                +++ b
                @@ -1,2 +1,2 @@
                 a
                -a string with trailing whitespace
                ?                                 ^^
                +a string with trailing whitespace
                """
                ),
            ),
            id="trailing-whitespace",
        ),
        pytest.param(
            *_UnitDiffCase(
                a=textwrap.dedent(
                    """\
                a long string
                that spans multiple lines
                and has trailing whitespace at the end  """
                ),
                b=textwrap.dedent(
                    """\
                a long string
                that spans multiple lines
                and has trailing whitespace at the end"""
                ),
                expected="--- a\n+++ b\n@@ -1,3 +1,3 @@\n a long string\n that spans multiple lines\n-and has trailing whitespace at the end\n?                                      ^^\n+and has trailing whitespace at the end\n\\ No newline at end of file (a)\n\\ No newline at end of file (b)\n",
            ),
            id="trailing-whitespace-at-end",
        ),
        pytest.param(
            *_UnitDiffCase(
                a=textwrap.dedent(
                    """\
                a long string
                that spans multiple lines
                and ends with a newline
                """
                ),
                b=textwrap.dedent(
                    """\
                a long string
                that spans multiple lines
                and ends with a newline"""
                ),
                expected="\\ No newline at end of file (b)\n",
            ),
            id="no-trailing-newline",
        ),
    ],
)
def test_unified_plus_format(a, b, expected):
    assert unified_plus.format_diff(a, b) == expected
