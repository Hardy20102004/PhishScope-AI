import React, { useState } from 'react';
import './CloudStyles.css';

interface Workspace {
  id: string;
  name: string;
  type: string;
  members: number;
}

export const WorkspaceExplorer: React.FC = () => {
  const [workspaces] = useState<Workspace[]>([
    { id: '1', name: 'SOC Incident Response', type: 'INCIDENT', members: 12 },
    { id: '2', name: 'APT29 Threat Hunting', type: 'THREAT_HUNTING', members: 5 },
    { id: '3', name: 'Global Malware Research', type: 'RESEARCH', members: 24 },
  ]);

  return (
    <div className="cloud-container">
      <header className="cloud-header flex-between">
        <div>
          <h2>Workspace Explorer</h2>
          <p className="subtitle">Isolated intelligence collaboration environments</p>
        </div>
        <button className="btn-primary glassmorphism">
          <span>+</span> Create Workspace
        </button>
      </header>

      <div className="workspace-grid">
        {workspaces.map(ws => (
          <div key={ws.id} className="workspace-card glassmorphism hover-lift">
            <div className="workspace-header">
              <h3>{ws.name}</h3>
              <span className="badge badge-neutral">{ws.type}</span>
            </div>
            <div className="workspace-stats">
              <div className="stat">
                <span className="stat-icon">👥</span> {ws.members} Members
              </div>
            </div>
            <div className="workspace-actions">
              <button className="btn-secondary">Enter Workspace</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
