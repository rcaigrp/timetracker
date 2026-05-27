// Global variables
let timerInterval = null;
let startTime = null;
let elapsedTime = 0;
let isRunning = false;

// DOM Elements
const timerDisplay = document.getElementById('timerDisplay');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const stopBtn = document.getElementById('stopBtn');
const entryForm = document.getElementById('entryForm');
const summaryDisplay = document.getElementById('summaryDisplay');
const entriesList = document.getElementById('entriesList');
const clearBtn = document.getElementById('clearBtn');
const exportBtn = document.getElementById('exportBtn');

// Initialize the extension
function init() {
  // Set today's date as default for date input
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('entryDate').value = today;
  
  // Load saved data
  loadSavedData();
  
  // Start timer if it was running
  startTimerIfNecessary();
  
  // Event listeners
  startBtn.addEventListener('click', startTimer);
  pauseBtn.addEventListener('click', pauseTimer);
  stopBtn.addEventListener('click', stopTimer);
  entryForm.addEventListener('submit', addManualEntry);
  clearBtn.addEventListener('click', clearAllEntries);
  exportBtn.addEventListener('click', exportData);
}

// Timer functions
function startTimer() {
  if (!isRunning) {
    isRunning = true;
    startTime = Date.now() - elapsedTime;
    timerInterval = setInterval(updateTimer, 1000);
  }
}

function pauseTimer() {
  if (isRunning) {
    isRunning = false;
    clearInterval(timerInterval);
  }
}

function stopTimer() {
  isRunning = false;
  clearInterval(timerInterval);
  elapsedTime = 0;
  updateTimerDisplay(0, 0, 0);
  
  // Save timer state
  chrome.storage.local.set({
    timerState: { isRunning: false, elapsedTime: 0 }
  });
}

function updateTimer() {
  const now = Date.now();
  elapsedTime = now - startTime;
  
  const seconds = Math.floor(elapsedTime / 1000) % 60;
  const minutes = Math.floor(elapsedTime / (1000 * 60)) % 60;
  const hours = Math.floor(elapsedTime / (1000 * 60 * 60));
  
  updateTimerDisplay(hours, minutes, seconds);
}

