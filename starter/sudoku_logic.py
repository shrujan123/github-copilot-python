import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def count_solutions(board, limit=2):
    """Count valid Sudoku solutions up to a given limit."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                solution_count = 0
                for num in range(1, SIZE + 1):
                    if is_safe(board, row, col, num):
                        board[row][col] = num
                        solution_count += count_solutions(board, limit - solution_count)
                        board[row][col] = EMPTY
                        if solution_count >= limit:
                            return solution_count
                return solution_count
    return 1


def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1


def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)

    puzzle = deep_copy(solution)
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    removed = 0

    for row, col in cells:
        if SIZE * SIZE - removed <= clues:
            break

        original = puzzle[row][col]
        puzzle[row][col] = EMPTY
        if count_solutions(puzzle) != 1:
            puzzle[row][col] = original
        else:
            removed += 1

    if sum(1 for row in puzzle for cell in row if cell != EMPTY) != clues:
        raise ValueError(f"Could not generate a unique puzzle with {clues} clues")

    return puzzle, solution
