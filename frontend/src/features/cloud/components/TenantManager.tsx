import React, { useState } from 'react';
import './CloudStyles.css';

interface Tenant {
  id: string;
  name: string;
  description: string;
  status: string;
}

export const TenantManager: React.FC = () => {
  const [tenants] = useState<Tenant[]>([
    { id: '1', name: 'Global HQ', description: 'Main corporate tenant', status: 'Active' },
    { id: '2', name: 'EMEA Division', description: 'European operations', status: 'Active' },
    { id: '3', name: 'APAC SOC', description: 'Asia Pacific Security', status: 'Active' },
  ]);

  return (
    <div className="cloud-container">
      <header className="cloud-header flex-between">
        <div>
          <h2>Tenant Management</h2>
          <p className="subtitle">Manage multi-tier organizational boundaries</p>
        </div>
        <button className="btn-primary glassmorphism">
          <span>+</span> New Tenant
        </button>
      </header>

      <div className="tenant-list">
        {tenants.map(tenant => (
          <div key={tenant.id} className="tenant-card glassmorphism hover-lift">
            <div className="tenant-header flex-between">
              <h3>{tenant.name}</h3>
              <span className="badge badge-success">{tenant.status}</span>
            </div>
            <p className="tenant-desc">{tenant.description}</p>
            <div className="tenant-actions">
              <button className="btn-secondary">Manage Workspaces</button>
              <button className="btn-icon">⚙️</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
