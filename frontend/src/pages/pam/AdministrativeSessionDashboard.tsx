import React from 'react';
import { Link } from 'react-router-dom';
import { Server, ShieldAlert, Activity, Eye, Video } from 'lucide-react';

const SESSIONS = [
  { id: '1', identity: 'aws-prod-dba', resource: 'Production Aurora DB', type: 'JIT_ELEVATED', status: 'ACTIVE', risk: 'LOW', started: '10:15 AM' },
  { id: '2', identity: 'global_admin@corp.com', resource: 'Entra Admin Portal', type: 'STANDING', status: 'ACTIVE', risk: 'MEDIUM', started: '09:30 AM' },
  { id: '3', identity: 'breakglass_01', resource: 'Root AWS Account', type: 'EMERGENCY', status: 'ACTIVE', risk: 'CRITICAL', started: '10:45 AM' },
  { id: '4', identity: 'network-admin', resource: 'Core Switch 01', type: 'JIT_ELEVATED', status: 'COMPLETED', risk: 'LOW', started: '08:00 AM' }
];

export default function AdministrativeSessionDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{AS_STYLES}</style>
      <div className="as-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="as-header-icon"><Server size={24} /></div>
          <div>
            <h1 className="as-title">Administrative Session Governance</h1>
            <p className="as-subtitle">Monitor live privileged sessions and audit historical access</p>
          </div>
        </div>
        <Link to="/pam" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← PAM</Link>
      </div>

      <div className="as-card">
        <h3 className="as-card-title"><Activity size={16} /> Active & Recent Privileged Sessions</h3>
        <table className="as-table">
          <thead>
            <tr><th>Identity</th><th>Target Resource</th><th>Access Type</th><th>Risk Level</th><th>Started At</th><th>Status</th><th>Audit</th></tr>
          </thead>
          <tbody>
            {SESSIONS.map(s => (
              <tr key={s.id} className="as-row">
                <td style={{ fontWeight: 600 }}>{s.identity}</td>
                <td style={{ color: '#94a3b8' }}>{s.resource}</td>
                <td><span className={`as-type-badge as-type-${s.type.toLowerCase()}`}>{s.type.replace('_', ' ')}</span></td>
                <td><span className={`as-risk-badge as-risk-${s.risk.toLowerCase()}`}>{s.risk}</span></td>
                <td style={{ color: '#64748b' }}>{s.started}</td>
                <td>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: s.status === 'ACTIVE' ? '#34d399' : '#94a3b8' }}>
                    {s.status}
                  </span>
                </td>
                <td>
                  <button className="as-btn-audit"><Video size={14} /> View Record</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const AS_STYLES = `
.as-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.as-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.as-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.as-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.as-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.as-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.as-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.as-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.as-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.as-row td { padding: 12px; }
.as-type-badge { padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.as-type-jit_elevated { background: rgba(16,185,129,0.15); color: #34d399; }
.as-type-standing { background: rgba(245,158,11,0.15); color: #fbbf24; }
.as-type-emergency { background: rgba(239,68,68,0.15); color: #f87171; }
.as-risk-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.as-risk-critical { background: rgba(239,68,68,0.15); color: #f87171; }
.as-risk-medium { background: rgba(245,158,11,0.15); color: #fbbf24; }
.as-risk-low { background: rgba(59,130,246,0.15); color: #60a5fa; }
.as-btn-audit { display: inline-flex; align-items: center; gap: 4px; padding: 6px 10px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #cbd5e1; cursor: pointer; font-size: 0.75rem; font-weight: 500; transition: background 0.2s; }
.as-btn-audit:hover { background: rgba(255,255,255,0.1); color: white; }
`;
