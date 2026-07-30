import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, AlertTriangle } from 'lucide-react';

const RISKS = [
  { id: '1', identity: 'alice.security', overall: 88, auth_risk: 95, behavior_risk: 80, priv_risk: 90, level: 'CRITICAL', factors: ['Impossible travel detected', 'Password spray target'] },
  { id: '2', identity: 'bob.devops', overall: 72, auth_risk: 80, behavior_risk: 90, priv_risk: 45, level: 'HIGH', factors: ['Anomalous velocity', 'New device seen'] },
  { id: '3', identity: 'svc-backup', overall: 65, auth_risk: 95, behavior_risk: 20, priv_risk: 80, level: 'MEDIUM', factors: ['MFA fatigue indicators'] }
];

export default function IdentityRiskDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{IDR_STYLES}</style>
      <div className="idr-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="idr-header-icon"><TrendingUp size={24} /></div>
          <div>
            <h1 className="idr-title">Identity Risk Matrix</h1>
            <p className="idr-subtitle">Dynamic risk scores based on behavior, authentication, and privileges</p>
          </div>
        </div>
        <Link to="/itdr" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ITDR</Link>
      </div>

      <div className="idr-card">
        <h3 className="idr-card-title"><AlertTriangle size={16} /> Highest Risk Identities</h3>
        <table className="idr-table">
          <thead>
            <tr><th>Identity</th><th>Overall Score</th><th>Auth Risk</th><th>Behavior Risk</th><th>Privilege Risk</th><th>Risk Level</th><th>Key Factors</th></tr>
          </thead>
          <tbody>
            {RISKS.map(r => (
              <tr key={r.id} className="idr-row">
                <td style={{ fontWeight: 600 }}>{r.identity}</td>
                <td><strong style={{ fontSize: '1.1rem', color: r.level === 'CRITICAL' ? '#ef4444' : r.level === 'HIGH' ? '#f59e0b' : '#3b82f6' }}>{r.overall}</strong></td>
                <td style={{ color: '#94a3b8' }}>{r.auth_risk}</td>
                <td style={{ color: '#94a3b8' }}>{r.behavior_risk}</td>
                <td style={{ color: '#94a3b8' }}>{r.priv_risk}</td>
                <td><span className={`idr-risk-badge idr-risk-${r.level.toLowerCase()}`}>{r.level}</span></td>
                <td>
                  <ul className="idr-factors-list">
                    {r.factors.map((f, i) => (
                      <li key={i}>• {f}</li>
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

const IDR_STYLES = `
.idr-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.idr-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.idr-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.idr-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.idr-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.idr-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.idr-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.idr-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.idr-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.idr-row td { padding: 12px; }
.idr-risk-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.idr-risk-critical { background: rgba(239,68,68,0.15); color: #f87171; }
.idr-risk-high { background: rgba(245,158,11,0.15); color: #fbbf24; }
.idr-risk-medium { background: rgba(59,130,246,0.15); color: #60a5fa; }
.idr-factors-list { margin: 0; padding: 0; list-style: none; font-size: 0.75rem; color: #cbd5e1; display: flex; flex-direction: column; gap: 2px; }
`;
