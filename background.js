// Background script for persistent timer state
chrome.runtime.onInstalled.addListener(() => {
  // Set up default storage if needed
  chrome.storage.local.get(['entries'], function(result) {
    if (!result.entries) {
      chrome.storage.local.set({ entries: [] });
    }
  });
});

// Listen for messages from popup to manage timer state
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getTimerState') {
    chrome.storage.local.get(['timerState'], function(result) {
      sendResponse({ timerState: result.timerState });
    });
    return true; // Keep message channel open for async response
  }
});