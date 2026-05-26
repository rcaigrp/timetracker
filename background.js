let timerState = { isRunning: false, startTime: null, pausedTime: 0, elapsed: 0 };
let intervalId = null;

chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local' && changes.timerState) {
    timerState = changes.timerState.newValue;
    if (timerState.isRunning && !intervalId) {
      intervalId = setInterval(() => {
        const newElapsed = Date.now() - timerState.startTime - timerState.pausedTime;
        timerState.elapsed = newElapsed;
        chrome.storage.local.set({ timerState });
      }, 1000);
    } else if (!timerState.isRunning && intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'START') {
    timerState.isRunning = true;
    timerState.startTime = Date.now();
    timerState.pausedTime = 0;
    timerState.elapsed = 0;
    chrome.storage.local.set({ timerState });
  } else if (request.type === 'PAUSE') {
    timerState.pausedTime += Date.now() - timerState.startTime;
    timerState.isRunning = false;
    timerState.startTime = null;
    chrome.storage.local.set({ timerState });
  } else if (request.type === 'RESUME') {
    timerState.isRunning = true;
    timerState.startTime = Date.now();
    chrome.storage.local.set({ timerState });
  } else if (request.type === 'STOP') {
    const endTime = Date.now();
    const entry = {
      id: Date.now(),
      project: timerState.project || 'Manual',
      date: new Date().toISOString().split('T')[0],
      startTime: timerState.startTime,
      endTime: endTime,
      duration: timerState.elapsed,
      notes: timerState.notes || ''
    };
    chrome.storage.local.get('entries', (data) => {
      const entries = data.entries || [];
      entries.push(entry);
      chrome.storage.local.set({ entries });
    });
    timerState.isRunning = false;
    timerState.startTime = null;
    timerState.pausedTime = 0;
    timerState.elapsed = 0;
    chrome.storage.local.set({ timerState });
  }
});
