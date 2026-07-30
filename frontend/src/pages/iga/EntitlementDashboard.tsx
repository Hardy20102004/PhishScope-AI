import React from 'react';
import { Link } from 'react-router-dom';
import { Shield } from 'lucide-react';

const ENTITLEMENTS = [
  { id: '1', name: 'AWS Prod DB Admin', type: 'CLOUD_ROLE', system: 'AWS IAM', owners: ['security_team'], members: 14 },
  { id: '2', name: 'VPN Access', type: 'VPN_GROUP', system: 'Cisco AnyConnect', owners: ['net_ops'], members: 1250 },
  { id: '3', name: 'Financial Reports View', type: 'APP_ROLE', system: 'SAP', owners: ['finance_lead'], members: 45 }
];

export default function EntitlementDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ENT_STYLES}</style>
      <div className="ent-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ent-header-icon"><Shield size={24} /></div>
          <div>
            <h1 className="ent-title">Entitlement Inventory</h1>
            <p className="ent-subtitle">Catalog of all enterprise roles, groups, and permissions</p>
          </div>
        </div>
        <Link to="/iga" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← IGA</Link>
      </div>

      <div className="ent-card">
        <h3 className="ent-card-title">Managed Entitlements</h3>
        <table className="ent-table">
          <thead>
            <tr><th>Entitlement Name</th><th>Type</th><th>System</th><th>Owners</th><th>Assigned Members</th><th>Action</th></tr>
          </thead>
          <tbody>
            {ENTITLEMENTS.map(ent => (
              <tr key={ent.id} className="ent-row">
                <td style={{ fontWeight: 600 }}>{ent.name}</td>
                <td><span className="ent-type-badge">{ent.type.replace('_', ' ')}</span></td>
                <td style={{ color: '#94a3b8' }}>{ent.system}</td>
                <td style={{ color: '#cbd5e1' }}>{ent.owners.join(', ')}</td>
                <td style={{ fontWeight: 600 }}>{ent.members}</td>
                <td>
                  <button className="ent-btn-view">View Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const ENT_STYLES = `
.ent-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ent-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #14b8a6, #0d9488); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ent-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ent-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ent-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.ent-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.ent-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.ent-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.ent-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.ent-row td { padding: 12px; }
.ent-type-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.75rem; }
.ent-btn-view { padding: 6px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #e2e8f0; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.ent-btn-view:hover { background: rgba(255,255,255,0.1); }
`;
