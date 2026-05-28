import React, { useState, useEffect } from 'react';
import Timer from './Timer';

const Dashboard = () => {
  const [logs, setLogs] = useState([]);
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const res = await fetch('/api/time');
      const data = await res.json();
      setLogs(data.logs);
    };
    const fetchProjects = async () => {
      const res = await fetch('/api/projects');
      const data = await res.json();
      setProjects(data);
    };
    fetchLogs();
    fetchProjects();
  }, []);

  return (
    <div className="Dashboard">
      <h1>Time Tracker Dashboard</h1>
      <Timer logs={logs} setLogs={setLogs} projects={projects} />
      <div className="logs-section">
        <h2>Time Logs</h2>
        {logs.map((log, index) => (
          <div key={index} className="log-item">
            <span>{log.project}:</span>
            <span>{log.duration}h</span>
            <span>{log.date}</span>
          </div>
        ))}
      </div>
      <div className="projects-section">
        <h2>Available Projects</h2>
        <ul>
          {projects.map((p, index) => (
            <li key={index}>{p.name} ({p.id})</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;