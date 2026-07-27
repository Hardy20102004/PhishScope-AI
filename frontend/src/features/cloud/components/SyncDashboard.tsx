import React from 'react';
import './CloudStyles.css';

export const SyncDashboard: React.FC = () => {
  return (
    <div className="cloud-container">
      <header className="cloud-header">
        <h2>Synchronization & Conflicts</h2>
        <p className="subtitle">Monitor active syncs and resolve conflicts</p>
      </header>

      <div className="sync-section glassmorphism">
        <h3>Pending Conflicts (1)</h3>
        <div className="conflict-row flex-between">
          <div>
            <h4>Indicator: IP 192.168.1.100</h4>
            <p>Local version: 2 | Remote version: 3</p>
          </div>
          <div className="conflict-actions">
            <button className="btn-secondary">Keep Local</button>
            <button className="btn-primary">Accept Remote</button>
            <button className="btn-secondary">Manual Merge</button>
          </div>
        </div>
      </div>

      <div className="sync-section glassmorphism mt-4">
        <h3>Sync History</h3>
        <table className="sync-table">
          <thead>
            <tr>
              <th>Node</th>
              <th>Type</th>
              <th>Objects Synced</th>
              <th>Status</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>CISA TAXII Node</td>
              <td>PULL</td>
              <td>15</td>
              <td><span className="text-success">SUCCESS</span></td>
              <td>2 mins ago</td>
            </tr>
            <tr>
              <td>Financial ISAC</td>
              <td>PUSH</td>
              <td>8</td>
              <td><span className="text-success">SUCCESS</span></td>
              <td>10 mins ago</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
