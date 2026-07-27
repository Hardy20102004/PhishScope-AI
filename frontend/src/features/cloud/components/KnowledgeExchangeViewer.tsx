import React from 'react';
import './CloudStyles.css';

export const KnowledgeExchangeViewer: React.FC = () => {
  return (
    <div className="cloud-container">
      <header className="cloud-header">
        <h2>Knowledge Exchange</h2>
        <p className="subtitle">Discover intelligence shared across the federation</p>
      </header>

      <div className="search-bar glassmorphism">
        <input type="text" placeholder="Search across federation..." className="search-input" />
        <button className="btn-primary">Search</button>
      </div>

      <div className="exchange-results">
        <div className="exchange-row glassmorphism hover-lift flex-between">
          <div className="row-info">
            <h4>Campaign: Operation Cobalt</h4>
            <p className="row-meta">Source: Financial ISAC | Confidence: High</p>
          </div>
          <div className="row-actions">
            <span className="tlp-badge tlp-amber">TLP:AMBER</span>
            <button className="btn-secondary">View Details</button>
          </div>
        </div>

        <div className="exchange-row glassmorphism hover-lift flex-between">
          <div className="row-info">
            <h4>Threat Actor: Lazarus Group TTPs</h4>
            <p className="row-meta">Source: Government CERT | Confidence: Critical</p>
          </div>
          <div className="row-actions">
            <span className="tlp-badge tlp-red">TLP:RED</span>
            <button className="btn-secondary">View Details</button>
          </div>
        </div>
      </div>
    </div>
  );
};
