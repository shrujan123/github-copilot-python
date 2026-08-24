import os


def read_project_file(*parts):
    path = os.path.join(os.path.dirname(__file__), '..', *parts)
    with open(os.path.normpath(path), 'r', encoding='utf-8') as f:
        return f.read()


def test_input_validation_provides_immediate_feedback():
    content = read_project_file('static', 'main.js')

    assert "addEventListener('input'" in content
    assert "fetch('/check'" in content
    assert "input.classList.toggle('incorrect'" in content
    assert "if (!value) return;" in content
    assert "if (input.disabled) return;" in content


def test_incorrect_feedback_has_light_and_dark_text_colors():
    content = read_project_file('static', 'styles.css')

    assert content.count('--incorrect-text:') == 2
    assert '.sudoku-cell.incorrect' in content
    assert 'color: var(--incorrect-text);' in content