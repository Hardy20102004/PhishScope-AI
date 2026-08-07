import React, { useState, useEffect } from 'react';
import './CloudStyles.css';

export const CloudDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState({
    active_tenants: 0,
    active_workspaces: 0,
    shared_objects: 0,
    federation_health: 'OPTIMAL'
  });

  useEffect(() => {
    // In a real app, this would fetch from /api/v1/cloud/analytics/summary
    // Mocking for now to show premium UI
    setTimeout(() => {
      setMetrics({
        active_tenants: 12,
        active_workspaces: 48,
        shared_objects: 1024,
        federation_health: 'OPTIMAL'
      });
    }, 1000);
  }, []);

  return (
    <div className="cloud-container">
      <header className="cloud-header">
        <h1>Enterprise Threat Intelligence Cloud</h1>
        <p className="subtitle">Global Intelligence Federation & Synchronization</p>
      </header>

      <div className="cloud-metrics-grid">
        <div className="metric-card glassmorphism hover-lift">
          <div className="metric-icon tenant-icon">🏢</div>
          <div className="metric-content">
            <h3>Active Tenants</h3>
            <div className="metric-value">{metrics.active_tenants}</div>
          </div>
        </div>

        <div className="metric-card glassmorphism hover-lift">
          <div className="metric-icon workspace-icon">📁</div>
          <div className="metric-content">
            <h3>Workspaces</h3>
            <div className="metric-value">{metrics.active_workspaces}</div>
          </div>
        </div>

        <div className="metric-card glassmorphism hover-lift">
          <div className="metric-icon share-icon">🌐</div>
          <div className="metric-content">
            <h3>Shared Intelligence</h3>
            <div className="metric-value">{metrics.shared_objects.toLocaleString()}</div>
          </div>
        </div>

        <div className="metric-card glassmorphism hover-lift">
          <div className="metric-icon health-icon">🛡️</div>
          <div className="metric-content">
            <h3>Federation Health</h3>
            <div className="metric-value health-optimal">{metrics.federation_health}</div>
          </div>
        </div>
      </div>

      <div className="cloud-content-grid">
        <div className="cloud-panel glassmorphism">
          <h2>Recent Federation Activity</h2>
          <ul className="activity-list">
            <li>
              <span className="activity-time">10:42 AM</span>
              <span className="activity-desc">Synced 15 STIX objects from <strong>CISA TAXII Node</strong></span>
              <span className="badge badge-success">Success</span>
            </li>
            <li>
              <span className="activity-time">09:15 AM</span>
              <span className="activity-desc">Pushed Campaign Alpha to <strong>Financial ISAC</strong></span>
              <span className="badge badge-success">Success</span>
            </li>
            <li>
              <span className="activity-time">08:30 AM</span>
              <span className="activity-desc">Conflict detected on Indicator X in <strong>Internal Workspace</strong></span>
              <span className="badge badge-warning">Pending Resolution</span>
            </li>
          </ul>
        </div>

        <div className="cloud-panel glassmorphism">
          <h2>Knowledge Exchange Highlights</h2>
          <div className="exchange-preview">
            <div className="exchange-item">
              <h4>Ransomware TTPs 2026</h4>
              <p>Shared by: Global SecOps</p>
              <div className="tlp-badge tlp-amber">TLP:AMBER</div>
            </div>
            <div className="exchange-item">
              <h4>Zero-Day IOCs</h4>
              <p>Shared by: Threat Intel Dept</p>
              <div className="tlp-badge tlp-red">TLP:RED</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
