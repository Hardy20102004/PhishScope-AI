import React from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, ShieldAlert } from 'lucide-react';

const VIOLATIONS = [
  { id: '1', rule: 'AP Clerk and AP Manager', identity: 'alice.smith', detected: '2026-07-29', severity: 'CRITICAL', status: 'UNRESOLVED' },
  { id: '2', rule: 'Dev and Prod Access', identity: 'bob.devops', detected: '2026-07-30', severity: 'HIGH', status: 'UNRESOLVED' }
];

export default function SoDDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{SOD_STYLES}</style>
      <div className="sod-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="sod-header-icon"><AlertTriangle size={24} /></div>
          <div>
            <h1 className="sod-title">Segregation of Duties (SoD)</h1>
            <p className="sod-subtitle">Detect and resolve conflicting entitlement assignments</p>
          </div>
        </div>
        <Link to="/iga" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← IGA</Link>
      </div>

      <div className="sod-card">
        <h3 className="sod-card-title"><ShieldAlert size={16} /> Active SoD Violations</h3>
        <table className="sod-table">
          <thead>
            <tr><th>Violated Rule</th><th>Identity</th><th>Detected Date</th><th>Severity</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            {VIOLATIONS.map(v => (
              <tr key={v.id} className="sod-row">
                <td style={{ fontWeight: 600 }}>{v.rule}</td>
                <td>{v.identity}</td>
                <td style={{ color: '#64748b' }}>{v.detected}</td>
                <td><span className={`sod-sev-badge sod-sev-${v.severity.toLowerCase()}`}>{v.severity}</span></td>
                <td style={{ color: '#ef4444', fontWeight: 600, fontSize: '0.75rem' }}>{v.status}</td>
                <td>
                  <button className="sod-btn-resolve">Resolve</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const SOD_STYLES = `
.sod-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.sod-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.sod-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.sod-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.sod-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.sod-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; color: #fca5a5; }
.sod-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.sod-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.sod-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.sod-row td { padding: 12px; }
.sod-sev-badge { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.sod-sev-critical { background: rgba(239,68,68,0.15); color: #fca5a5; }
.sod-sev-high { background: rgba(249,115,22,0.15); color: #fdba74; }
.sod-btn-resolve { padding: 6px 12px; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 6px; color: #fca5a5; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.sod-btn-resolve:hover { background: rgba(239,68,68,0.2); }
`;
