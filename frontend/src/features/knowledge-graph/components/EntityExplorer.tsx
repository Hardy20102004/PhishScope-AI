import React from 'react';
import './KnowledgeGraphStyles.css';

export const EntityExplorer: React.FC = () => {
  return (
    <div className="kg-container">
      <header className="kg-header">
        <h2>Entity Explorer</h2>
        <p className="kg-subtitle">Search and inspect specific Threat Entities</p>
      </header>

      <div className="kg-search-bar glassmorphism">
        <input type="text" placeholder="Search for IPs, Domains, Malware, or Threat Actors..." className="kg-search-input" />
        <button className="kg-btn-primary">Search Graph</button>
      </div>

      <div className="kg-content-grid mt-4">
        <div className="kg-panel glassmorphism hover-lift">
          <div className="flex-between">
            <h3>APT29</h3>
            <span className="kg-badge kg-badge-neutral">THREAT_ACTOR</span>
          </div>
          <div className="mt-4 text-sm text-gray-300">
            <p><strong>Confidence:</strong> High (0.95)</p>
            <p><strong>Connected Edges:</strong> 142</p>
            <p><strong>Observed:</strong> 2024-01-10 to Present</p>
          </div>
          <div className="mt-4">
            <button className="kg-btn-secondary w-full">Visualize Neighborhood</button>
          </div>
        </div>

        <div className="kg-panel glassmorphism hover-lift">
          <div className="flex-between">
            <h3>192.168.1.5</h3>
            <span className="kg-badge kg-badge-neutral">IPV4</span>
          </div>
          <div className="mt-4 text-sm text-gray-300">
            <p><strong>Confidence:</strong> Medium (0.75)</p>
            <p><strong>Connected Edges:</strong> 3</p>
            <p><strong>Observed:</strong> 2026-07-20 to 2026-07-25</p>
          </div>
          <div className="mt-4">
            <button className="kg-btn-secondary w-full">Visualize Neighborhood</button>
          </div>
        </div>
      </div>
    </div>
  );
};
