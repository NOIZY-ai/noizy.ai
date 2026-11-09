import React, { useState, useEffect } from 'react';

/**
 * MissionControl.tsx
 *
 * Description:
 * React dashboard. Status, agents, actions.
 * Visualizes the "Brain" state.
 * STRICT MODE: Enabled.
 */

interface MissionControlState {
    systemHealth: 'ONLINE' | 'OFFLINE' | 'DEGRADED';
    activeAgents: string[];
    logStream: string[];
}

const MissionControl: React.FC = () => {
  const [systemHealth, setSystemHealth] = useState<MissionControlState['systemHealth']>('ONLINE');
  const [activeAgents, setActiveAgents] = useState<string[]>(['SHIRL', 'GABRIEL', 'ENGR_KEITH']);
  const [logStream, setLogStream] = useState<string[]>([]);

  useEffect(() => {
    // Poll for status (mock)
    const interval = setInterval(() => {
      setLogStream(prev => [`[${new Date().toLocaleTimeString()}] System Pulse Check OK`, ...prev.slice(0, 9)]);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="mission-control-container" style={{ background: '#000', color: '#0f0', fontFamily: 'monospace', padding: '20px', minHeight: '100vh' }}>
      <h1>MISSION CONTROL // GORUNFREE</h1>
      
      <div className="grid-layout" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        
        <div className="panel status-panel" style={{ border: '1px solid #333', padding: '10px' }}>
          <h2>SYSTEM STATUS</h2>
          <div style={{ fontSize: '24px', color: systemHealth === 'ONLINE' ? '#0f0' : '#f00' }}>
            {systemHealth}
          </div>
          <p>Latency: &lt; 7ms</p>
          <p>Memory Usage: Optimized</p>
        </div>

        <div className="panel agent-panel" style={{ border: '1px solid #333', padding: '10px' }}>
          <h2>ACTIVE AGENTS</h2>
          <ul>
            {activeAgents.map(agent => (
              <li key={agent} style={{ listStyle: 'none', margin: '5px 0' }}>
                 🟢 {agent} - ACTIVE
              </li>
            ))}
          </ul>
        </div>

        <div className="panel log-panel" style={{ gridColumn: '1 / 3', border: '1px solid #333', padding: '10px' }}>
          <h2>LIVE FEED</h2>
          <div className="logs" style={{ height: '200px', overflowY: 'auto' }}>
            {logStream.map((log, i) => (
              <div key={i} className="log-line">{log}</div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default MissionControl;
