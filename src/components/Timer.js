import React, { useState } from 'react';

function Timer() {
  const [description, setDescription] = useState('');
  const [project, setProject] = useState('');
  const [elapsed, setElapsed] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  const toggleTimer = () => {
    setIsRunning(!isRunning);
    // In a real app, this would send a POST request to start/stop timer
    // fetch('/api/timer', { method: 'POST', body: JSON.stringify({ description, project }) });
  };

  return (
    <div>
      <h2>Manual Timer</h2>
      <div className="form-group">
        <label>Project:</label>
        <select value={project} onChange={(e) => setProject(e.target.value)}>
          <option value="General">General</option>
          <option value="Development">Development</option>
          <option value="Meeting">Meeting</option>
        </select>
      </div>
      <div className="form-group">
        <label>Description:</label>
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description"
        />
      </div>
      <div>Elapsed: {Math.floor(elapsed / 60000)}m</div>
      <button onClick={toggleTimer} className={isRunning ? 'running' : 'stopped'}>
        {isRunning ? 'Stop Timer' : 'Start Timer'}
      </button>
    </div>
  );
}

export default Timer;