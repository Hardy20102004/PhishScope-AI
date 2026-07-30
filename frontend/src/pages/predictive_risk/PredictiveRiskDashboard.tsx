import React from 'react';
import { Link } from 'react-router-dom';
import { LineChart, BarChart2, Briefcase, TrendingDown, Sparkles } from 'lucide-react';

const RISK_METRICS = {
  current_enterprise_risk: 42,
  forecasted_risk_q3: 31,
  strategic_plans_active: 3,
  investment_scenarios: 5
};

export default function PredictiveRiskDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PRD_STYLES}</style>
      
      {/* Header */}
      <div className="prd-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="prd-header-icon"><LineChart size={24} /></div>
          <div>
            <h1 className="prd-title">Predictive Cyber Risk & Strategy</h1>
            <p className="prd-subtitle">Executive forecasting and human-governed strategic planning</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/predictive-risk/assistant" className="prd-btn prd-btn-ai"><Sparkles size={14} /> AI Strategy Copilot</Link>
          <button className="prd-btn"><Briefcase size={14} /> Board Presentation Mode</button>
        </div>
      </div>

      {/* KPI Row */}
      <div className="prd-grid-4">
        {[
          { label: 'Current Enterprise Risk Score', value: RISK_METRICS.current_enterprise_risk, color: '#f59e0b', suffix: '' },
          { label: 'Forecasted Risk (Q3 Proj.)', value: RISK_METRICS.forecasted_risk_q3, color: '#10b981', suffix: '' },
          { label: 'Active Strategic Plans', value: RISK_METRICS.strategic_plans_active, color: '#3b82f6', suffix: '' },
          { label: 'Modeled Investment Scenarios', value: RISK_METRICS.investment_scenarios, color: '#8b5cf6', suffix: '' }
        ].map(k => (
          <div key={k.label} className="prd-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.6rem', fontWeight: 800, color: k.color }}>{k.value}{k.suffix}</span>
            <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      {/* Navigation Modules */}
      <div className="prd-main-layout">
        <div className="prd-modules-grid">
          <ModuleCard title="Executive Risk Forecast" icon={<LineChart />} link="/predictive-risk/forecasts" desc="Quarterly and annual risk projections with confidence intervals." color="#f59e0b" />
          <ModuleCard title="Investment Prioritization" icon={<BarChart2 />} link="/predictive-risk/investments" desc="Budget allocation modeling against forecasted risk reduction." color="#10b981" />
          <ModuleCard title="Strategic Roadmap" icon={<Briefcase />} link="/predictive-risk/plans" desc="Long-term capability maturity goals and operational planning." color="#3b82f6" />
          <ModuleCard title="Resilience Projections" icon={<TrendingDown />} link="/predictive-risk/resilience" desc="Forward-looking operational resilience assessments." color="#8b5cf6" />
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ title, icon, link, desc, color }: any) {
  return (
    <Link to={link} className="prd-mod-card" style={{ '--mod-color': color } as React.CSSProperties}>
      <div className="prd-mod-icon" style={{ color }}>{icon}</div>
      <div className="prd-mod-content">
        <h3 className="prd-mod-title">{title}</h3>
        <p className="prd-mod-desc">{desc}</p>
      </div>
    </Link>
  );
}

const PRD_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.prd-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.prd-header-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #10b981, #059669); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.prd-title { font-size: 1.45rem; font-weight: 800; margin: 0 0 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.prd-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.prd-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; cursor: pointer; transition: all 0.2s; }
.prd-btn:hover { background: rgba(255,255,255,0.1); }
.prd-btn-ai { background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.3); color: #34d399; }
.prd-grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }
.prd-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.prd-modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.prd-mod-card { display: flex; align-items: flex-start; gap: 16px; padding: 20px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; text-decoration: none; transition: all 0.2s; }
.prd-mod-card:hover { background: rgba(255,255,255,0.04); border-color: var(--mod-color); transform: translateY(-2px); }
.prd-mod-icon { padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; }
.prd-mod-content { flex: 1; }
.prd-mod-title { margin: 0 0 4px; font-size: 0.95rem; font-weight: 700; color: #f8fafc; }
.prd-mod-desc { margin: 0; font-size: 0.75rem; color: #94a3b8; line-height: 1.4; }
`;
