import random

import sudoku_logic


def setup_module(module):
    # Seed randomness for deterministic tests
    random.seed(0)


def test_create_empty_board():
    board = sudoku_logic.create_empty_board()
    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy():
    b = sudoku_logic.create_empty_board()
    b[0][0] = 5
    c = sudoku_logic.deep_copy(b)
    assert c == b
    b[0][0] = sudoku_logic.EMPTY
    assert c[0][0] == 5


def test_is_safe_and_fill_board():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.is_safe(board, 0, 0, 1)
    board[0][1] = 1
    assert not sudoku_logic.is_safe(board, 0, 0, 1)

    filled = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(filled) is True
    # No empties
    assert all(0 not in row for row in filled)
    # Each row should be a permutation of 1..SIZE
    for row in filled:
        assert set(row) == set(range(1, sudoku_logic.SIZE + 1))


def test_generate_puzzle_and_solution_counts():
    clues = 30
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE

    non_empty = sum(1 for r in puzzle for c in r if c != sudoku_logic.EMPTY)
    assert non_empty == clues

    # Solution should be full (no empties)
    assert all(cell != sudoku_logic.EMPTY for row in solution for cell in row)

    # Puzzle should not equal solution (some cells removed)
    assert puzzle != solution

    # Generated puzzles must have exactly one valid solution.
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_count_solutions_for_complete_board():
    solved = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    assert sudoku_logic.count_solutions(solved) == 1
