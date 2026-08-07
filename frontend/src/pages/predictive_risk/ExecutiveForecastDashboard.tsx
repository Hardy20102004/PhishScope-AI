import React from 'react';
import { Link } from 'react-router-dom';
import { LineChart, BarChart2, ShieldAlert } from 'lucide-react';

const FORECASTS = [
  { id: '1', domain: 'Cloud Security', q3_proj: 35, eoy_proj: 28, confidence: '92%' },
  { id: '2', domain: 'Identity & Access', q3_proj: 42, eoy_proj: 30, confidence: '88%' },
  { id: '3', domain: 'Endpoint Security', q3_proj: 25, eoy_proj: 22, confidence: '95%' }
];

export default function ExecutiveForecastDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{EXF_STYLES}</style>
      <div className="exf-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="exf-header-icon"><LineChart size={24} /></div>
          <div>
            <h1 className="exf-title">Executive Risk Forecast</h1>
            <p className="exf-subtitle">Quarterly and annual risk projections with confidence intervals</p>
          </div>
        </div>
        <Link to="/predictive-risk" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Strategic Planning Home</Link>
      </div>

      <div className="exf-card">
        <h3 className="exf-card-title"><ShieldAlert size={16} color="#f59e0b" /> Domain Risk Projections</h3>
        <table className="exf-table">
          <thead>
            <tr><th>Security Domain</th><th>Q3 Projected Risk</th><th>End-of-Year Risk Target</th><th>Model Confidence</th></tr>
          </thead>
          <tbody>
            {FORECASTS.map(f => (
              <tr key={f.id} className="exf-row">
                <td style={{ fontWeight: 600 }}>{f.domain}</td>
                <td><span className="exf-score">{f.q3_proj}</span></td>
                <td><span className="exf-score exf-target">{f.eoy_proj}</span></td>
                <td style={{ color: '#94a3b8' }}>{f.confidence}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const EXF_STYLES = `
.exf-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.exf-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.exf-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.exf-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.exf-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.exf-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.exf-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.exf-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.exf-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.exf-row td { padding: 12px; }
.exf-score { display: inline-block; padding: 2px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; }
.exf-target { background: rgba(16,185,129,0.15); color: #34d399; }
`;
