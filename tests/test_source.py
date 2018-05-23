from typing import Callable
from unittest.mock import MagicMock

import pytest
from bugzoo.core.bug import Bug as Snapshot

from boggart.config.operators import Operators as OperatorManager
from boggart.server.sourcefile import SourceFileManager


class MockSourceFileManager(SourceFileManager):
    def __init__(self, src: str) -> None:
        super().__init__(None, None, OperatorManager())
        self.read_file = MagicMock(return_value=src)


class MockSnapshot(object):
    def name(self) -> str:
        return "foo"


def test_line_col_to_offset():
    def build_convert(src: str) -> Callable[[int, int], int]:
        snapshot = MockSnapshot()
        mgr = MockSourceFileManager(src)
        def convert(line: int, col: int) -> int:
            return mgr.line_col_to_offset(snapshot, "foo.c", line, col)
        return convert

    convert = build_convert("""
int sm = 0;
for (int i = 0; i < 10; ++i) {
  sm += i;
}
    """.strip())

    assert convert(1, 0) == 0
    assert convert(1, 11) == 11
    assert convert(2, 0) == 12
    assert convert(2, 5) == 17
