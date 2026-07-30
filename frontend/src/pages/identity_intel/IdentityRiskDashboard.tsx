import React from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, Activity } from 'lucide-react';

const RISKS = [
  { id: '1', user: 'david.smith (Admin)', overall: 88, priv_risk: 95, op_risk: 20, level: 'CRITICAL', trend: '+12%' },
  { id: '2', user: 'contractors_grp', overall: 65, priv_risk: 30, op_risk: 80, level: 'HIGH', trend: '-5%' },
  { id: '3', user: 'sarah.connor', overall: 15, priv_risk: 10, op_risk: 10, level: 'LOW', trend: 'Stable' }
];

export default function IdentityRiskDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{RISK_STYLES}</style>
      <div className="risk-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="risk-header-icon"><AlertTriangle size={24} /></div>
          <div>
            <h1 className="risk-title">Identity Risk Analytics</h1>
            <p className="risk-subtitle">Continuous quantification of identity and privilege risk</p>
          </div>
        </div>
        <Link to="/identity-intel" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Intelligence Dashboard</Link>
      </div>

      <div className="risk-card">
        <h3 className="risk-card-title"><Activity size={16} /> Identity Risk Profiles</h3>
        <table className="risk-table">
          <thead>
            <tr><th>Identity / Group</th><th>Overall Risk (0-100)</th><th>Privilege Risk</th><th>Operational Risk</th><th>Trend (30d)</th><th>Risk Level</th></tr>
          </thead>
          <tbody>
            {RISKS.map(risk => (
              <tr key={risk.id} className="risk-row">
                <td style={{ fontWeight: 600 }}>{risk.user}</td>
                <td style={{ fontWeight: 700, color: risk.overall > 75 ? '#ef4444' : risk.overall > 50 ? '#f59e0b' : '#10b981' }}>
                  {risk.overall}
                </td>
                <td style={{ color: '#94a3b8' }}>{risk.priv_risk}</td>
                <td style={{ color: '#94a3b8' }}>{risk.op_risk}</td>
                <td style={{ color: risk.trend.includes('+') ? '#ef4444' : risk.trend.includes('-') ? '#10b981' : '#cbd5e1' }}>
                  {risk.trend}
                </td>
                <td>
                  <span className={`risk-status risk-${risk.level.toLowerCase()}`}>
                    {risk.level}
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

const RISK_STYLES = `
.risk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.risk-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.risk-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.risk-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.risk-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.risk-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.risk-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.risk-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.risk-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.risk-row td { padding: 12px; }
.risk-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.risk-critical { background: rgba(239,68,68,0.2); color: #fca5a5; }
.risk-high { background: rgba(249,115,22,0.2); color: #fdba74; }
.risk-medium { background: rgba(234,179,8,0.2); color: #fde047; }
.risk-low { background: rgba(16,185,129,0.15); color: #34d399; }
`;
