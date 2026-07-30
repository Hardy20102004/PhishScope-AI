import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Activity } from 'lucide-react';

const ASSURANCE = [
  { id: '1', group: 'Domain Admins', current_aal: 'AAL1', required_aal: 'AAL3', gap: true, users_failing: 45 },
  { id: '2', group: 'Engineering', current_aal: 'AAL2', required_aal: 'AAL2', gap: false, users_failing: 12 },
  { id: '3', group: 'Finance', current_aal: 'AAL3', required_aal: 'AAL3', gap: false, users_failing: 0 }
];

export default function AssuranceDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{AAL_STYLES}</style>
      <div className="aal-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="aal-header-icon"><ShieldCheck size={24} /></div>
          <div>
            <h1 className="aal-title">Authentication Assurance Levels (AAL)</h1>
            <p className="aal-subtitle">Monitor NIST SP 800-63B authentication strength compliance</p>
          </div>
        </div>
        <Link to="/authn" style={{ color: '#a78bfa', textDecoration: 'none', fontSize: '0.85rem' }}>← AUTHN Dashboard</Link>
      </div>

      <div className="aal-card">
        <h3 className="aal-card-title"><Activity size={16} /> AAL Compliance by Group</h3>
        <table className="aal-table">
          <thead>
            <tr><th>Identity Group</th><th>Current Avg AAL</th><th>Required AAL Policy</th><th>Status</th><th>Non-Compliant Users</th></tr>
          </thead>
          <tbody>
            {ASSURANCE.map(aal => (
              <tr key={aal.id} className="aal-row">
                <td style={{ fontWeight: 600 }}>{aal.group}</td>
                <td><span className={`aal-badge aal-badge-${aal.current_aal.toLowerCase()}`}>{aal.current_aal}</span></td>
                <td style={{ color: '#94a3b8' }}>{aal.required_aal}</td>
                <td>
                  <span className={`aal-status aal-status-${aal.gap ? 'gap' : 'ok'}`}>
                    {aal.gap ? 'POLICY VIOLATION' : 'COMPLIANT'}
                  </span>
                </td>
                <td style={{ color: aal.users_failing > 0 ? '#ef4444' : '#10b981', fontWeight: 600 }}>
                  {aal.users_failing}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const AAL_STYLES = `
.aal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.aal-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.aal-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.aal-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.aal-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.aal-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.aal-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.aal-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.aal-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.aal-row td { padding: 12px; }
.aal-badge { padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-family: monospace; }
.aal-badge-aal1 { background: rgba(239,68,68,0.2); color: #fca5a5; }
.aal-badge-aal2 { background: rgba(245,158,11,0.2); color: #fcd34d; }
.aal-badge-aal3 { background: rgba(16,185,129,0.2); color: #6ee7b7; }
.aal-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.aal-status-gap { background: rgba(239,68,68,0.15); color: #f87171; }
.aal-status-ok { background: rgba(16,185,129,0.15); color: #34d399; }
`;
