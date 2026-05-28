import React, { useState, useEffect } from 'react';

const Settings = () => {
  const [config, setConfig] = useState({ jiraUrl: '', username: '', apiKey: '' });

  useEffect(() => {
    const fetchConfig = async () => {
      const res = await fetch('/api/settings');
      const data = await res.json();
      setConfig(data);
    };
    fetchConfig();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    await fetch('/api/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
    alert('Settings saved!');
  };

  return (
    <div className="Settings">
      <h2>Jira Integration Settings</h2>
      <form onSubmit={handleSave}>
        <div className="form-group">
          <label>Jira Base URL</label>
          <input 
            type="text" 
            value={config.jiraUrl} 
            onChange={(e) => setConfig({ ...config, jiraUrl: e.target.value })}
            placeholder="https://your-jira-instance.com"
            required
          />
        </div>
        <div className="form-group">
          <label>Username</label>
          <input 
            type="text" 
            value={config.username} 
            onChange={(e) => setConfig({ ...config, username: e.target.value })}
            placeholder="Your Jira Username"
            required
          />
        </div>
        <div className="form-group">
          <label>API Key</label>
          <input 
            type="password" 
            value={config.apiKey} 
            onChange={(e) => setConfig({ ...config, apiKey: e.target.value })}
            placeholder="API Key from Jira Settings"
            required
          />
        </div>
        <button type="submit">Save Configuration</button>
      </form>
    </div>
  );
};

export default Settings;