from flask import Flask, render_template, jsonify, request
import sudoku_logic
import random

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}
CURRENT['hints_used'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    clues = int(request.args.get('clues', 35))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    # reset hints on new game
    CURRENT['hints_used'] = 0
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            # treat empty or wrong values as incorrect; correct entries are not marked
            try:
                val = int(board[i][j])
            except Exception:
                val = 0
            if val != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})


@app.route('/hint', methods=['POST'])
def hint():
    solution = CURRENT.get('solution')
    puzzle = CURRENT.get('puzzle')
    if solution is None or puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400
    empties = [(i, j) for i in range(sudoku_logic.SIZE) for j in range(sudoku_logic.SIZE) if puzzle[i][j] == sudoku_logic.EMPTY]
    if not empties:
        return jsonify({'error': 'No empty cells left'}), 400
    row, col = random.choice(empties)
    val = solution[row][col]
    puzzle[row][col] = val
    CURRENT['hints_used'] = CURRENT.get('hints_used', 0) + 1
    return jsonify({'row': row, 'col': col, 'value': val, 'hints_used': CURRENT['hints_used']})

if __name__ == '__main__':
    app.run(debug=True)