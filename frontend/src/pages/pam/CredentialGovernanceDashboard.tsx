import React from 'react';
import { Link } from 'react-router-dom';
import { Key, ShieldAlert, CheckCircle, RefreshCw } from 'lucide-react';

const CREDENTIALS = [
  { id: '1', name: 'AWS Root IAM Key', type: 'API_KEY', identity: 'breakglass_01', status: 'ACTIVE', compliant: true, rotation_days: 90, last_rotated: '2026-06-15' },
  { id: '2', name: 'Service Bus Connection String', type: 'SECRET', identity: 'svc-data-sync', status: 'ROTATION_PENDING', compliant: false, rotation_days: 30, last_rotated: '2026-06-25' },
  { id: '3', name: 'Global Admin Backup Cert', type: 'CERTIFICATE', identity: 'N/A', status: 'EXPIRED', compliant: false, rotation_days: 365, last_rotated: '2025-07-28' },
];

export default function CredentialGovernanceDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CG_STYLES}</style>
      <div className="cg-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="cg-header-icon"><Key size={24} /></div>
          <div>
            <h1 className="cg-title">Credential Lifecycle Governance</h1>
            <p className="cg-subtitle">Oversight of vault credentials, rotation policies, and lifecycle events</p>
          </div>
        </div>
        <Link to="/pam" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← PAM</Link>
      </div>

      <div className="cg-card">
        <h3 className="cg-card-title">Managed Privileged Credentials</h3>
        <table className="cg-table">
          <thead>
            <tr><th>Credential Name</th><th>Type</th><th>Linked Identity</th><th>Status</th><th>Policy Compliant</th><th>Rotation Interval</th><th>Last Rotated</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {CREDENTIALS.map(c => (
              <tr key={c.id} className="cg-row">
                <td style={{ fontWeight: 600 }}>{c.name}</td>
                <td><span className="cg-type-badge">{c.type}</span></td>
                <td style={{ color: '#94a3b8' }}>{c.identity}</td>
                <td><span className={`cg-status cg-${c.status.toLowerCase()}`}>{c.status.replace('_', ' ')}</span></td>
                <td>
                  {c.compliant ? 
                    <span style={{ color: '#34d399', display: 'flex', alignItems: 'center', gap: 4 }}><CheckCircle size={14} /> Yes</span> : 
                    <span style={{ color: '#f87171', display: 'flex', alignItems: 'center', gap: 4 }}><ShieldAlert size={14} /> No</span>}
                </td>
                <td style={{ color: '#94a3b8' }}>{c.rotation_days} days</td>
                <td style={{ color: '#cbd5e1' }}>{c.last_rotated}</td>
                <td>
                  <button className="cg-btn-rotate"><RefreshCw size={12} /> Force Rotate</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const CG_STYLES = `
.cg-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.cg-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.cg-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.cg-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.cg-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.cg-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.cg-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.cg-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.cg-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.cg-row td { padding: 12px; }
.cg-type-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 0.75rem; font-family: monospace; }
.cg-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.cg-active { background: rgba(16,185,129,0.15); color: #34d399; }
.cg-rotation_pending { background: rgba(245,158,11,0.15); color: #fbbf24; }
.cg-expired { background: rgba(239,68,68,0.15); color: #f87171; }
.cg-btn-rotate { display: inline-flex; align-items: center; gap: 4px; padding: 6px 10px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #e2e8f0; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.cg-btn-rotate:hover { background: rgba(255,255,255,0.1); }
`;
