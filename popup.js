document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get(['timerState', 'entries'], (data) => {
    updateUI(data.timerState || { isRunning: false, startTime: null, pausedTime: 0, elapsed: 0 }, data.entries || []);
  });

  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'local' && changes.timerState) {
      updateUI(changes.timerState.newValue, null);
    }
  });

  document.getElementById('start').onclick = () => chrome.runtime.sendMessage({ type: 'START' });
  document.getElementById('pause').onclick = () => chrome.runtime.sendMessage({ type: 'PAUSE' });
  document.getElementById('resume').onclick = () => chrome.runtime.sendMessage({ type: 'RESUME' });
  document.getElementById('stop').onclick = () => chrome.runtime.sendMessage({ type: 'STOP' });

  document.getElementById('manual-entry').onsubmit = (e) => {
    e.preventDefault();
    const project = document.getElementById('project').value;
    const date = document.getElementById('date').value;
    const hours = parseFloat(document.getElementById('hours').value) || 0;
    const minutes = parseFloat(document.getElementById('minutes').value) || 0;
    const notes = document.getElementById('notes').value;
    const duration = (hours * 60 + minutes) * 1000;

    const entry = { id: Date.now(), project, date, startTime: 0, endTime: 0, duration, notes };
    chrome.storage.local.get('entries', (data) => {
      const entries = data.entries || [];
      entries.push(entry);
      chrome.storage.local.set({ entries });
    });
    e.target.reset();
  };

  document.getElementById('export-json').onclick = () => exportJSON();
  document.getElementById('export-csv').onclick = () => exportCSV();
  document.getElementById('clear').onclick = () => clearStorage();
});

function updateUI(state, entries) {
  const display = document.getElementById('timer-display');
  const totalSpan = document.getElementById('today-total');
  if (state) {
    const elapsed = state.isRunning ? Date.now() - state.startTime - state.pausedTime : state.elapsed;
    display.textContent = formatTime(elapsed);
  }
  if (entries) {
    const list = document.getElementById('entries-list');
    list.innerHTML = entries.slice(-5).map(e => `<div>${e.project} - ${formatTime(e.duration)}</div>`).join('');
  }
}

function formatTime(ms) {
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function exportJSON() {
  chrome.storage.local.get('entries', (data) => {
    const blob = new Blob([JSON.stringify(data.entries, null, 2)]);
    download(blob, 'localtrack.json');
  });
}

function exportCSV() {
  chrome.storage.local.get('entries', (data) => {
    const headers = ['Project', 'Date', 'Duration (ms)', 'Notes'];
    const rows = data.entries.map(e => [e.project, e.date, e.duration, e.notes]);
    const csv = [headers, ...rows].map(r => r.join(',')).join('\n');
    const blob = new Blob([csv]);
    download(blob, 'localtrack.csv');
  });
}

function download(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function clearStorage() {
  chrome.storage.local.clear();
  location.reload();
}
