import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, TrendingUp, TrendingDown, AlertTriangle, BarChart3 } from 'lucide-react';

const RISK_DATA = {
  distribution: { CRITICAL: 23, HIGH: 89, MEDIUM: 201, LOW: 534 },
  average_score: 31.7,
  top_risks: [
    { name: 'orphaned-svc-legacy', score: 94.1, level: 'CRITICAL', type: 'SERVICE_ACCOUNT', trend: 'WORSENING', factors: ['Orphaned identity', 'No MFA', 'Privileged access', 'Inactive 241 days'] },
    { name: 'John Smith', score: 87.3, level: 'CRITICAL', type: 'HUMAN', trend: 'WORSENING', factors: ['Privileged account', 'No MFA', 'Admin sprawl', 'Password only'] },
    { name: 'svc-payroll-api', score: 72.1, level: 'HIGH', type: 'SERVICE_ACCOUNT', trend: 'STABLE', factors: ['No MFA', 'Excessive permissions', 'Privileged access'] },
    { name: 'David Chen', score: 65.8, level: 'HIGH', type: 'HUMAN', trend: 'WORSENING', factors: ['Dormant 90 days', 'Privileged account', 'Certification overdue'] },
    { name: 'machine-k8s-node-01', score: 42.5, level: 'MEDIUM', type: 'MACHINE', trend: 'STABLE', factors: ['No MFA', 'Workload identity risk'] },
    { name: 'app-oauth-github', score: 45.2, level: 'MEDIUM', type: 'APPLICATION', trend: 'IMPROVING', factors: ['Excess token permissions', 'OAuth scope drift'] },
  ],
  dimension_averages: { authentication: 38.4, privilege: 42.1, behavioral: 18.6, hygiene: 28.3, governance: 35.7, threat_intel: 6.2 }
};

const LEVEL_COLORS: Record<string, string> = { CRITICAL: '#ef4444', HIGH: '#f97316', MEDIUM: '#f59e0b', LOW: '#10b981' };
const TREND_ICONS: Record<string, React.ReactNode> = {
  WORSENING: <TrendingUp size={12} color="#ef4444" />,
  IMPROVING: <TrendingDown size={12} color="#10b981" />,
  STABLE: <span style={{ fontSize: '0.7rem', color: '#64748b' }}>→</span>
};

