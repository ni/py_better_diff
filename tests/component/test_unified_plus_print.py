import pathlib

import pytest
import pytest_snapshot.plugin  # type: ignore[import]

import better_diff

_MODULE_DIR = pathlib.Path(__file__).parent
_TEST_CASES_DIR = _MODULE_DIR / "test_cases"

_TEST_CASES = [
    folder
    for folder in _TEST_CASES_DIR.iterdir()
    if folder.is_dir() and (folder / "a.txt").exists() and (folder / "b.txt").exists()
]


@pytest.mark.parametrize("test_case", _TEST_CASES, ids=lambda o: o.name.replace("_", "-"))
def test___test_case___unified_plus_format___matches_snapshot(
    test_case: pathlib.Path, snapshot: pytest_snapshot.plugin.Snapshot
):
    a = (test_case / "a.txt").read_text()
    b = (test_case / "b.txt").read_text()

    result = better_diff.unified_plus.format_diff(a, b, fromfile="a.txt", tofile="b.txt")

    snapshot.snapshot_dir = test_case
    snapshot.assert_match(result, "expected.diff")
