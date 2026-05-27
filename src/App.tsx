import React, { useState } from 'react';
import './App.css';

function App() {
  const [timeEntries, setTimeEntries] = useState([]);
  const [newEntry, setNewEntry] = useState({ project: '', hours: 0 });

  const addEntry = () => {
    if (newEntry.project.trim()) {
      setTimeEntries([...timeEntries, newEntry]);
      setNewEntry({ project: '', hours: 0 });
    }
  };

  return (
    <div className="App">
      <h1>Time Tracker</h1>
      <div>
        <input
          type="text"
          placeholder="Project name"
          value={newEntry.project}
          onChange={(e) => setNewEntry({...newEntry, project: e.target.value})}
        />
        <input
          type="number"
          placeholder="Hours"
          value={newEntry.hours}
          onChange={(e) => setNewEntry({...newEntry, hours: Number(e.target.value)})}
        />
        <button onClick={addEntry}>Add Entry</button>
      </div>
      <ul>
        {timeEntries.map((entry, index) => (
          <li key={index}>{entry.project}: {entry.hours} hours</li>
        ))}
      </ul>
    </div>
  );
}

export default App;