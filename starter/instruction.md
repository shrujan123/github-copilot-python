# Copilot Instructions — Sudoku Project

## Project Goal

This project is a Flask-based Sudoku game that refactors a legacy Sudoku application into a modern, maintainable and user-friendly application.

## Coding Standards

- Use clear, readable and maintainable Python, HTML, CSS and JavaScript.
- Keep functionality modular and avoid unnecessary duplication.
- Preserve existing working functionality when adding new features.
- Use meaningful variable and function names.
- Add comments only where they improve understanding.
- Handle errors gracefully.
- Prefer simple solutions over unnecessary complexity.

## Sudoku Requirements

- Every generated puzzle must have exactly one unique solution.
- Support Easy, Medium and Hard difficulties.
- Prefilled cells must remain locked.
- Hints must fill one correct cell and lock it.
- Check must provide immediate feedback for incorrect entries.
- Successfully completed puzzles must display a completion message.
- The timer must track the current game.
- Completed games must update the Top 10 leaderboard.

## UI Requirements

- Support light and dark modes.
- Use responsive layouts for desktop and mobile.
- Make the interface readable and accessible.
- Use alternating visual styling for the 3x3 Sudoku blocks.
- Keep controls consistent and easy to understand.

## Testing

- Do not remove existing tests when adding features.
- Add tests for important new functionality.
- Run the complete pytest suite after significant changes.
- Do not accept Copilot suggestions blindly.
- Review generated code before accepting it.
- Reject or modify suggestions that do not satisfy the project requirements.

## Git

- Make focused commits describing the changes.
- Do not commit virtual environments, __pycache__, or other generated files.