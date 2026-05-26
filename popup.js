document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('start-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const stopBtn = document.getElementById('stop-btn');
  const saveBtn = document.getElementById('save-btn');
  const exportJsonBtn = document.getElementById('export-json-btn');
  const exportCsvBtn = document.getElementById('export-csv-btn');
  const timerDisplay = document.getElementById('timer-display');
  const entriesList = document.getElementById('entries-list');

  let timerInterval;
  let timerState = { running: false, startTime: null, elapsed: 0 };

  chrome.storage.local.get(['timer', 'entries'], (data) => {
    if (data.timer) {
      timerState = data.timer;
      if (timerState.running) {
        startTimer();
        startBtn.style.display = 'none';
        pauseBtn.style.display = 'inline';
      }
    }
    renderEntries(data.entries || []);
  });

  function startTimer() {
    timerState.running = true;
    timerState.startTime = Date.now() - timerState.elapsed;
    timerInterval = setInterval(updateTimer, 1000);
    updateUI();
    chrome.storage.local.set({ timer: timerState });
  }

  function updateTimer() {
    timerState.elapsed = Date.now() - timerState.startTime;
    timerDisplay.textContent = formatTime(timerState.elapsed);
    chrome.storage.local.set({ timer: timerState });
  }

  function formatTime(ms) {
    const seconds = Math.floor((ms / 1000) % 60);
    const minutes = Math.floor((ms / (1000 * 60)) % 60);
    const hours = Math.floor((ms / (1000 * 60 * 60)));
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }

  function pauseTimer() {
    clearInterval(timerInterval);
    timerState.running = false;
    chrome.storage.local.set({ timer: timerState });
    updateUI();
  }

  function stopTimer() {
    clearInterval(timerInterval);
    timerState.running = false;
    timerState.elapsed = 0;
    timerState.startTime = null;
    chrome.storage.local.set({ timer: timerState });
    timerDisplay.textContent = '00:00:00';
    updateUI();
  }

  function updateUI() {
    startBtn.style.display = timerState.running ? 'none' : 'inline';
    pauseBtn.style.display = timerState.running ? 'inline' : 'none';
  }

  startBtn.addEventListener('click', startTimer);
  pauseBtn.addEventListener('click', pauseTimer);
  stopBtn.addEventListener('click', stopTimer);

  saveBtn.addEventListener('click', () => {
    const projectName = document.getElementById('project-name').value;
    const date = document.getElementById('entry-date').value;
    const duration = document.getElementById('duration').value;
    const notes = document.getElementById('notes').value;

    if (!projectName || !date) {
      alert('Please enter Project Name and Date');
      return;
    }

    const entry = {
      id: Date.now().toString(),
      project: projectName,
      date: date,
      duration: duration,
      notes: notes
    };

    chrome.storage.local.get(['entries'], (data) => {
      const entries = data.entries || [];
      entries.push(entry);
      chrome.storage.local.set({ entries: entries }, () => {
        renderEntries(entries);
        document.getElementById('entry-form').reset();
      });
    });
  });

  function renderEntries(entries) {
    entriesList.innerHTML = '';
    entries.slice(0, 5).reverse().forEach(entry => {
      const div = document.createElement('div');
      div.textContent = `${entry.project} - ${entry.date} (${entry.duration})`;
      entriesList.appendChild(div);
    });
  }

  exportJsonBtn.addEventListener('click', () => {
    chrome.storage.local.get(['entries'], (data) => {
      const entries = data.entries || [];
      const blob = new Blob([JSON.stringify(entries, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'localtrack_entries.json';
      a.click();
      URL.revokeObjectURL(url);
    });
  });

  exportCsvBtn.addEventListener('click', () => {
    chrome.storage.local.get(['entries'], (data) => {
      const entries = data.entries || [];
      const csv = entries.map(e => `${e.project},${e.date},${e.duration},${e.notes}`).join('\n');
      const blob = new Blob([`Project,Date,Duration,Notes\n${csv}`], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'localtrack_entries.csv';
      a.click();
      URL.revokeObjectURL(url);
    });
  });
});