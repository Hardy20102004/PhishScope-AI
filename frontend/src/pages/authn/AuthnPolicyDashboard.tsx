import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, ShieldAlert, CheckCircle } from 'lucide-react';

const POLICIES = [
  { id: '1', name: 'Admin Zero Trust Access', target: 'Domain Admins', aal: 'AAL3', active: true },
  { id: '2', name: 'General Workforce', target: 'All Employees', aal: 'AAL2', active: true },
  { id: '3', name: 'Legacy System Bypass', target: 'Service Accounts', aal: 'AAL1', active: false }
];

export default function AuthnPolicyDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{POL_STYLES}</style>
      <div className="pol-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="pol-header-icon"><Shield size={24} /></div>
          <div>
            <h1 className="pol-title">Authentication Policies</h1>
            <p className="pol-subtitle">Govern access requirements and required assurance levels</p>
          </div>
        </div>
        <Link to="/authn" style={{ color: '#a78bfa', textDecoration: 'none', fontSize: '0.85rem' }}>← AUTHN Dashboard</Link>
      </div>

      <div className="pol-card">
        <h3 className="pol-card-title">Enforced Policies</h3>
        <table className="pol-table">
          <thead>
            <tr><th>Policy Name</th><th>Target Group</th><th>Required Assurance (AAL)</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            {POLICIES.map(pol => (
              <tr key={pol.id} className="pol-row">
                <td style={{ fontWeight: 600 }}>{pol.name}</td>
                <td style={{ color: '#94a3b8' }}>{pol.target}</td>
                <td><span className="pol-badge">{pol.aal}</span></td>
                <td>
                  <span className={`pol-status pol-status-${pol.active ? 'active' : 'inactive'}`}>
                    {pol.active ? 'ENFORCED' : 'DISABLED'}
                  </span>
                </td>
                <td>
                  <button className="pol-btn-view">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const POL_STYLES = `
.pol-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.pol-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.pol-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.pol-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.pol-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.pol-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.pol-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.pol-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.pol-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.pol-row td { padding: 12px; }
.pol-badge { padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-family: monospace; background: rgba(255,255,255,0.05); color: #cbd5e1; }
.pol-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.pol-status-active { background: rgba(16,185,129,0.15); color: #34d399; }
.pol-status-inactive { background: rgba(255,255,255,0.1); color: #94a3b8; }
.pol-btn-view { padding: 6px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #e2e8f0; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.pol-btn-view:hover { background: rgba(255,255,255,0.1); }
`;
