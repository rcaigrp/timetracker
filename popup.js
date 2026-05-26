document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('start-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const stopBtn = document.getElementById('stop-btn');
  const timerDisplay = document.getElementById('timer-display');
  const todayTotal = document.getElementById('today-total');
  const entriesList = document.getElementById('entries-list');
  const manualForm = document.getElementById('manual-form');
  const exportJsonBtn = document.getElementById('export-json');
  const exportCsvBtn = document.getElementById('export-csv');

  let timerInterval;
  let isRunning = false;

  // Load timer state
  chrome.storage.local.get(['timerState', 'entries'], (data) => {
    if (data.timerState && data.timerState.status === 'running') {
      startTimer(data.timerState.startTime);
      startBtn.disabled = true;
      pauseBtn.disabled = false;
      stopBtn.disabled = false;
      isRunning = true;
    } else {
      startBtn.disabled = false;
      pauseBtn.disabled = true;
      stopBtn.disabled = true;
      isRunning = false;
    }
    loadEntries(data.entries || []);
    loadSummary(data.entries || []);
  });

  function startTimer(startTime) {
    const update = () => {
      const now = Date.now();
      const elapsed = now - startTime;
      const hours = Math.floor(elapsed / (1000 * 60 * 60));
      const minutes = Math.floor((elapsed % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((elapsed % (1000 * 60)) / 1000);
      timerDisplay.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    };
    update();
    timerInterval = setInterval(update, 1000);
  }

  startBtn.addEventListener('click', () => {
    const startTime = Date.now();
    chrome.storage.local.set({ timerState: { status: 'running', startTime } });
    startTimer(startTime);
    startBtn.disabled = true;
    pauseBtn.disabled = false;
    stopBtn.disabled = false;
    isRunning = true;
  });

  pauseBtn.addEventListener('click', () => {
    clearInterval(timerInterval);
    chrome.storage.local.set({ timerState: { status: 'paused', startTime: null } });
    pauseBtn.disabled = true;
    stopBtn.disabled = true;
    startBtn.disabled = false;
    isRunning = false;
  });

  stopBtn.addEventListener('click', () => {
    clearInterval(timerInterval);
    const endTime = Date.now();
    const startTime = getStoredStartTime();
    const duration = endTime - startTime;
    const entry = {
      id: Date.now(),
      project: 'Timer Entry',
      date: new Date().toISOString().split('T')[0],
      startTime: new Date(startTime).toLocaleTimeString(),
      endTime: new Date(endTime).toLocaleTimeString(),
      duration: duration,
      notes: ''
    };
    chrome.storage.local.get(['entries'], (data) => {
      const entries = data.entries || [];
      entries.unshift(entry);
      chrome.storage.local.set({ entries, timerState: { status: 'stopped' } });
      loadEntries(entries);
      loadSummary(entries);
      startBtn.disabled = false;
      pauseBtn.disabled = true;
      stopBtn.disabled = true;
      isRunning = false;
      timerDisplay.textContent = '00:00:00';
    });
  });

  function getStoredStartTime() {
    return new Promise((resolve) => {
      chrome.storage.local.get('timerState', (data) => {
        resolve(data.timerState.startTime);
      });
    });
  }

  manualForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const projectName = document.getElementById('project-name').value;
    const date = document.getElementById('entry-date').value;
    const durationStr = document.getElementById('duration').value;
    const notes = document.getElementById('notes').value;

    const [hours, minutes] = durationStr.split(':').map(Number);
    if (isNaN(hours) || isNaN(minutes)) {
      alert('Invalid duration format. Use h:mm');
      return;
    }
    const duration = (hours * 60 + minutes) * 60 * 1000;

    const entry = {
      id: Date.now(),
      project: projectName,
      date: date,
      startTime: '',
      endTime: '',
      duration: duration,
      notes: notes
    };

    chrome.storage.local.get(['entries'], (data) => {
      const entries = data.entries || [];
      entries.unshift(entry);
      chrome.storage.local.set({ entries });
      loadEntries(entries);
      loadSummary(entries);
      manualForm.reset();
    });
  });

  exportJsonBtn.addEventListener('click', () => {
    chrome.storage.local.get('entries', (data) => {
      const blob = new Blob([JSON.stringify(data.entries, null, 2)]);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'localtrack_entries.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
  });

  exportCsvBtn.addEventListener('click', () => {
    chrome.storage.local.get('entries', (data) => {
      const entries = data.entries;
      if (!entries || entries.length === 0) {
        alert('No entries to export');
        return;
      }
      const csv = entries.map(e => `${e.id},${e.project},${e.date},${e.duration},${e.notes}`).join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'localtrack_entries.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
  });

  function loadEntries(entries) {
    entriesList.innerHTML = '';
    entries.forEach(entry => {
      const li = document.createElement('li');
      li.textContent = `${entry.project} - ${entry.date} (${(entry.duration / (1000 * 60)).toFixed(1)}m)`;
      entriesList.appendChild(li);
    });
  }

  function loadSummary(entries) {
    const today = new Date().toISOString().split('T')[0];
    const todayEntries = entries.filter(e => e.date === today);
    const totalMs = todayEntries.reduce((sum, e) => sum + e.duration, 0);
    const totalHours = (totalMs / (1000 * 60 * 60)).toFixed(2);
    todayTotal.textContent = `${totalHours} hours`;
  }
});