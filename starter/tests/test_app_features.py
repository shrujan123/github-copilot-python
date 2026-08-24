import random

from app import app, CURRENT
import sudoku_logic


def setup_module(module):
    random.seed(0)
    app.testing = True


def make_solved_board():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(board)
    return board


def test_check_endpoint_marks_incorrect_only():
    solution = make_solved_board()
    puzzle = sudoku_logic.deep_copy(solution)
    # make one cell empty for user to fill
    puzzle[0][0] = sudoku_logic.EMPTY

    CURRENT['puzzle'] = sudoku_logic.deep_copy(puzzle)
    CURRENT['solution'] = sudoku_logic.deep_copy(solution)
    CURRENT['hints_used'] = 0

    # user fills the empty cell with an incorrect value
    board = sudoku_logic.deep_copy(puzzle)
    wrong = (solution[0][0] % 9) + 1
    if wrong == solution[0][0]:
        wrong = (wrong % 9) + 1
    board[0][0] = wrong

    client = app.test_client()
    resp = client.post('/check', json={'board': board})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'incorrect' in data
    assert [0, 0] in data['incorrect']
    # ensure a known correct prefilled cell is not marked incorrect
    # find a prefilled cell
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if puzzle[i][j] != sudoku_logic.EMPTY:
                assert [i, j] not in data['incorrect']
                break
        else:
            continue
        break


def test_hint_fills_cell_and_increments_count():
    solution = make_solved_board()
    puzzle = sudoku_logic.deep_copy(solution)
    # make two empties
    puzzle[0][0] = sudoku_logic.EMPTY
    puzzle[1][1] = sudoku_logic.EMPTY

    CURRENT['puzzle'] = sudoku_logic.deep_copy(puzzle)
    CURRENT['solution'] = sudoku_logic.deep_copy(solution)
    CURRENT['hints_used'] = 0

    client = app.test_client()
    resp = client.post('/hint')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'row' in data and 'col' in data and 'value' in data
    r, c, v = data['row'], data['col'], data['value']
    assert CURRENT['puzzle'][r][c] == CURRENT['solution'][r][c]
    assert CURRENT['hints_used'] == 1


def test_new_resets_hints():
    # set hints used
    CURRENT['hints_used'] = 3
    client = app.test_client()
    resp = client.get('/new?clues=45')
    assert resp.status_code == 200
    assert CURRENT.get('hints_used', 0) == 0
