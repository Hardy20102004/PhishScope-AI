import React from 'react';
import { Link } from 'react-router-dom';
import { Eye, TrendingUp, CheckCircle, Presentation } from 'lucide-react';

const BOARD_METRICS = {
  overall_posture: 'A-',
  yoy_improvement: '+14%',
  compliance_readiness: '100%',
  critical_incidents: 0
};

export default function BoardReportingDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{BRD_STYLES}</style>
      <div className="brd-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="brd-header-icon"><Eye size={24} /></div>
          <div>
            <h1 className="brd-title">Board Reporting & Strategic View</h1>
            <p className="brd-subtitle">Quarterly presentation-ready metrics for executive leadership</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <button className="brd-btn"><Presentation size={14} /> Enter Presentation Mode</button>
          <Link to="/identity-cc" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem', display: 'flex', alignItems: 'center' }}>← Back</Link>
        </div>
      </div>

      <div className="brd-grid">
        <div className="brd-card">
          <h3 className="brd-card-title">Enterprise Security Posture Grade</h3>
          <span style={{ fontSize: '3rem', fontWeight: 800, color: '#10b981' }}>{BOARD_METRICS.overall_posture}</span>
        </div>
        <div className="brd-card">
          <h3 className="brd-card-title">YoY Posture Improvement</h3>
          <span style={{ fontSize: '3rem', fontWeight: 800, color: '#3b82f6' }}>{BOARD_METRICS.yoy_improvement}</span>
        </div>
        <div className="brd-card">
          <h3 className="brd-card-title">Compliance Audit Readiness</h3>
          <span style={{ fontSize: '3rem', fontWeight: 800, color: '#8b5cf6' }}>{BOARD_METRICS.compliance_readiness}</span>
        </div>
        <div className="brd-card">
          <h3 className="brd-card-title">Critical Identity Incidents (Q3)</h3>
          <span style={{ fontSize: '3rem', fontWeight: 800, color: '#10b981' }}>{BOARD_METRICS.critical_incidents}</span>
        </div>
      </div>
      
      <div className="brd-card" style={{ marginTop: 24 }}>
        <h3 className="brd-card-title"><CheckCircle size={16} color="#10b981" /> Strategic Roadmap Delivery</h3>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.6 }}>
          In Q3, the Enterprise Identity Security Command Center successfully achieved 100% continuous validation across all tier-1 applications. We fully rolled out Passwordless (FIDO2) authentication to the engineering organization and migrated legacy federated trusts to modern OIDC pipelines. Standing privileges in AWS have been eliminated, replaced by JIT provisioning governed by the Command Center.
        </p>
      </div>
    </div>
  );
}

const BRD_STYLES = `
.brd-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
.brd-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #475569, #1e293b); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.brd-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.brd-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.brd-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; }
.brd-btn:hover { background: rgba(255,255,255,0.1); }
.brd-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.brd-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 32px; text-align: center; }
.brd-card-title { font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; display: flex; align-items: center; justify-content: center; gap: 8px; }
@media (max-width: 1024px) { .brd-grid { grid-template-columns: 1fr 1fr; } }
`;
