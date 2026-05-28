import React, { useState, useEffect } from 'react';

const Timer = ({ logs, setLogs, projects }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [selectedProject, setSelectedProject] = useState(projects[0]?.id || 'Default');

  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        setElapsed((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const toggleTimer = async () => {
    setIsRunning(!isRunning);
    if (!isRunning) {
      // Stop timer and save log
      const newLog = {
        id: Date.now(),
        project: selectedProject,
        duration: Math.floor(elapsed / 3600),
        date: new Date().toISOString().split('T')[0]
      };
      await fetch('/api/time', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newLog)
      });
      setLogs([...logs, newLog]);
      setElapsed(0);
    }
  };

  return (
    <div className="Timer">
      <div className="timer-display">{Math.floor(elapsed / 3600)}h {Math.floor((elapsed % 3600) / 60)}m</div>
      <div className="timer-controls">
        <select 
          value={selectedProject} 
          onChange={(e) => setSelectedProject(e.target.value)}
        >
          {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <button onClick={toggleTimer} className={isRunning ? 'running' : 'stopped'}>
          {isRunning ? 'Stop' : 'Start'}
        </button>
      </div>
    </div>
  );
};

export default Timer;