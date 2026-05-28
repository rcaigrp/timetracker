import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch('/api/projects')
      .then(res => res.json())
      .then(data => setProjects(data));
    fetch('/api/logs')
      .then(res => res.json())
      .then(data => setLogs(data));
  }, []);

  return (
    <div>
      <h2>Active Projects</h2>
      <ul>
        {projects.map(p => <li key={p.id}>{p.name}</li>)}
      </ul>
      <h2>Time Logs</h2>
      <ul>
        {logs.map(log => (
          <li key={log.id}>
            {log.description} - {log.project} - {log.duration}h
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;