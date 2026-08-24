import io
import os


def test_index_contains_timer():
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'id="timer"' in content


def test_main_js_has_timer_functions():
    path = os.path.join(os.path.dirname(__file__), '..', 'static', 'main.js')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # check for function names and that newGame wires up reset/start
    assert 'function startTimer' in content
    assert 'function stopTimer' in content
    assert 'function resetTimer' in content
    assert 'resetTimer();' in content
    assert 'startTimer();' in content
