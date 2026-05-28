import React, { useState } from 'react';

function Settings() {
  const [jiraUrl, setJiraUrl] = useState('');
  const [username, setUsername] = useState('');
  const [apiKey, setApiKey] = useState('');

  const saveSettings = () => {
    // POST to backend to save config
    fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ jiraUrl, username, apiKey })
    });
  };

  return (
    <div>
      <h2>Jira Configuration</h2>
      <div className="form-group">
        <label>Jira Base URL:</label>
        <input
          value={jiraUrl}
          onChange={(e) => setJiraUrl(e.target.value)}
          placeholder="https://my-jira.company.com"
        />
      </div>
      <div className="form-group">
        <label>Username:</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label>API Key:</label>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </div>
      <button onClick={saveSettings}>Save Configuration</button>
    </div>
  );
}

export default Settings;