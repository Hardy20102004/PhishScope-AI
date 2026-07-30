import React from 'react';
import { Link } from 'react-router-dom';
import { BarChart2, DollarSign, TrendingDown } from 'lucide-react';

const SCENARIOS = [
  { id: '1', name: 'Zero Trust Network Rollout', budget: '$1.2M', risk_reduction: '18%', roi: 'HIGH' },
  { id: '2', name: 'PAM Cloud Migration', budget: '$800K', risk_reduction: '12%', roi: 'MEDIUM' }
];

export default function InvestmentPrioritizationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{INV_STYLES}</style>
      <div className="inv-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="inv-header-icon"><BarChart2 size={24} /></div>
          <div>
            <h1 className="inv-title">Investment Prioritization</h1>
            <p className="inv-subtitle">Budget allocation modeling against forecasted risk reduction</p>
          </div>
        </div>
        <Link to="/predictive-risk" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Strategic Planning Home</Link>
      </div>

      <div className="inv-card">
        <h3 className="inv-card-title"><DollarSign size={16} color="#10b981" /> ROI Analysis (Risk Reduction)</h3>
        <table className="inv-table">
          <thead>
            <tr><th>Initiative Scenario</th><th>Est. Budget</th><th>Forecasted Risk Reduction</th><th>ROI Tier</th></tr>
          </thead>
          <tbody>
            {SCENARIOS.map(s => (
              <tr key={s.id} className="inv-row">
                <td style={{ fontWeight: 600 }}>{s.name}</td>
                <td style={{ color: '#94a3b8' }}>{s.budget}</td>
                <td><span className="inv-score"><TrendingDown size={12} style={{marginRight: 4}}/>{s.risk_reduction}</span></td>
                <td>
                  <span className={`inv-status inv-${s.roi.toLowerCase()}`}>
                    {s.roi}
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

const INV_STYLES = `
.inv-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.inv-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.inv-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.inv-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.inv-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.inv-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.inv-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.inv-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.inv-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.inv-row td { padding: 12px; }
.inv-score { display: inline-flex; align-items: center; padding: 2px 8px; background: rgba(16,185,129,0.15); color: #34d399; border-radius: 4px; font-family: monospace; font-weight: bold; }
.inv-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.inv-high { background: rgba(16,185,129,0.15); color: #34d399; }
.inv-medium { background: rgba(245,158,11,0.15); color: #fbbf24; }
`;
