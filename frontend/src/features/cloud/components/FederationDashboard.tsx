import React from 'react';
import './CloudStyles.css';

export const FederationDashboard: React.FC = () => {
  return (
    <div className="cloud-container">
      <header className="cloud-header flex-between">
        <div>
          <h2>Federation Manager</h2>
          <p className="subtitle">Manage connections to partner TAXII and STIX nodes</p>
        </div>
        <button className="btn-primary glassmorphism">Add Node</button>
      </header>

      <div className="node-grid">
        <div className="node-card glassmorphism hover-lift">
          <div className="node-header">
            <h3>CISA TAXII Node</h3>
            <span className="badge badge-success">Online</span>
          </div>
          <div className="node-details">
            <p><strong>URL:</strong> https://taxii.cisa.gov</p>
            <p><strong>Type:</strong> GOVERNMENT</p>
            <p><strong>Auth:</strong> mTLS</p>
          </div>
          <div className="node-actions">
            <button className="btn-secondary">Test Connection</button>
            <button className="btn-secondary">Trigger Sync</button>
          </div>
        </div>

        <div className="node-card glassmorphism hover-lift">
          <div className="node-header">
            <h3>Financial ISAC</h3>
            <span className="badge badge-warning">Degraded</span>
          </div>
          <div className="node-details">
            <p><strong>URL:</strong> https://taxii.fsisac.com</p>
            <p><strong>Type:</strong> PARTNER</p>
            <p><strong>Auth:</strong> API_KEY</p>
          </div>
          <div className="node-actions">
            <button className="btn-secondary">Test Connection</button>
            <button className="btn-secondary">Trigger Sync</button>
          </div>
        </div>
      </div>
    </div>
  );
};
