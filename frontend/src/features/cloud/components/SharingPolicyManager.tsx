import React from 'react';
import './CloudStyles.css';

export const SharingPolicyManager: React.FC = () => {
  return (
    <div className="cloud-container">
      <header className="cloud-header flex-between">
        <div>
          <h2>Sharing Policies</h2>
          <p className="subtitle">Governance and data classification controls</p>
        </div>
        <button className="btn-primary glassmorphism">Create Policy</button>
      </header>

      <div className="policy-grid grid grid-cols-2 gap-4">
        <div className="cloud-panel glassmorphism hover-lift">
          <div className="flex-between">
            <h3>SOC Default Policy</h3>
            <span className="badge badge-success">Active</span>
          </div>
          <div className="mt-4">
            <p><strong>Max TLP:</strong> <span className="tlp-badge tlp-amber">TLP:AMBER</span></p>
            <p><strong>Requires Approval:</strong> Yes</p>
            <p><strong>Anonymize Source:</strong> True</p>
            <p><strong>Target Audiences:</strong> Internal, Partners</p>
          </div>
          <div className="mt-4">
            <button className="btn-secondary">Edit</button>
          </div>
        </div>

        <div className="cloud-panel glassmorphism hover-lift">
          <div className="flex-between">
            <h3>Strict Internal</h3>
            <span className="badge badge-success">Active</span>
          </div>
          <div className="mt-4">
            <p><strong>Max TLP:</strong> <span className="tlp-badge tlp-red">TLP:RED</span></p>
            <p><strong>Requires Approval:</strong> Yes</p>
            <p><strong>Anonymize Source:</strong> False</p>
            <p><strong>Target Audiences:</strong> Internal Only</p>
          </div>
          <div className="mt-4">
            <button className="btn-secondary">Edit</button>
          </div>
        </div>
      </div>
    </div>
  );
};
