import React from 'react';
import { Link } from 'react-router-dom';
import { UserCheck, FileSignature } from 'lucide-react';

const GOV_APPROVALS = [
  { id: '1', request: 'JIT Elevation (AWS Admin)', user: 'david.smith', module: 'PAM', status: 'PENDING' },
  { id: '2', request: 'B2B Trust Configuration', user: 'vendor_admin', module: 'FEDERATION', status: 'APPROVED' },
  { id: '3', request: 'Service Account Creation', user: 'ci_cd_pipeline', module: 'NHI', status: 'PENDING' }
];

export default function UnifiedGovernanceDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{UGOV_STYLES}</style>
      <div className="ugov-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ugov-header-icon"><UserCheck size={24} /></div>
          <div>
            <h1 className="ugov-title">Unified Governance</h1>
            <p className="ugov-subtitle">Centralized human approval gate for all identity operations</p>
          </div>
        </div>
        <Link to="/identity-cc" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Command Center</Link>
      </div>

      <div className="ugov-card">
        <h3 className="ugov-card-title"><FileSignature size={16} /> Pending Strategic Approvals</h3>
        <table className="ugov-table">
          <thead>
            <tr><th>Governance Request</th><th>Subject Identity</th><th>Source Module</th><th>Approval Status</th></tr>
          </thead>
          <tbody>
            {GOV_APPROVALS.map(gov => (
              <tr key={gov.id} className="ugov-row">
                <td style={{ fontWeight: 600 }}>{gov.request}</td>
                <td style={{ color: '#94a3b8' }}>{gov.user}</td>
                <td>
                  <span className="ugov-module-badge">{gov.module}</span>
                </td>
                <td>
                  <span className={`ugov-status ugov-${gov.status.toLowerCase()}`}>
                    {gov.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const UGOV_STYLES = `
.ugov-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ugov-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ugov-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ugov-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ugov-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.ugov-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.ugov-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.ugov-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.ugov-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.ugov-row td { padding: 12px; }
.ugov-module-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; font-size: 0.7rem; color: #cbd5e1; }
.ugov-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.ugov-pending { background: rgba(245,158,11,0.15); color: #fbbf24; }
.ugov-approved { background: rgba(16,185,129,0.15); color: #34d399; }
`;
