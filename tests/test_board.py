import pytest

from py_2048 import Board


def test_board_moves_left_according_to_the_rules(monkeypatch):
    sut = Board.from_iterables_of_ints(
        [
            [2, 2, 2, 2],
            [0, 2, 4, 4],
            [0, 2, 4, 2],
            [2, 0, 2, 4],
        ]
    )
    result = Board.from_iterables_of_ints(
        [
            [4, 4, 0, 0],
            [2, 8, 0, 0],
            [2, 4, 2, 0],
            [4, 4, 0, 0],
        ]
    )
    # disable tile spawn
    monkeypatch.setattr(sut, "_spawn_random_tile", lambda: None)

    sut.move_left()

    assert sut == result


def test_board_has_no_more_moves():
    sut = Board.from_iterables_of_ints(
        [
            [2, 4, 2, 4],
            [4, 8, 4, 8],
            [2, 4, 2, 4],
            [4, 8, 4, 8],
        ]
    )
    assert sut.has_legal_moves() is False


@pytest.mark.parametrize(
    "grid",
    [
        # empty spot
        [
            [2, 4, 2, 4],
            [4, 8, 4, 8],
            [2, 0, 2, 4],
            [4, 8, 4, 8],
        ],
        # equal tiles in row
        [
            [2, 4, 2, 4],
            [4, 8, 4, 8],
            [2, 2, 2, 4],
            [4, 8, 4, 8],
        ],
        # equal tiles in column
        [
            [2, 4, 2, 4],
            [4, 8, 4, 8],
            [2, 8, 2, 4],
            [4, 8, 4, 8],
        ],
    ],
)
def test_board_has_yet_another_move(grid):
    sut = Board.from_iterables_of_ints(grid)
    assert sut.has_legal_moves() is True
