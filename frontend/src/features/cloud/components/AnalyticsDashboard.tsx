import React from 'react';
import './CloudStyles.css';

export const AnalyticsDashboard: React.FC = () => {
  return (
    <div className="cloud-container">
      <header className="cloud-header">
        <h2>Cloud Analytics</h2>
        <p className="subtitle">Sharing trends and collaboration statistics</p>
      </header>

      <div className="cloud-metrics-grid">
        <div className="metric-card glassmorphism">
          <div className="metric-icon">📈</div>
          <div className="metric-content">
            <h3>Sharing Velocity (24h)</h3>
            <div className="metric-value">+42 Objects</div>
          </div>
        </div>
        <div className="metric-card glassmorphism">
          <div className="metric-icon">🤝</div>
          <div className="metric-content">
            <h3>Active Collaborators</h3>
            <div className="metric-value">128 Users</div>
          </div>
        </div>
        <div className="metric-card glassmorphism">
          <div className="metric-icon">🏢</div>
          <div className="metric-content">
            <h3>Partner Engagements</h3>
            <div className="metric-value">8 Active Nodes</div>
          </div>
        </div>
      </div>

      <div className="cloud-panel glassmorphism mt-4">
        <h3>Top Sharing Workspaces</h3>
        <table className="sync-table">
          <thead>
            <tr>
              <th>Workspace</th>
              <th>Objects Shared</th>
              <th>Primary TLP</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>SOC Incident Response</td>
              <td>142</td>
              <td><span className="tlp-badge tlp-amber">AMBER</span></td>
            </tr>
            <tr>
              <td>Global Malware Research</td>
              <td>89</td>
              <td><span className="tlp-badge tlp-amber">AMBER</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
