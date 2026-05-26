// Background service worker for persistent timer state
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'getTimerState') {
    chrome.storage.local.get('timerState', (data) => {
      sendResponse(data.timerState);
    });
  }
});