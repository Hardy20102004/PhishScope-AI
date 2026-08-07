import React from 'react';
import { Link } from 'react-router-dom';
import { UserCheck, ShieldAlert } from 'lucide-react';

const ENROLLMENTS = [
  { id: '1', user: 'david.smith', methods: ['Password', 'SMS OTP'], coverage: 'Low (Legacy)', last_login: '2026-07-30 08:00', risk: 'HIGH' },
  { id: '2', user: 'sarah.connor', methods: ['Apple Passkey', 'YubiKey (Backup)'], coverage: 'High (Passwordless)', last_login: '2026-07-29 14:30', risk: 'LOW' }
];

export default function EnrollmentDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ENR_STYLES}</style>
      <div className="enr-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="enr-header-icon"><UserCheck size={24} /></div>
          <div>
            <h1 className="enr-title">User Enrollments & Coverage</h1>
            <p className="enr-subtitle">Track authentication methods enrolled per user identity</p>
          </div>
        </div>
        <Link to="/authn" style={{ color: '#a78bfa', textDecoration: 'none', fontSize: '0.85rem' }}>← AUTHN Dashboard</Link>
      </div>

      <div className="enr-card">
        <h3 className="enr-card-title"><ShieldAlert size={16} /> Identity Enrollment Posture</h3>
        <table className="enr-table">
          <thead>
            <tr><th>Identity</th><th>Enrolled Methods</th><th>Coverage Posture</th><th>Last Successful Login</th><th>Auth Risk</th></tr>
          </thead>
          <tbody>
            {ENROLLMENTS.map(enr => (
              <tr key={enr.id} className="enr-row">
                <td style={{ fontWeight: 600 }}>{enr.user}</td>
                <td>
                  <div style={{ display: 'flex', gap: 6 }}>
                    {enr.methods.map(m => (
                      <span key={m} className="enr-method-badge">{m}</span>
                    ))}
                  </div>
                </td>
                <td style={{ color: '#94a3b8' }}>{enr.coverage}</td>
                <td style={{ color: '#cbd5e1' }}>{enr.last_login}</td>
                <td><span className={`enr-risk enr-risk-${enr.risk.toLowerCase()}`}>{enr.risk}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const ENR_STYLES = `
.enr-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.enr-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.enr-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.enr-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.enr-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.enr-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.enr-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.enr-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.enr-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.enr-row td { padding: 12px; }
.enr-method-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 0.7rem; color: #cbd5e1; white-space: nowrap; }
.enr-risk { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.enr-risk-high { background: rgba(239,68,68,0.15); color: #f87171; }
.enr-risk-low { background: rgba(16,185,129,0.15); color: #34d399; }
`;
