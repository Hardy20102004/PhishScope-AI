import React from 'react';
import { Link } from 'react-router-dom';
import { Briefcase, Target, ShieldCheck } from 'lucide-react';

const STRATEGIC_PLANS = [
  { id: '1', title: 'Global Identity Modernization', target_maturity: 4, status: 'APPROVED', date: '2027 Q1' },
  { id: '2', title: 'AI-Native SOC Transformation', target_maturity: 5, status: 'PROPOSED', date: '2028 Q2' }
];

export default function StrategicPlanningDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{STR_STYLES}</style>
      <div className="str-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="str-header-icon"><Briefcase size={24} /></div>
          <div>
            <h1 className="str-title">Strategic Roadmap</h1>
            <p className="str-subtitle">Long-term capability maturity goals and executive planning</p>
          </div>
        </div>
        <Link to="/predictive-risk" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Strategic Planning Home</Link>
      </div>

      <div className="str-card">
        <h3 className="str-card-title"><Target size={16} color="#3b82f6" /> Proposed & Active Strategic Initiatives</h3>
        <table className="str-table">
          <thead>
            <tr><th>Initiative Title</th><th>Target Capability Maturity</th><th>Governance Status</th><th>Target Date</th></tr>
          </thead>
          <tbody>
            {STRATEGIC_PLANS.map(p => (
              <tr key={p.id} className="str-row">
                <td style={{ fontWeight: 600 }}>{p.title}</td>
                <td>Level {p.target_maturity}</td>
                <td>
                  <span className={`str-status str-${p.status.toLowerCase()}`}>
                    {p.status === 'APPROVED' ? <ShieldCheck size={12} style={{marginRight:4}}/> : null}
                    {p.status}
                  </span>
                </td>
                <td style={{ color: '#94a3b8' }}>{p.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const STR_STYLES = `
.str-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.str-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.str-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.str-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.str-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.str-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.str-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.str-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.str-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.str-row td { padding: 12px; }
.str-status { display: inline-flex; align-items: center; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.str-approved { background: rgba(16,185,129,0.15); color: #34d399; }
.str-proposed { background: rgba(245,158,11,0.15); color: #fbbf24; }
`;
