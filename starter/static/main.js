// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let hintsUsed = 0;
let elapsedSeconds = 0;
let timerInterval = null;
let scoreSubmitted = false;
let currentGameId = '';
const DARK_MODE_KEY = 'sudoku_dark_mode';

function applyDarkMode(enabled) {
  const body = document.body;
  if (enabled) body.classList.add('dark-theme');
  else body.classList.remove('dark-theme');
}

function toggleDarkMode() {
  const cur = localStorage.getItem(DARK_MODE_KEY) === '1';
  const next = !cur;
  localStorage.setItem(DARK_MODE_KEY, next ? '1' : '0');
  applyDarkMode(next);
}

function initDarkModeFromStorage() {
  const enabled = localStorage.getItem(DARK_MODE_KEY) === '1';
  applyDarkMode(enabled);
  const chk = document.getElementById('dark-mode-toggle');
  if (chk) chk.checked = enabled;
}

function formatTime(seconds) {
  const mm = String(Math.floor(seconds / 60)).padStart(2, '0');
  const ss = String(seconds % 60).padStart(2, '0');
  return `${mm}:${ss}`;
}

function updateTimerDisplay() {
  const el = document.getElementById('timer');
  if (el) el.innerText = formatTime(elapsedSeconds);
}

function getDifficultyLabel() {
  const diffEl = document.getElementById('difficulty');
  const val = diffEl ? diffEl.value : '35';
  if (val === '45') return 'Easy';
  if (val === '30') return 'Hard';
  return 'Medium';
}

function computeGameId() {
  // simple string representation of puzzle + difficulty
  try {
    return puzzle.flat().join(',') + '|' + (document.getElementById('difficulty')?.value || '35');
  } catch (e) {
    return String(Date.now());
  }
}

function loadLeaderboard() {
  try {
    const raw = localStorage.getItem('sudoku_leaderboard') || '[]';
    return JSON.parse(raw);
  } catch (e) {
    return [];
  }
}

function saveLeaderboard(list) {
  localStorage.setItem('sudoku_leaderboard', JSON.stringify(list));
}

function renderLeaderboard() {
  const container = document.getElementById('leaderboard');
  if (!container) return;
  const lb = loadLeaderboard();
  if (lb.length === 0) {
    container.innerHTML = '<p>No scores yet.</p>';
    return;
  }
  let html = '<table><thead><tr><th>Rank</th><th>Time</th><th>Difficulty</th></tr></thead><tbody>';
  for (let i = 0; i < lb.length; i++) {
    const e = lb[i];
    html += `<tr><td>${i+1}</td><td>${formatTime(e.time)}</td><td>${e.difficulty}</td></tr>`;
  }
  html += '</tbody></table>';
  container.innerHTML = html;
}

function addScore(timeSeconds, difficultyLabel) {
  const gameId = currentGameId || computeGameId();
  const last = localStorage.getItem('sudoku_last_submitted_game');
  if (last === gameId) return false; // prevent duplicate submission for same game
  let lb = loadLeaderboard();
  lb.push({time: timeSeconds, difficulty: difficultyLabel, gameId});
  lb.sort((a, b) => a.time - b.time);
  // keep first occurrence per gameId
  const seen = new Set();
  const unique = [];
  for (const e of lb) {
    if (!seen.has(e.gameId)) {
      unique.push(e);
      seen.add(e.gameId);
    }
  }
  lb = unique.slice(0, 10);
  saveLeaderboard(lb);
  localStorage.setItem('sudoku_last_submitted_game', gameId);
  scoreSubmitted = true;
  renderLeaderboard();
  return true;
}

function startTimer() {
  if (timerInterval) return;
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function resetTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.className = 'sudoku-cell';
      }
    }
  }
}

async function newGame() {
  const diffEl = document.getElementById('difficulty');
  const clues = diffEl ? parseInt(diffEl.value, 10) : 35;
  const res = await fetch(`/new?clues=${clues}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  // reset client-side hint count display (server also resets)
  hintsUsed = 0;
  const hc = document.getElementById('hint-count');
  if (hc) hc.innerText = `Hints: ${hintsUsed}`;
  // reset and start timer when a new game is loaded
  resetTimer();
  startTimer();
  // reset leaderboard submission state for the new game
  scoreSubmitted = false;
  currentGameId = computeGameId();
  // render leaderboard (in case persisted scores exist)
  renderLeaderboard();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    // stop timer and show final time
    stopTimer();
    msg.style.color = '#388e3c';
    msg.innerText = `Congratulations! You solved it! Time: ${formatTime(elapsedSeconds)}`;
    // submit score if not already submitted for this game
    const diffLabel = getDifficultyLabel();
    // ensure we don't add a score when incorrect or duplicate
    if (!scoreSubmitted) {
      const added = addScore(elapsedSeconds, diffLabel);
      if (added) {
        // optionally show a small confirmation
        console.log('Score added to leaderboard');
      }
    }
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

async function requestHint() {
  const res = await fetch('/hint', {method: 'POST'});
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const {row, col, value, hints_used} = data;
  hintsUsed = hints_used;
  document.getElementById('hint-count').innerText = `Hints: ${hintsUsed}`;
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const idx = row * SIZE + col;
  const inp = inputs[idx];
  inp.value = value;
  inp.disabled = true;
  inp.className = 'sudoku-cell hinted';
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  const hintBtn = document.getElementById('hint-button');
  if (hintBtn) hintBtn.addEventListener('click', requestHint);
  const darkToggle = document.getElementById('dark-mode-toggle');
  if (darkToggle) darkToggle.addEventListener('change', toggleDarkMode);
  initDarkModeFromStorage();
  // initialize using selected difficulty
  renderLeaderboard();
  newGame();
});