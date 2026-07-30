import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, ShieldAlert } from 'lucide-react';

const TRUST_SCORES = [
  { id: '1', user: 'david.smith (Admin)', composite: 45.2, auth_conf: 90, beh_conf: 20, hygiene: 100, level: 'LOW_TRUST' },
  { id: '2', user: 'sarah.connor', composite: 92.5, auth_conf: 100, beh_conf: 95, hygiene: 85, level: 'HIGH_TRUST' },
  { id: '3', user: 'service.build', composite: 98.0, auth_conf: 100, beh_conf: 98, hygiene: 100, level: 'HIGH_TRUST' }
];

export default function AdaptiveTrustDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ATS_STYLES}</style>
      <div className="ats-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ats-header-icon"><ShieldCheck size={24} /></div>
          <div>
            <h1 className="ats-title">Adaptive Trust Scoring</h1>
            <p className="ats-subtitle">Dynamic identity trust evaluation based on Zero Trust readiness</p>
          </div>
        </div>
        <Link to="/identity-intel" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Intelligence Dashboard</Link>
      </div>

      <div className="ats-card">
        <h3 className="ats-card-title"><ShieldAlert size={16} /> Current Trust Scores</h3>
        <table className="ats-table">
          <thead>
            <tr><th>Identity</th><th>Composite Trust Score (0-100)</th><th>Auth Confidence</th><th>Behavior Confidence</th><th>Hygiene</th><th>Trust Level</th></tr>
          </thead>
          <tbody>
            {TRUST_SCORES.map(score => (
              <tr key={score.id} className="ats-row">
                <td style={{ fontWeight: 600 }}>{score.user}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div className="ats-bar-bg">
                      <div className="ats-bar-fill" style={{ width: `${score.composite}%`, background: score.composite < 50 ? '#ef4444' : score.composite < 80 ? '#f59e0b' : '#10b981' }}></div>
                    </div>
                    <span style={{ fontWeight: 700 }}>{score.composite.toFixed(1)}</span>
                  </div>
                </td>
                <td style={{ color: '#94a3b8' }}>{score.auth_conf}%</td>
                <td style={{ color: '#94a3b8' }}>{score.beh_conf}%</td>
                <td style={{ color: '#94a3b8' }}>{score.hygiene}%</td>
                <td>
                  <span className={`ats-status ats-${score.level.toLowerCase()}`}>
                    {score.level.replace('_', ' ')}
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

const ATS_STYLES = `
.ats-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ats-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ats-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ats-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ats-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.ats-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.ats-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.ats-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.ats-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.ats-row td { padding: 12px; }
.ats-bar-bg { flex: 1; max-width: 120px; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; }
.ats-bar-fill { height: 100%; border-radius: 3px; }
.ats-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.ats-high_trust { background: rgba(16,185,129,0.15); color: #34d399; }
.ats-medium_trust { background: rgba(245,158,11,0.15); color: #fbbf24; }
.ats-low_trust { background: rgba(239,68,68,0.2); color: #fca5a5; }
.ats-zero_trust { background: rgba(255,255,255,0.1); color: #cbd5e1; }
`;
