import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Activity, Lock, Search, Filter, Server, Users, Key, AlertTriangle, Eye, ArrowRight, TrendingUp, CheckCircle, Smartphone } from 'lucide-react';

const ZTA_DATA = {
  verifications_today: 125430,
  failed_verifications: 420,
  adaptive_challenges: 1250,
  sessions_revoked: 14,
  maturity_score: 68.5,
  maturity_level: 'ADVANCED',
  top_risks: [
    { type: 'Device', issue: 'Unmanaged devices accessing critical apps', severity: 'HIGH', count: 184 },
    { type: 'Identity', issue: 'Failed continuous verification due to anomalous location', severity: 'MEDIUM', count: 86 },
    { type: 'Session', issue: 'Session hijacked suspicion (MITRE T1185)', severity: 'CRITICAL', count: 4 }
  ],
  verifications_by_type: { IDENTITY: 45000, DEVICE: 42000, NETWORK: 20000, SESSION: 18430 }
};

export default function ZTADashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ZTA_STYLES}</style>
      
      {/* Header */}
      <div className="zta-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="zta-header-icon"><Shield size={24} /></div>
          <div>
            <h1 className="zta-title">Zero Trust Architecture</h1>
            <p className="zta-subtitle">Continuous Verification · Adaptive Access · Context Evaluation</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/zta/verify" className="zta-btn"><Activity size={14} /> Verification Logs</Link>
          <Link to="/zta/access" className="zta-btn"><Lock size={14} /> Access Decisions</Link>
          <Link to="/zta/assistant" className="zta-btn zta-btn-ai">Ask AI Assistant</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="zta-grid-4">
        {[
          { label: 'Verifications Today', value: ZTA_DATA.verifications_today.toLocaleString(), color: '#6366f1' },
          { label: 'Failed Verifications', value: ZTA_DATA.failed_verifications.toLocaleString(), color: '#ef4444' },
          { label: 'Adaptive Challenges', value: ZTA_DATA.adaptive_challenges.toLocaleString(), color: '#f59e0b' },
          { label: 'Sessions Revoked', value: ZTA_DATA.sessions_revoked.toLocaleString(), color: '#10b981' }
        ].map(k => (
          <div key={k.label} className="zta-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '2rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="zta-main-layout">
        <div className="zta-left-col">
          {/* Verification Types */}
          <div className="zta-card">
            <h3 className="zta-card-title"><Activity size={16} /> Continuous Verifications by Context</h3>
            <div className="zta-v-bars">
              {Object.entries(ZTA_DATA.verifications_by_type).map(([type, count]) => {
                const colors: any = { IDENTITY: '#6366f1', DEVICE: '#8b5cf6', NETWORK: '#06b6d4', SESSION: '#10b981' };
                const pct = (count / ZTA_DATA.verifications_today) * 100;
                return (
                  <div key={type} className="zta-v-bar-row">
                    <div className="zta-v-label">{type}</div>
                    <div className="zta-v-track">
                      <div className="zta-v-fill" style={{ width: `${pct}%`, background: colors[type] }} />
                    </div>
                    <div className="zta-v-value">{count.toLocaleString()}</div>
                  </div>
                );
              })}
            </div>
          </div>
          
          {/* Top Risks */}
          <div className="zta-card">
            <h3 className="zta-card-title"><AlertTriangle size={16} /> Top Risk Factors Triggering Denials</h3>
            <div className="zta-risk-list">
              {ZTA_DATA.top_risks.map((risk, i) => (
                <div key={i} className="zta-risk-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{risk.type} Risk</strong>
                    <span className="zta-risk-badge" style={{ 
                      color: risk.severity === 'CRITICAL' ? '#f87171' : risk.severity === 'HIGH' ? '#fbbf24' : '#60a5fa',
                      background: risk.severity === 'CRITICAL' ? 'rgba(239,68,68,0.15)' : risk.severity === 'HIGH' ? 'rgba(245,158,11,0.15)' : 'rgba(59,130,246,0.15)'
                    }}>{risk.severity}</span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.8rem', color: '#94a3b8' }}>{risk.issue}</p>
                  <p style={{ margin: '4px 0 0', fontSize: '0.75rem', color: '#64748b' }}>{risk.count} occurrences today</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="zta-right-col">
          {/* ZTA Maturity */}
          <div className="zta-card zta-card-center">
            <h3 className="zta-card-title" style={{ alignSelf: 'flex-start' }}><TrendingUp size={16} /> Maturity Score</h3>
            <div className="zta-score-ring">
              <span style={{ fontSize: '3rem', fontWeight: 800, color: '#6366f1' }}>{ZTA_DATA.maturity_score}</span>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>/ 100</span>
            </div>
            <div className="zta-maturity-badge">{ZTA_DATA.maturity_level}</div>
            <p style={{ textAlign: 'center', fontSize: '0.8rem', color: '#64748b', marginTop: 12 }}>Continuous verification and adaptive policies are actively enforcing least privilege.</p>
          </div>
          
          {/* Quick Actions */}
          <div className="zta-card">
            <h3 className="zta-card-title">Zero Trust Modules</h3>
            <div className="zta-module-links">
              <Link to="/zta/verify" className="zta-mod-link"><Activity size={16} /> Continuous Verification</Link>
              <Link to="/zta/access" className="zta-mod-link"><Lock size={16} /> Adaptive Access</Link>
              <Link to="/zta/policies" className="zta-mod-link"><Shield size={16} /> Policy Governance</Link>
              <Link to="/zta/sessions" className="zta-mod-link"><Server size={16} /> Session Intelligence</Link>
              <Link to="/zta/risk" className="zta-mod-link"><AlertTriangle size={16} /> Contextual Risk</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const ZTA_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.zta-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.zta-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.zta-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.zta-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.zta-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.zta-btn:hover { background: rgba(255,255,255,0.1); }
.zta-btn-ai { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.3); color: #818cf8; }
.zta-grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 16px; }
.zta-kpi-card { display: flex; flex-direction: column; padding: 20px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.zta-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .zta-main-layout { grid-template-columns: 1fr; } }
.zta-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.zta-card-center { display: flex; flex-direction: column; align-items: center; justify-content: center; }
.zta-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.zta-v-bars { display: flex; flex-direction: column; gap: 12px; }
.zta-v-bar-row { display: flex; align-items: center; gap: 12px; }
.zta-v-label { width: 80px; font-size: 0.75rem; color: #94a3b8; font-weight: 500; }
.zta-v-track { flex: 1; height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden; }
.zta-v-fill { height: 100%; border-radius: 4px; transition: width 0.8s; }
.zta-v-value { width: 50px; text-align: right; font-size: 0.75rem; color: #e2e8f0; font-weight: 600; }
.zta-risk-list { display: flex; flex-direction: column; gap: 10px; }
.zta-risk-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; }
.zta-risk-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.zta-score-ring { width: 140px; height: 140px; border-radius: 50%; border: 8px solid rgba(99,102,241,0.2); border-top-color: #6366f1; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 16px; }
.zta-maturity-badge { background: rgba(99,102,241,0.1); color: #818cf8; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(99,102,241,0.2); }
.zta-module-links { display: flex; flex-direction: column; gap: 8px; }
.zta-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.zta-mod-link:hover { background: rgba(99,102,241,0.1); border-color: rgba(99,102,241,0.3); color: #fff; }
`;
