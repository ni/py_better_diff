import typing


class _UnitDiffCase(typing.NamedTuple):
    a: str
    b: str
    expected: str


class _OutputDiffCase(typing.NamedTuple):
    a: str
    b: str
