document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const stopBtn = document.getElementById('stop-btn');
    const form = document.getElementById('entry-form');
    const entriesUl = document.getElementById('entries-ul');
    const exportJsonBtn = document.getElementById('export-json-btn');
    const exportCsvBtn = document.getElementById('export-csv-btn');
    const clearBtn = document.getElementById('clear-btn');
    const timerDisplay = document.getElementById('timer-display');

    let timerInterval = null;
    let startTime = null;
    let isRunning = false;

    chrome.storage.local.get(['timerState', 'entries'], (data) => {
        if (data.timerState) {
            startTime = data.timerState.startTime;
            isRunning = data.timerState.isRunning;
            if (isRunning) {
                startBtn.disabled = true;
                pauseBtn.disabled = false;
                updateTimerDisplay();
                timerInterval = setInterval(updateTimerDisplay, 1000);
            } else {
                startBtn.disabled = false;
                pauseBtn.disabled = true;
            }
        }
        if (data.entries) {
            renderEntries(data.entries);
        }
    });

    function updateTimerDisplay() {
        if (!startTime) return;
        const elapsed = Date.now() - startTime;
        const hours = Math.floor(elapsed / 3600000);
        const minutes = Math.floor((elapsed % 3600000) / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        timerDisplay.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    startBtn.addEventListener('click', () => {
        if (isRunning) return;
        startTime = Date.now();
        isRunning = true;
        timerInterval = setInterval(updateTimerDisplay, 1000);
        chrome.storage.local.set({ timerState: { startTime, isRunning: true } });
        startBtn.disabled = true;
        pauseBtn.disabled = false;
    });

    pauseBtn.addEventListener('click', () => {
        if (!isRunning) return;
        isRunning = false;
        clearInterval(timerInterval);
        chrome.storage.local.set({ timerState: { startTime, isRunning: false } });
        startBtn.disabled = false;
        pauseBtn.disabled = true;
    });

    stopBtn.addEventListener('click', () => {
        if (!isRunning) return;
        const duration = Date.now() - startTime;
        const entry = {
            id: Date.now(),
            project: 'Timer',
            date: new Date().toISOString().split('T')[0],
            startTime: new Date(startTime).toISOString(),
            endTime: new Date().toISOString(),
            duration: duration / 3600000,
            notes: ''
        };
        chrome.storage.local.get(['entries'], (data) => {
            const entries = data.entries || [];
            entries.unshift(entry);
            chrome.storage.local.set({ entries, timerState: { startTime: null, isRunning: false } });
            renderEntries(entries);
            timerDisplay.textContent = '00:00:00';
            startBtn.disabled = false;
            pauseBtn.disabled = true;
            isRunning = false;
        });
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const projectName = document.getElementById('project-name').value;
        const date = document.getElementById('entry-date').value;
        const hours = parseFloat(document.getElementById('duration-hours').value) || 0;
        const minutes = parseFloat(document.getElementById('duration-minutes').value) || 0;
        const notes = document.getElementById('notes').value;
        const duration = hours + minutes / 60;

        const entry = {
            id: Date.now(),
            project: projectName,
            date: date,
            startTime: new Date(date).toISOString(),
            endTime: new Date(new Date(date).getTime() + duration * 3600000).toISOString(),
            duration: duration,
            notes: notes
        };

        chrome.storage.local.get(['entries'], (data) => {
            const entries = data.entries || [];
            entries.unshift(entry);
            chrome.storage.local.set({ entries });
            renderEntries(entries);
            form.reset();
        });
    });

    function renderEntries(entries) {
        entriesUl.innerHTML = '';
        entries.forEach(entry => {
            const li = document.createElement('li');
            li.textContent = `${entry.project} (${entry.duration}h) - ${entry.date}`;
            entriesUl.appendChild(li);
        });
    }

    exportJsonBtn.addEventListener('click', () => {
        chrome.storage.local.get(['entries'], (data) => {
            if (!data.entries) return;
            const blob = new Blob([JSON.stringify(data.entries, null, 2)], { type: 'application/json' });
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
            if (!data.entries) return;
            const csv = data.entries.map(e => `${e.project},${e.date},${e.duration},${e.notes}`).join('\n');
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'localtrack_entries.csv';
            a.click();
            URL.revokeObjectURL(url);
        });
    });

    clearBtn.addEventListener('click', () => {
        chrome.storage.local.set({ entries: [], timerState: { startTime: null, isRunning: false } });
        renderEntries([]);
        timerDisplay.textContent = '00:00:00';
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        isRunning = false;
    });
});