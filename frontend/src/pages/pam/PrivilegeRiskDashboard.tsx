import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, TrendingUp, AlertTriangle } from 'lucide-react';

const RISKS = [
  { id: '1', entity: 'AWS Prod DB Admin', type: 'IDENTITY', score: 92, level: 'CRITICAL', factors: ['No MFA enforced on role assumption', 'Standing privilege for > 90 days without usage'] },
  { id: '2', entity: 'svc-data-sync', type: 'CREDENTIAL', score: 85, level: 'HIGH', factors: ['Credential overdue for rotation by 45 days', 'Used from anomalous IP block'] },
  { id: '3', entity: 'Global Admin Backup Cert', type: 'CREDENTIAL', score: 75, level: 'HIGH', factors: ['Certificate expired'] },
  { id: '4', entity: 'Admin Session - breakglass_01', type: 'SESSION', score: 60, level: 'MEDIUM', factors: ['Break-glass account in active use', 'Outside normal business hours'] }
];

export default function PrivilegeRiskDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PR_STYLES}</style>
      <div className="pr-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="pr-header-icon"><ShieldAlert size={24} /></div>
          <div>
            <h1 className="pr-title">Privilege Risk Scoring</h1>
            <p className="pr-subtitle">Contextual risk assessments for standing privileges, sessions, and credentials</p>
          </div>
        </div>
        <Link to="/pam" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← PAM</Link>
      </div>

      <div className="pr-card">
        <h3 className="pr-card-title"><TrendingUp size={16} /> Highest Risk Entities</h3>
        <table className="pr-table">
          <thead>
            <tr><th>Entity</th><th>Type</th><th>Risk Score</th><th>Risk Level</th><th>Contributing Factors</th></tr>
          </thead>
          <tbody>
            {RISKS.map(r => (
              <tr key={r.id} className="pr-row">
                <td style={{ fontWeight: 600 }}>{r.entity}</td>
                <td><span className="pr-type-badge">{r.type}</span></td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div style={{ width: 40, height: 4, background: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                      <div style={{ width: `${r.score}%`, height: '100%', background: r.level === 'CRITICAL' ? '#f87171' : r.level === 'HIGH' ? '#fbbf24' : '#60a5fa', borderRadius: 2 }} />
                    </div>
                    <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>{r.score}</span>
                  </div>
                </td>
                <td><span className={`pr-risk-badge pr-risk-${r.level.toLowerCase()}`}>{r.level}</span></td>
                <td>
                  <ul className="pr-factors-list">
                    {r.factors.map((f, i) => (
                      <li key={i}><AlertTriangle size={12} color="#f59e0b" /> {f}</li>
                    ))}
                  </ul>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const PR_STYLES = `
.pr-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.pr-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.pr-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.pr-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.pr-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.pr-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.pr-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.pr-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.pr-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.pr-row td { padding: 12px; }
.pr-type-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 0.75rem; font-family: monospace; }
.pr-risk-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.pr-risk-critical { background: rgba(239,68,68,0.15); color: #f87171; }
.pr-risk-high { background: rgba(245,158,11,0.15); color: #fbbf24; }
.pr-risk-medium { background: rgba(59,130,246,0.15); color: #60a5fa; }
.pr-factors-list { margin: 0; padding: 0; list-style: none; font-size: 0.8rem; color: #cbd5e1; display: flex; flex-direction: column; gap: 4px; }
.pr-factors-list li { display: flex; align-items: flex-start; gap: 6px; }
`;