export default function IdentityRiskDashboard() {
  const total = Object.values(RISK_DATA.distribution).reduce((a, b) => a + b, 0);

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{RISK_STYLES}</style>
      <div className="risk-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="risk-icon"><ShieldAlert size={24} /></div>
          <div>
            <h1 className="risk-title">Identity Risk Dashboard</h1>
            <p className="risk-subtitle">Composite Risk Scores · Multi-Dimension Analysis · Explainable AI · MITRE ATT&CK Alignment</p>
          </div>
        </div>
        <Link to="/ispm" style={{ textDecoration: 'none', color: '#818cf8', fontSize: '0.82rem', fontWeight: 500, padding: '8px 14px', background: 'rgba(99,102,241,0.12)', borderRadius: 9, border: '1px solid rgba(99,102,241,0.3)' }}>← ISPM</Link>
      </div>

      <div className="risk-main-grid">
        {/* Distribution */}
        <div className="risk-dist-card">
          <h3><BarChart3 size={16} /> Risk Distribution</h3>
          <div className="risk-dist-avg">
            <span style={{ fontSize: '2.8rem', fontWeight: 800, color: '#f59e0b', lineHeight: 1 }}>{RISK_DATA.average_score.toFixed(1)}</span>
            <span style={{ fontSize: '0.78rem', color: '#64748b' }}>avg risk score</span>
          </div>
          {Object.entries(RISK_DATA.distribution).map(([level, count]) => (
            <div key={level} style={{ marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5, fontSize: '0.82rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: LEVEL_COLORS[level] }} />
                  <span style={{ color: '#94a3b8' }}>{level}</span>
                </div>
                <div style={{ display: 'flex', gap: 12 }}>
                  <span style={{ color: LEVEL_COLORS[level], fontWeight: 700 }}>{count}</span>
                  <span style={{ color: '#475569' }}>{((count / total) * 100).toFixed(1)}%</span>
                </div>
              </div>
              <div style={{ height: 8, background: 'rgba(255,255,255,0.07)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${(count / total) * 100}%`, height: '100%', background: LEVEL_COLORS[level], borderRadius: 4, transition: 'width 0.8s' }} />
              </div>
            </div>
          ))}
          <div style={{ marginTop: 16, paddingTop: 14, borderTop: '1px solid rgba(255,255,255,0.07)', display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#64748b' }}>
            <span>Total Identities</span>
            <strong style={{ color: '#e2e8f0' }}>{total.toLocaleString()}</strong>
          </div>
        </div>

        {/* Risk Dimensions */}
        <div className="risk-dim-card">
          <h3>Risk Dimensions (Average Scores)</h3>
          {Object.entries(RISK_DATA.dimension_averages).map(([dim, score]) => {
            const colors: Record<string, string> = { authentication: '#6366f1', privilege: '#ef4444', behavioral: '#f97316', hygiene: '#f59e0b', governance: '#8b5cf6', threat_intel: '#dc2626' };
            return (
              <div key={dim} style={{ marginBottom: 14 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 5 }}>
                  <span style={{ color: '#94a3b8', textTransform: 'capitalize' }}>{dim.replace('_', ' ')} Risk</span>
                  <span style={{ color: colors[dim], fontWeight: 700 }}>{score.toFixed(1)}</span>
                </div>
                <div style={{ height: 6, background: 'rgba(255,255,255,0.07)', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ width: `${score}%`, height: '100%', background: colors[dim], transition: 'width 0.8s' }} />
                </div>
              </div>
            );
          })}
          <div style={{ marginTop: 14, padding: '12px', background: 'rgba(239,68,68,0.06)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: 10, fontSize: '0.78rem', color: '#fca5a5' }}>
            <AlertTriangle size={13} style={{ display: 'inline', marginRight: 6 }} />
            Privilege and Authentication risk are primary drivers. MITRE T1078, T1110 exposure confirmed.
          </div>
        </div>
      </div>

      {/* High-Risk Identities */}
      <div className="risk-table-card">
        <h3><AlertTriangle size={16} /> Top Risk Identities</h3>
        <table className="risk-table">
          <thead><tr><th>Identity</th><th>Type</th><th>Risk Score</th><th>Level</th><th>Trend</th><th>Contributing Factors</th></tr></thead>
          <tbody>
            {RISK_DATA.top_risks.map(identity => (
              <tr key={identity.name} className="risk-row">
                <td><span style={{ color: '#e2e8f0', fontWeight: 500 }}>{identity.name}</span></td>
                <td><span className="risk-type-badge">{identity.type.replace('_', ' ')}</span></td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div style={{ width: 55, height: 6, background: 'rgba(255,255,255,0.07)', borderRadius: 3, overflow: 'hidden' }}>
                      <div style={{ width: `${identity.score}%`, height: '100%', background: LEVEL_COLORS[identity.level] }} />
                    </div>
                    <span style={{ color: LEVEL_COLORS[identity.level], fontWeight: 700, fontSize: '0.83rem' }}>{identity.score.toFixed(1)}</span>
                  </div>
                </td>
                <td>
                  <span style={{ display: 'inline-block', padding: '3px 9px', borderRadius: 6, border: `1px solid ${LEVEL_COLORS[identity.level]}40`, background: `${LEVEL_COLORS[identity.level]}18`, color: LEVEL_COLORS[identity.level], fontSize: '0.72rem', fontWeight: 700 }}>{identity.level}</span>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                    {TREND_ICONS[identity.trend]}
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{identity.trend}</span>
                  </div>
                </td>
                <td>
                  <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap' }}>
                    {identity.factors.slice(0, 2).map(f => (
                      <span key={f} style={{ padding: '2px 7px', borderRadius: 4, background: 'rgba(255,255,255,0.06)', color: '#94a3b8', fontSize: '0.68rem' }}>{f}</span>
                    ))}
                    {identity.factors.length > 2 && <span style={{ fontSize: '0.68rem', color: '#475569' }}>+{identity.factors.length - 2}</span>}
                  </div>
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.risk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; gap: 16px; flex-wrap: wrap; }
.risk-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #dc2626); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.risk-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin: 0 0 2px; }
.risk-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.risk-main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
@media (max-width: 900px) { .risk-main-grid { grid-template-columns: 1fr; } }
.risk-dist-card, .risk-dim-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; }
.risk-dist-card h3, .risk-dim-card h3 { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 18px; }
.risk-dist-avg { display: flex; flex-direction: column; align-items: flex-start; margin-bottom: 18px; }
.risk-table-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; }
.risk-table-card h3 { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.risk-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.risk-table th { color: #64748b; font-weight: 500; padding: 10px 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.07); font-size: 0.75rem; }
.risk-row { border-bottom: 1px solid rgba(255,255,255,0.04); }
.risk-row:hover { background: rgba(255,255,255,0.03); }
.risk-row td { padding: 11px 12px; vertical-align: middle; }
.risk-type-badge { padding: 3px 8px; border-radius: 5px; background: rgba(255,255,255,0.06); color: #64748b; font-size: 0.72rem; }
`;
