import os


def test_index_has_dark_toggle():
    path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'id="dark-mode-toggle"' in content


def test_main_js_has_dark_functions_and_key():
    path = os.path.join(os.path.dirname(__file__), '..', 'static', 'main.js')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'DARK_MODE_KEY' in content
    assert 'function toggleDarkMode' in content
    assert 'function applyDarkMode' in content
    assert 'initDarkModeFromStorage' in content


def test_styles_contains_dark_theme_rule():
    path = os.path.join(os.path.dirname(__file__), '..', 'static', 'styles.css')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '.dark-theme' in content
    assert '--bg' in content
