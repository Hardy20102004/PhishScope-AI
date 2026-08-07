import React from 'react';
import { Link } from 'react-router-dom';
import { Cpu, AlertCircle, CheckCircle } from 'lucide-react';

const IDENTITIES = [
  { id: '1', name: 'prod-db-service-acc', type: 'SERVICE_ACCOUNT', provider: 'AWS IAM', env: 'Production', status: 'ROTATION_REQUIRED', last_rotated: '2025-10-01' },
  { id: '2', name: 'github-actions-deployer', type: 'API_KEY', provider: 'GitHub', env: 'CI/CD', status: 'ACTIVE', last_rotated: '2026-07-15' },
  { id: '3', name: 'legacy-app-svc', type: 'SERVICE_ACCOUNT', provider: 'Azure AD', env: 'Legacy', status: 'EXPIRED', last_rotated: '2024-01-10' }
];

export default function MachineIdentityDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{MI_STYLES}</style>
      <div className="mi-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="mi-header-icon"><Cpu size={24} /></div>
          <div>
            <h1 className="mi-title">Machine Identity Inventory</h1>
            <p className="mi-subtitle">Central visibility into service accounts and API keys</p>
          </div>
        </div>
        <Link to="/nhi" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← NHI Dashboard</Link>
      </div>

      <div className="mi-card">
        <h3 className="mi-card-title">All Managed Machine Identities</h3>
        <table className="mi-table">
          <thead>
            <tr><th>Identity Name</th><th>Type</th><th>Provider</th><th>Environment</th><th>Credential Status</th><th>Last Rotated</th><th>Action</th></tr>
          </thead>
          <tbody>
            {IDENTITIES.map(id => (
              <tr key={id.id} className="mi-row">
                <td style={{ fontWeight: 600 }}>{id.name}</td>
                <td><span className="mi-type-badge">{id.type.replace('_', ' ')}</span></td>
                <td style={{ color: '#94a3b8' }}>{id.provider}</td>
                <td style={{ color: '#cbd5e1' }}>{id.env}</td>
                <td>
                  <span className={`mi-status mi-${id.status.toLowerCase()}`}>
                    {id.status.replace('_', ' ')}
                  </span>
                </td>
                <td style={{ color: '#94a3b8' }}>{id.last_rotated}</td>
                <td>
                  {id.status !== 'ACTIVE' && (
                    <button className="mi-btn-rotate"><AlertCircle size={12} /> Force Rotation</button>
                  )}
                  {id.status === 'ACTIVE' && (
                    <button className="mi-btn-view"><CheckCircle size={12} /> Healthy</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const MI_STYLES = `
.mi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.mi-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.mi-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.mi-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.mi-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.mi-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.mi-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.mi-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.mi-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.mi-row td { padding: 12px; }
.mi-type-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.75rem; }
.mi-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.mi-active { background: rgba(16,185,129,0.15); color: #34d399; }
.mi-rotation_required { background: rgba(245,158,11,0.15); color: #fbbf24; }
.mi-expired { background: rgba(239,68,68,0.15); color: #f87171; }
.mi-btn-rotate { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; background: rgba(245,158,11,0.2); border: 1px solid rgba(245,158,11,0.4); border-radius: 4px; color: #fbbf24; cursor: pointer; font-size: 0.75rem; font-weight: 600; }
.mi-btn-view { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; background: transparent; border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; color: #94a3b8; font-size: 0.75rem; }
`;
