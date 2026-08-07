import React from 'react';
import { Link } from 'react-router-dom';
import { Key, Clock, ShieldAlert, FileText, CheckCircle, Search, Users, Shield, Server, TrendingDown } from 'lucide-react';

const PAM_DATA = {
  total_privileged_identities: 142,
  standing_privileges: 45,
  jit_adoption_rate: 68.3,
  active_admin_sessions: 12,
  overdue_rotations: 3,
  pam_maturity_score: 78,
  pam_maturity_level: 'OPTIMIZED',
  top_risks: [
    { type: 'Standing Access', issue: 'AWS Prod Admin Role has no recent usage', severity: 'HIGH', count: 14 },
    { type: 'Credential', issue: 'Service account keys overdue for rotation', severity: 'MEDIUM', count: 3 },
    { type: 'Session', issue: 'Anomalous velocity detected for global admin', severity: 'CRITICAL', count: 1 }
  ]
};

export default function PAMDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PAM_STYLES}</style>
      
      {/* Header */}
      <div className="pam-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="pam-header-icon"><Key size={24} /></div>
          <div>
            <h1 className="pam-title">Privileged Access Management (PAM)</h1>
            <p className="pam-subtitle">JIT Elevation · Credential Governance · Session Oversight</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/pam/jit" className="pam-btn"><Clock size={14} /> Request JIT Access</Link>
          <Link to="/pam/assistant" className="pam-btn pam-btn-ai">Ask AI Assistant</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="pam-grid-4">
        {[
          { label: 'Privileged Identities', value: PAM_DATA.total_privileged_identities, color: '#6366f1' },
          { label: 'Standing Privileges', value: PAM_DATA.standing_privileges, color: '#ef4444' },
          { label: 'JIT Adoption Rate', value: `${PAM_DATA.jit_adoption_rate}%`, color: '#10b981' },
          { label: 'Active Admin Sessions', value: PAM_DATA.active_admin_sessions, color: '#f59e0b' }
        ].map(k => (
          <div key={k.label} className="pam-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '2rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="pam-main-layout">
        <div className="pam-left-col">
          {/* Top Risks */}
          <div className="pam-card">
            <h3 className="pam-card-title"><ShieldAlert size={16} /> Top Privilege Risks & Governance Gaps</h3>
            <div className="pam-risk-list">
              {PAM_DATA.top_risks.map((risk, i) => (
                <div key={i} className="pam-risk-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{risk.type} Risk</strong>
                    <span className={`pam-risk-badge pam-risk-${risk.severity.toLowerCase()}`}>{risk.severity}</span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.8rem', color: '#94a3b8' }}>{risk.issue}</p>
                  <p style={{ margin: '4px 0 0', fontSize: '0.75rem', color: '#64748b' }}>{risk.count} affected entities</p>
                </div>
              ))}
            </div>
          </div>
          
          <div className="pam-card">
            <h3 className="pam-card-title"><TrendingDown size={16} /> JIT Migration Progress</h3>
            <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: '0 0 12px' }}>Transitioning standing access to ephemeral JIT approval workflows.</p>
            <div style={{ width: '100%', height: 12, background: 'rgba(255,255,255,0.05)', borderRadius: 6, overflow: 'hidden' }}>
              <div style={{ width: `${PAM_DATA.jit_adoption_rate}%`, height: '100%', background: '#10b981' }} />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: '0.75rem', color: '#64748b' }}>
              <span>0%</span>
              <span>Target: 95%</span>
            </div>
          </div>
        </div>
        
        <div className="pam-right-col">
          {/* Maturity */}
          <div className="pam-card pam-card-center">
            <h3 className="pam-card-title" style={{ alignSelf: 'flex-start' }}><CheckCircle size={16} /> PAM Maturity</h3>
            <div className="pam-score-ring">
              <span style={{ fontSize: '3rem', fontWeight: 800, color: '#8b5cf6' }}>{PAM_DATA.pam_maturity_score}</span>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>/ 100</span>
            </div>
            <div className="pam-maturity-badge">{PAM_DATA.pam_maturity_level}</div>
          </div>
          
          {/* Quick Actions */}
          <div className="pam-card">
            <h3 className="pam-card-title">PAM Modules</h3>
            <div className="pam-module-links">
              <Link to="/pam/identities" className="pam-mod-link"><Users size={16} /> Privileged Identities</Link>
              <Link to="/pam/jit" className="pam-mod-link"><Clock size={16} /> JIT Access Workflows</Link>
              <Link to="/pam/sessions" className="pam-mod-link"><Server size={16} /> Session Governance</Link>
              <Link to="/pam/credentials" className="pam-mod-link"><Key size={16} /> Credential Governance</Link>
              <Link to="/pam/risk" className="pam-mod-link"><ShieldAlert size={16} /> Privilege Risk Scores</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const PAM_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.pam-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.pam-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.pam-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.pam-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.pam-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.pam-btn:hover { background: rgba(255,255,255,0.1); }
.pam-btn-ai { background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.3); color: #34d399; }
.pam-grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 16px; }
.pam-kpi-card { display: flex; flex-direction: column; padding: 20px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.pam-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .pam-main-layout { grid-template-columns: 1fr; } }
.pam-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.pam-card-center { display: flex; flex-direction: column; align-items: center; justify-content: center; }
.pam-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.pam-risk-list { display: flex; flex-direction: column; gap: 10px; }
.pam-risk-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; }
.pam-risk-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.pam-risk-critical { color: #f87171; background: rgba(239,68,68,0.15); }
.pam-risk-high { color: #fbbf24; background: rgba(245,158,11,0.15); }
.pam-risk-medium { color: #60a5fa; background: rgba(59,130,246,0.15); }
.pam-score-ring { width: 140px; height: 140px; border-radius: 50%; border: 8px solid rgba(139,92,246,0.2); border-top-color: #8b5cf6; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 16px; }
.pam-maturity-badge { background: rgba(139,92,246,0.1); color: #a78bfa; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(139,92,246,0.2); }
.pam-module-links { display: flex; flex-direction: column; gap: 8px; }
.pam-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.pam-mod-link:hover { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.3); color: #fff; }
`;
