import itertools
import random
import reprlib
from collections.abc import Iterable, Iterator
from enum import Flag, auto
from functools import partialmethod
from typing import Any, TypeAlias

Tile: TypeAlias = int


class Direction(Flag):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


class Board:
    def __init__(self, size: tuple[int, int] = (4, 4)) -> None:
        height, width = size
        self._grid = [[0] * width for _ in range(height)]

        for _ in range(2):
            self._spawn_random_tile()

    @property
    def size(self) -> tuple[int, int]:
        return len(self._grid), len(self._grid[0])

    @classmethod
    def from_iterables_of_ints(cls, grid: Iterable[Iterable[int]]) -> "Board":
        board = cls()
        board._grid = [[tile for tile in row] for row in grid]
        return board

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name} < {reprlib.repr(self._grid)} >"

    def __str__(self) -> str:
        widest_tile = len(str(max(self._flatten())))
        empty_spot = "."

        def format_tile(tile: Tile) -> str:
            return str(tile or empty_spot).center(widest_tile)

        def format_row(row: list[Tile]) -> str:
            return " ".join(map(format_tile, row))

        return "\n".join(map(format_row, self._grid))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return self._grid == other._grid

    def has_legal_moves(self) -> bool:
        return self._has_empty_spots() or self._has_adjacent_equal_tiles()

    def _move(self, direction: Direction) -> None:
        if not self.has_legal_moves():
            return
        self._tiles_moved = False
        self._move_grid(direction)
        if self._tiles_moved:
            self._spawn_random_tile()

    move_left = partialmethod(_move, Direction.LEFT)
    move_right = partialmethod(_move, Direction.RIGHT)
    move_up = partialmethod(_move, Direction.UP)
    move_down = partialmethod(_move, Direction.DOWN)

    def _move_grid(self, direction: Direction) -> None:
        if direction in Direction.UP | Direction.DOWN:
            self._grid = list(self._transpose())

        for row in self._grid:
            if direction in Direction.RIGHT | Direction.DOWN:
                row.reverse()

            self._move_row_left(row)

            if direction in Direction.RIGHT | Direction.DOWN:
                row.reverse()

        if direction in Direction.UP | Direction.DOWN:
            self._grid = list(self._transpose())

    def _move_row_left(self, row: list[Tile]) -> None:
        slow, fast = 0, 1  # two pointers moving from left to right
        while fast < len(row):
            t1, t2 = row[slow], row[fast]
            if t1 and t2:  # find two non-empty tiles
                if t1 == t2:  # merge two equal tiles
                    merged_value = t1 * 2
                    row[slow] = merged_value
                    row[fast] = 0
                    self._tiles_moved = True
                slow += 1
                fast = slow
            elif t2:  # empty spot on the left, move the right tile there
                row[slow] = t2
                row[fast] = 0
                self._tiles_moved = True
            fast += 1

    def _spawn_random_tile(self) -> None:
        if empty_spots := self._get_empty_spots():
            x, y = random.choice(empty_spots)
            self._grid[x][y] = self._make_tile()

    def _get_empty_spots(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for x, row in enumerate(self._grid)
            for y, tile in enumerate(row)
            if not tile
        ]

    def _make_tile(self) -> Tile:
        chance_to_get_4 = 0.1
        return 2 if random.random() > chance_to_get_4 else 4

    def _has_empty_spots(self) -> bool:
        return not all(self._flatten())

    def _has_adjacent_equal_tiles(self) -> bool:
        rows = iter(self._grid)
        columns = self._transpose()
        return any(
            t1 == t2
            for tiles in itertools.chain(rows, columns)
            for t1, t2 in itertools.pairwise(tiles)
        )

    def _flatten(self) -> Iterator[Tile]:
        return itertools.chain.from_iterable(self._grid)

    def _transpose(self) -> Iterator[list[Tile]]:
        return map(list, zip(*self._grid))
