import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import Timer from './components/Timer';
import Settings from './components/Settings';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="App">
      <h1>JiraTime Tracker</h1>
      <div className="tabs">
        <button onClick={() => setActiveTab('dashboard')}>Dashboard</button>
        <button onClick={() => setActiveTab('timer')}>Timer</button>
        <button onClick={() => setActiveTab('settings')}>Settings</button>
      </div>
      {activeTab === 'dashboard' && <Dashboard />}
      {activeTab === 'timer' && <Timer />}
      {activeTab === 'settings' && <Settings />}
    </div>
  );
}

export default App;