import React from 'react';
import './TimelineStyles.css';

export const TimelineDashboard: React.FC = () => {
  return (
    <div className="tl-container">
      <header className="tl-header">
        <h1>Enterprise Threat Timeline Intelligence</h1>
        <p className="tl-subtitle">Chronological evidence-backed tracking of cyber threats</p>
      </header>

      <div className="tl-metrics-grid">
        <div className="tl-metric-card glassmorphism hover-lift">
          <div className="tl-metric-icon">⏱️</div>
          <div className="tl-metric-content">
            <h3>Active Timelines</h3>
            <div className="tl-metric-value">24</div>
          </div>
        </div>
        <div className="tl-metric-card glassmorphism hover-lift">
          <div className="tl-metric-icon">📑</div>
          <div className="tl-metric-content">
            <h3>Events Indexed</h3>
            <div className="tl-metric-value">142,850</div>
          </div>
        </div>
        <div className="tl-metric-card glassmorphism hover-lift">
          <div className="tl-metric-icon">🧠</div>
          <div className="tl-metric-content">
            <h3>AI Reconstructions</h3>
            <div className="tl-metric-value tl-accent">1,204</div>
          </div>
        </div>
      </div>

      <div className="tl-panel glassmorphism">
        <div className="flex-between mb-4">
          <h2>Recent Timelines</h2>
          <button className="tl-btn-primary">Create New Timeline</button>
        </div>
        
        <table className="tl-table w-full">
          <thead>
            <tr>
              <th>Timeline Name</th>
              <th>Type</th>
              <th>Duration</th>
              <th>Events</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>APT29 Infrastructure Shift</strong></td>
              <td><span className="tl-badge">THREAT_ACTOR</span></td>
              <td>45 Days</td>
              <td>128</td>
              <td><span className="text-green-400">Tracking</span></td>
            </tr>
            <tr>
              <td><strong>Campaign Alpha Spearphishing</strong></td>
              <td><span className="tl-badge">CAMPAIGN</span></td>
              <td>12 Days</td>
              <td>42</td>
              <td><span className="text-yellow-400">Reconstructing</span></td>
            </tr>
            <tr>
              <td><strong>SOC Incident #8892</strong></td>
              <td><span className="tl-badge">INVESTIGATION</span></td>
              <td>2 Hours</td>
              <td>15</td>
              <td><span className="text-green-400">Active</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