function updateTimerDisplay(hours, minutes, seconds) {
  timerDisplay.textContent = 
    `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function startTimerIfNecessary() {
  chrome.storage.local.get(['timerState'], function(result) {
    if (result.timerState && result.timerState.isRunning) {
      isRunning = true;
      elapsedTime = result.timerState.elapsedTime || 0;
      startTime = Date.now() - elapsedTime;
      timerInterval = setInterval(updateTimer, 1000);
      updateTimerDisplay(
        Math.floor(elapsedTime / (1000 * 60 * 60)),
        Math.floor(elapsedTime / (1000 * 60)) % 60,
        Math.floor(elapsedTime / 1000) % 60
      );
    }
  });
}

// Manual entry functions
function addManualEntry(e) {
  e.preventDefault();
  
  const project = document.getElementById('projectName').value;
  const date = document.getElementById('entryDate').value;
  const hours = parseInt(document.getElementById('hours').value) || 0;
  const minutes = parseInt(document.getElementById('minutes').value) || 0;
  const notes = document.getElementById('notes').value;
  
  // Validate inputs
  if (!project || !date) {
    alert('Please fill in required fields');
    return;
  }
  
  if (hours < 0 || minutes < 0 || hours > 23 || minutes > 59) {
    alert('Please enter valid time values');
    return;
  }
  
  // Calculate duration in milliseconds
  const durationMs = (hours * 60 + minutes) * 60 * 1000;
  
  // Create entry object
  const entry = {
    id: Date.now(),
    project,
    date,
    startTime: new Date().toISOString(),
    endTime: new Date(Date.now() + durationMs).toISOString(),
    duration: durationMs,
    notes
  };
  
  // Save entry
  saveEntry(entry);
  
  // Reset form
  entryForm.reset();
  document.getElementById('entryDate').value = new Date().toISOString().split('T')[0];
}

function saveEntry(entry) {
  chrome.storage.local.get(['entries'], function(result) {
    const entries = result.entries || [];
    entries.unshift(entry);
    chrome.storage.local.set({ entries }, function() {
      updateUI();
    });
  });
}

// Data management functions
function loadSavedData() {
  chrome.storage.local.get(['entries'], function(result) {
    if (result.entries) {
      updateUI();
    }
  });
}

function updateUI() {
  chrome.storage.local.get(['entries'], function(result) {
    const entries = result.entries || [];
    displayEntries(entries);
    displaySummary(entries);
  });
}

function displayEntries(entries) {
  entriesList.innerHTML = '';
  
  if (entries.length === 0) {
    entriesList.innerHTML = '<li>No entries yet</li>';
    return;
  }
  
  entries.forEach(entry => {
    const li = document.createElement('li');
    
    const date = new Date(entry.date);
    const formattedDate = date.toLocaleDateString();
    
    const durationHours = Math.floor(entry.duration / (1000 * 60 * 60));
    const durationMinutes = Math.floor((entry.duration % (1000 * 60 * 60)) / (1000 * 60));
    
    li.innerHTML = `
      <div><strong>${entry.project}</strong> - ${formattedDate}</div>
      <div>${durationHours}h ${durationMinutes}m</div>
      ${entry.notes ? `<div><em>${entry.notes}</em></div>` : ''}
    `;
    
    entriesList.appendChild(li);
  });
}

function displaySummary(entries) {
  const today = new Date().toISOString().split('T')[0];
  let totalDuration = 0;
  
  entries.forEach(entry => {
    if (entry.date === today) {
      totalDuration += entry.duration;
    }
  });
  
  const hours = Math.floor(totalDuration / (1000 * 60 * 60));
  const minutes = Math.floor((totalDuration % (1000 * 60 * 60)) / (1000 * 60));
  
  summaryDisplay.textContent = `${hours} hours ${minutes} minutes`;
}

function clearAllEntries() {
  if (confirm('Are you sure you want to delete all entries?')) {
    chrome.storage.local.set({ entries: [] }, function() {
      updateUI();
    });
  }
}

function exportData() {
  chrome.storage.local.get(['entries'], function(result) {
    const entries = result.entries || [];
    
    if (entries.length === 0) {
      alert('No data to export');
      return;
    }
    
    // Export as JSON
    const jsonBlob = new Blob([JSON.stringify(entries, null, 2)], { type: 'application/json' });
    const jsonUrl = URL.createObjectURL(jsonBlob);
    
    const jsonLink = document.createElement('a');
    jsonLink.href = jsonUrl;
    jsonLink.download = `localtrack-export-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(jsonLink);
    jsonLink.click();
    document.body.removeChild(jsonLink);
    URL.revokeObjectURL(jsonUrl);
    
    // Export as CSV
    const csvContent = convertEntriesToCSV(entries);
    const csvBlob = new Blob([csvContent], { type: 'text/csv' });
    const csvUrl = URL.createObjectURL(csvBlob);
    
    const csvLink = document.createElement('a');
    csvLink.href = csvUrl;
    csvLink.download = `localtrack-export-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(csvLink);
    csvLink.click();
    document.body.removeChild(csvLink);
    URL.revokeObjectURL(csvUrl);
  });
}

function convertEntriesToCSV(entries) {
  const headers = ['ID', 'Project', 'Date', 'Start Time', 'End Time', 'Duration (ms)', 'Notes'];
  const csvRows = [headers.join(',')];
  
  entries.forEach(entry => {
    const row = [
      entry.id,
      entry.project.replace(/,/g, ''), // Remove commas to avoid CSV issues
      entry.date,
      entry.startTime,
      entry.endTime,
      entry.duration,
      entry.notes ? entry.notes.replace(/,/g, '') : ''
    ];
    csvRows.push(row.join(','));
  });
  
  return csvRows.join('\n');
}

// Initialize the extension when popup loads
window.addEventListener('load', init);