import os


def test_index_contains_leaderboard():
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'id="leaderboard"' in content


def test_main_js_has_leaderboard_functions_and_keys():
    path = os.path.join(os.path.dirname(__file__), '..', 'static', 'main.js')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'function loadLeaderboard' in content
    assert 'function saveLeaderboard' in content
    assert 'function renderLeaderboard' in content
    assert 'function addScore' in content
    assert "sudoku_leaderboard" in content
    assert "sudoku_last_submitted_game" in content
    assert "window.prompt" in content
    assert "name, time: timeSeconds" in content
    assert "hints: hintCount" in content
    assert '<th>Player</th>' in content
    assert '<th>Hints Used</th>' in content
    assert '.slice(0, 10)' in content
    # ensure newGame resets submission state
    assert 'scoreSubmitted = false' in content or 'scoreSubmitted=false' in content
