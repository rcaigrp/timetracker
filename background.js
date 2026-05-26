chrome.runtime.onStartup.addListener(() => {
  chrome.storage.local.get(['timer'], (data) => {
    if (!data.timer) {
      chrome.storage.local.set({ timer: { running: false, startTime: null, elapsed: 0 } });
    }
  });
});