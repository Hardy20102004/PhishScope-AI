import React from 'react';
import { Link } from 'react-router-dom';
import { BrainCircuit, Activity, ShieldCheck, AlertTriangle, Fingerprint, Bot } from 'lucide-react';

const INTEL_DATA = {
  avg_trust_score: 88.5,
  critical_risk_identities: 14,
  anomalous_behaviors_detected: 32,
  telemetry_events_processed: '1.45M',
  zero_trust_readiness: 'High',
  recent_anomalies: [
    { id: 'ANOM-001', user: 'david.smith (Admin)', detail: 'Unusual access time for AWS Prod', severity: 'CRITICAL', source: 'PAM' },
    { id: 'ANOM-002', user: 'sarah.connor', detail: 'Authentication from new geographical region', severity: 'HIGH', source: 'AUTHN' },
    { id: 'ANOM-003', user: 'service.build', detail: 'Volume spike in token requests', severity: 'MEDIUM', source: 'FEDERATION' }
  ]
};

export default function IdentityIntelDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{INTEL_STYLES}</style>
      
      {/* Header */}
      <div className="ii-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ii-header-icon"><BrainCircuit size={24} /></div>
          <div>
            <h1 className="ii-title">Identity Intelligence & Trust</h1>
            <p className="ii-subtitle">Correlate telemetry, map behavioral baselines, and calculate adaptive trust</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/identity-intel/assistant" className="ii-btn ii-btn-ai"><Bot size={14} /> Ask Intelligence AI</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="ii-grid-5">
        {[
          { label: 'Avg Identity Trust Score', value: INTEL_DATA.avg_trust_score, color: '#10b981' },
          { label: 'Events Analyzed (24h)', value: INTEL_DATA.telemetry_events_processed, color: '#3b82f6' },
          { label: 'Behavior Anomalies', value: INTEL_DATA.anomalous_behaviors_detected, color: '#f59e0b' },
          { label: 'Critical Risk Profiles', value: INTEL_DATA.critical_risk_identities, color: '#ef4444' },
          { label: 'Zero Trust Posture', value: INTEL_DATA.zero_trust_readiness, color: '#8b5cf6' }
        ].map(k => (
          <div key={k.label} className="ii-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="ii-main-layout">
        <div className="ii-left-col">
          {/* Recent Anomalies */}
          <div className="ii-card">
            <h3 className="ii-card-title"><AlertTriangle size={16} color="#f59e0b" /> Real-time Behavioral Anomalies</h3>
            <div className="ii-list">
              {INTEL_DATA.recent_anomalies.map((anom) => (
                <div key={anom.id} className="ii-list-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{anom.user}</strong>
                    <span className={`ii-badge ii-badge-${anom.severity.toLowerCase()}`}>{anom.severity}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#cbd5e1' }}>{anom.detail}</p>
                    <span style={{ fontSize: '0.7rem', color: '#64748b', fontWeight: 600 }}>{anom.source}</span>
                  </div>
                </div>
              ))}
            </div>
            <Link to="/identity-intel/behavior" style={{ display: 'block', textAlign: 'center', marginTop: 12, color: '#3b82f6', fontSize: '0.8rem', textDecoration: 'none' }}>Investigate Behavioral Baselines →</Link>
          </div>
        </div>
        
        <div className="ii-right-col">
          {/* Quick Actions / Navigation */}
          <div className="ii-card">
            <h3 className="ii-card-title">Intelligence Modules</h3>
            <div className="ii-module-links">
              <Link to="/identity-intel/behavior" className="ii-mod-link"><Activity size={16} /> Behavior Analytics</Link>
              <Link to="/identity-intel/trust" className="ii-mod-link"><ShieldCheck size={16} /> Adaptive Trust Scoring</Link>
              <Link to="/identity-intel/risk" className="ii-mod-link"><AlertTriangle size={16} /> Risk Analytics</Link>
              <Link to="/identity-intel/executive" className="ii-mod-link"><Fingerprint size={16} /> Executive Metrics</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const INTEL_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.ii-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.ii-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ii-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ii-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ii-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.ii-btn:hover { background: rgba(255,255,255,0.1); }
.ii-btn-ai { background: rgba(37,99,235,0.15); border-color: rgba(37,99,235,0.3); color: #93c5fd; }
.ii-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 16px; }
.ii-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.ii-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .ii-main-layout { grid-template-columns: 1fr; } }
.ii-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.ii-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.ii-list { display: flex; flex-direction: column; gap: 10px; }
.ii-list-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; transition: all 0.2s; }
.ii-list-item:hover { background: rgba(255,255,255,0.04); }
.ii-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.ii-badge-critical { color: #fca5a5; background: rgba(239,68,68,0.2); }
.ii-badge-high { color: #fdba74; background: rgba(249,115,22,0.2); }
.ii-badge-medium { color: #fde047; background: rgba(234,179,8,0.2); }
.ii-module-links { display: flex; flex-direction: column; gap: 8px; }
.ii-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.ii-mod-link:hover { background: rgba(37,99,235,0.1); border-color: rgba(37,99,235,0.3); color: #fff; }
`;
