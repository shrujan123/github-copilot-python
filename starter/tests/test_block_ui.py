import os


def read_project_file(*parts):
    path = os.path.join(os.path.dirname(__file__), '..', *parts)
    with open(os.path.normpath(path), 'r', encoding='utf-8') as f:
        return f.read()


def test_board_assigns_checkerboard_block_tones():
    content = read_project_file('static', 'main.js')

    assert 'Math.floor(i / 3)' in content
    assert 'Math.floor(j / 3)' in content
    assert "input.dataset.blockTone" in content
    assert "? 'base' : 'alternate'" in content


def test_block_tones_support_themes_and_cell_states():
    content = read_project_file('static', 'styles.css')

    assert content.count('--block-alt-bg:') == 2
    assert '.sudoku-cell[data-block-tone="alternate"]' in content
    assert '.sudoku-cell.prefilled' in content
    assert '.sudoku-cell.incorrect' in content
    assert '.sudoku-cell.hinted' in content