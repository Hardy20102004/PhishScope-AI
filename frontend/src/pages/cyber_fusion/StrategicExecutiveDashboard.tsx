import React from 'react';
import { Link } from 'react-router-dom';
import { Eye, TrendingDown, CheckCircle, Presentation } from 'lucide-react';

const EXECUTIVE_METRICS = {
  enterprise_risk_index: '24 (Low)',
  yoy_risk_reduction: '-42%',
  open_critical_findings: 1,
  ai_governance_automation: '88%'
};

export default function StrategicExecutiveDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{SED_STYLES}</style>
      <div className="sed-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="sed-header-icon"><Eye size={24} /></div>
          <div>
            <h1 className="sed-title">Strategic Executive View</h1>
            <p className="sed-subtitle">C-Level Board reporting for Enterprise Cyber Fusion & Defense</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <button className="sed-btn"><Presentation size={14} /> Board Presentation Mode</button>
          <Link to="/cyber-fusion" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem', display: 'flex', alignItems: 'center' }}>← Back</Link>
        </div>
      </div>

      <div className="sed-grid">
        <div className="sed-card">
          <h3 className="sed-card-title">Enterprise Risk Index (0-100)</h3>
          <span style={{ fontSize: '2.5rem', fontWeight: 800, color: '#10b981' }}>{EXECUTIVE_METRICS.enterprise_risk_index}</span>
        </div>
        <div className="sed-card">
          <h3 className="sed-card-title">YoY Risk Reduction</h3>
          <span style={{ fontSize: '2.5rem', fontWeight: 800, color: '#3b82f6' }}>{EXECUTIVE_METRICS.yoy_risk_reduction}</span>
        </div>
        <div className="sed-card">
          <h3 className="sed-card-title">Open Critical Findings</h3>
          <span style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ef4444' }}>{EXECUTIVE_METRICS.open_critical_findings}</span>
        </div>
        <div className="sed-card">
          <h3 className="sed-card-title">AI Governance Automation</h3>
          <span style={{ fontSize: '2.5rem', fontWeight: 800, color: '#8b5cf6' }}>{EXECUTIVE_METRICS.ai_governance_automation}</span>
        </div>
      </div>
      
      <div className="sed-card" style={{ marginTop: 24 }}>
        <h3 className="sed-card-title"><CheckCircle size={16} color="#10b981" /> Quarterly Cyber Operations Summary</h3>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.6 }}>
          In Q3, the Cyber Fusion Center successfully correlated and neutralized 12 advanced cross-domain threat chains before they reached data exfiltration stages. Our Enterprise Risk Index dropped by 42% year-over-year, largely driven by the full deployment of the Identity Command Center and the AI-driven Zero Trust continuous validation engines. 88% of standard tier-1 SOC and IAM governance approvals are now fully AI-assisted.
        </p>
      </div>
    </div>
  );
}

const SED_STYLES = `
.sed-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
.sed-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #475569, #1e293b); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.sed-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.sed-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.sed-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; }
.sed-btn:hover { background: rgba(255,255,255,0.1); }
.sed-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.sed-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 32px; text-align: center; }
.sed-card-title { font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; display: flex; align-items: center; justify-content: center; gap: 8px; }
@media (max-width: 1024px) { .sed-grid { grid-template-columns: 1fr 1fr; } }
`;
