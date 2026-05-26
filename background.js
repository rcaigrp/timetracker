chrome.storage.local.get(['timerState'], (data) => {
    if (data.timerState) {
        console.log('Timer state restored:', data.timerState);
    }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'updateTimer') {
        chrome.storage.local.set({ timerState: request.state });
        sendResponse({ success: true });
    }
});