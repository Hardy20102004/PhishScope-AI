import React from 'react';
import { Link } from 'react-router-dom';
import { Target, Activity, ShieldAlert, Crosshair, Map, ShieldX, TrendingUp, Search } from 'lucide-react';

const ITDR_DATA = {
  active_credential_attacks: 3,
  identities_at_risk: 12,
  open_investigations: 5,
  telemetry_events_24h: 145000,
  behavior_anomalies_detected: 42,
  recent_threats: [
    { id: '1', type: 'PASSWORD_SPRAY', target: 'VPN Gateway', severity: 'CRITICAL', status: 'ACTIVE', time: '10 mins ago' },
    { id: '2', type: 'IMPOSSIBLE_TRAVEL', target: 'alice.security', severity: 'HIGH', status: 'MITIGATED', time: '2 hours ago' },
    { id: '3', type: 'MFA_FATIGUE', target: 'bob.devops', severity: 'HIGH', status: 'INVESTIGATING', time: '4 hours ago' }
  ]
};

export default function ITDRDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ITDR_STYLES}</style>
      
      {/* Header */}
      <div className="itdr-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="itdr-header-icon"><Target size={24} /></div>
          <div>
            <h1 className="itdr-title">Identity Threat Detection & Response (ITDR)</h1>
            <p className="itdr-subtitle">Behavioral Intelligence · Credential Attack Defense · Response Automation</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/itdr/investigations" className="itdr-btn"><Search size={14} /> View Investigations</Link>
          <Link to="/itdr/assistant" className="itdr-btn itdr-btn-ai">Ask ITDR AI</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="itdr-grid-5">
        {[
          { label: 'Active Credential Attacks', value: ITDR_DATA.active_credential_attacks, color: '#ef4444' },
          { label: 'Identities at Risk', value: ITDR_DATA.identities_at_risk, color: '#f97316' },
          { label: 'Behavior Anomalies (24h)', value: ITDR_DATA.behavior_anomalies_detected, color: '#f59e0b' },
          { label: 'Open Investigations', value: ITDR_DATA.open_investigations, color: '#8b5cf6' },
          { label: 'Telemetry Events (24h)', value: (ITDR_DATA.telemetry_events_24h / 1000) + 'k', color: '#3b82f6' }
        ].map(k => (
          <div key={k.label} className="itdr-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="itdr-main-layout">
        <div className="itdr-left-col">
          {/* Recent Threats */}
          <div className="itdr-card">
            <h3 className="itdr-card-title"><ShieldAlert size={16} /> Live Threat Feed</h3>
            <div className="itdr-threat-list">
              {ITDR_DATA.recent_threats.map((threat) => (
                <div key={threat.id} className="itdr-threat-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{threat.type.replace('_', ' ')}</strong>
                    <span className={`itdr-threat-badge itdr-threat-${threat.severity.toLowerCase()}`}>{threat.severity}</span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.8rem', color: '#94a3b8' }}>Target: {threat.target}</p>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
                    <span style={{ fontSize: '0.7rem', color: '#64748b' }}>{threat.time}</span>
                    <span style={{ fontSize: '0.7rem', fontWeight: 600, color: threat.status === 'ACTIVE' ? '#ef4444' : '#10b981' }}>{threat.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="itdr-right-col">
          {/* Quick Actions / Navigation */}
          <div className="itdr-card">
            <h3 className="itdr-card-title">ITDR Modules</h3>
            <div className="itdr-module-links">
              <Link to="/itdr/timeline" className="itdr-mod-link"><Activity size={16} /> Identity Timeline</Link>
              <Link to="/itdr/behavior" className="itdr-mod-link"><Map size={16} /> Behavioral Analytics</Link>
              <Link to="/itdr/credentials" className="itdr-mod-link"><Crosshair size={16} /> Credential Defense</Link>
              <Link to="/itdr/investigations" className="itdr-mod-link"><Search size={16} /> Investigations</Link>
              <Link to="/itdr/risk" className="itdr-mod-link"><TrendingUp size={16} /> Identity Risk</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const ITDR_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.itdr-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.itdr-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.itdr-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.itdr-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.itdr-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.itdr-btn:hover { background: rgba(255,255,255,0.1); }
.itdr-btn-ai { background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.3); color: #fca5a5; }
.itdr-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 16px; }
.itdr-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.itdr-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .itdr-main-layout { grid-template-columns: 1fr; } }
.itdr-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.itdr-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.itdr-threat-list { display: flex; flex-direction: column; gap: 10px; }
.itdr-threat-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; border-left: 3px solid transparent; transition: all 0.2s; }
.itdr-threat-item:hover { background: rgba(255,255,255,0.04); }
.itdr-threat-item:has(.itdr-threat-critical) { border-left-color: #ef4444; }
.itdr-threat-item:has(.itdr-threat-high) { border-left-color: #f97316; }
.itdr-threat-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.itdr-threat-critical { color: #fca5a5; background: rgba(239,68,68,0.2); }
.itdr-threat-high { color: #fdba74; background: rgba(249,115,22,0.2); }
.itdr-module-links { display: flex; flex-direction: column; gap: 8px; }
.itdr-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.itdr-mod-link:hover { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.3); color: #fff; }
`;
