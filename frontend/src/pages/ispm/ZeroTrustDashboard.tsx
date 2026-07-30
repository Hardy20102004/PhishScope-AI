import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Network, Shield, CheckCircle, XCircle, AlertTriangle, TrendingUp, ChevronRight } from 'lucide-react';

const ZT_DATA = {
  overall_zt_score: 42.8,
  maturity_level: 'INITIAL',
  pillars: {
    identity: 58.5, devices: 42.1, networks: 38.7,
    applications: 51.3, data: 34.2, infrastructure: 39.8, analytics: 48.6
  },
  criteria: {
    continuous_verification_enabled: false,
    least_privilege_enforced: false,
    mfa_everywhere: false,
    device_trust_required: false,
    session_risk_evaluated: false,
    privileged_access_workstations: false
  },
  gap_analysis: [
    { pillar: 'IDENTITY', score: 58.5, gap: 11.5, priority: 'HIGH', description: 'MFA coverage and phishing-resistant auth needs improvement' },
    { pillar: 'NETWORKS', score: 38.7, gap: 21.3, priority: 'HIGH', description: 'Micro-segmentation and least-privilege network access not enforced' },
    { pillar: 'DATA', score: 34.2, gap: 25.8, priority: 'CRITICAL', description: 'Data classification and access controls not fully implemented' },
  ],
  roadmap: [
    { phase: 1, timeline: '0-30 days', title: 'Identity Verification Baseline', actions: ['Enforce MFA for all privileged accounts', 'Enable conditional access for cloud apps', 'Disable dormant privileged accounts'], expected_score_lift: 15 },
    { phase: 2, timeline: '30-90 days', title: 'Universal MFA & SSO Coverage', actions: ['Achieve 95%+ MFA coverage', 'Implement JIT privileged access', 'Enable SSO for all business applications'], expected_score_lift: 20 },
    { phase: 3, timeline: '90-180 days', title: 'Continuous Verification', actions: ['Deploy FIDO2 passkeys for 80% of identities', 'Implement risk-based authentication', 'Enable UEBA and behavioral analytics'], expected_score_lift: 25 },
  ]
};

const PILLAR_COLORS: Record<string, string> = {
  identity: '#6366f1', devices: '#8b5cf6', networks: '#06b6d4',
  applications: '#10b981', data: '#f59e0b', infrastructure: '#f97316', analytics: '#ec4899'
};

const MATURITY_LEVELS = ['TRADITIONAL', 'INITIAL', 'ADVANCED', 'OPTIMAL'];
const MATURITY_COLORS: Record<string, string> = {
  TRADITIONAL: '#ef4444', INITIAL: '#f59e0b', ADVANCED: '#8b5cf6', OPTIMAL: '#10b981'
};

const PillarBar: React.FC<{ pillar: string; score: number }> = ({ pillar, score }) => {
  const color = PILLAR_COLORS[pillar] || '#6366f1';
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: '0.83rem' }}>
        <span style={{ color: '#94a3b8', textTransform: 'capitalize' }}>{pillar} Pillar</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{ width: 60, height: 4, background: 'rgba(255,255,255,0.1)', borderRadius: 2, overflow: 'hidden' }}>
            <div style={{ width: `${score}%`, height: '100%', background: color }} />
          </div>
          <span style={{ color, fontWeight: 700 }}>{score.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};

const RadarChart: React.FC<{ pillars: Record<string, number> }> = ({ pillars }) => {
  const entries = Object.entries(pillars);
  const n = entries.length;
  const cx = 160, cy = 160, r = 120;

  const points = entries.map(([, score], i) => {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2;
    const rr = (score / 100) * r;
    return { x: cx + rr * Math.cos(angle), y: cy + rr * Math.sin(angle) };
  });

  const gridLevels = [20, 40, 60, 80, 100];
  const axisPoints = entries.map(([, ], i) => {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2;
    return { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) };
  });
  const labelPoints = entries.map(([label, ], i) => {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2;
    const lr = r + 22;
    return { x: cx + lr * Math.cos(angle), y: cy + lr * Math.sin(angle), label };
  });

  const gridPath = (level: number) => {
    const rr = (level / 100) * r;
    const pts = entries.map((_, i) => {
      const angle = (2 * Math.PI * i) / n - Math.PI / 2;
      return `${cx + rr * Math.cos(angle)},${cy + rr * Math.sin(angle)}`;
    });
    return `M${pts.join(' L')}Z`;
  };

  const dataPath = `M${points.map(p => `${p.x},${p.y}`).join(' L')}Z`;

  return (
    <svg width={320} height={320} viewBox="0 0 320 320">
      {gridLevels.map(l => (
        <path key={l} d={gridPath(l)} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="1" />
      ))}
      {axisPoints.map((p, i) => (
        <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="rgba(255,255,255,0.08)" strokeWidth="1" />
      ))}
      <path d={dataPath} fill="rgba(99,102,241,0.2)" stroke="#6366f1" strokeWidth="2" />
      {labelPoints.map(({ x, y, label }) => (
        <text key={label} x={x} y={y} textAnchor="middle" dominantBaseline="middle"
          fill="#64748b" fontSize="9" style={{ textTransform: 'capitalize' }}>{label}</text>
      ))}
      {points.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r={3} fill={Object.values(PILLAR_COLORS)[i] || '#6366f1'} />
      ))}
      <text x={cx} y={cy - 8} textAnchor="middle" fill="#fff" fontSize="18" fontWeight="800">{ZT_DATA.overall_zt_score.toFixed(0)}</text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="9">Zero Trust Score</text>
    </svg>
  );
};

export default function ZeroTrustDashboard() {
  const maturityIndex = MATURITY_LEVELS.indexOf(ZT_DATA.maturity_level);
  const maturityColor = MATURITY_COLORS[ZT_DATA.maturity_level];

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ZT_STYLES}</style>
      <div className="zt-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="zt-icon"><Network size={24} /></div>
          <div>
            <h1 className="zt-title">Zero Trust Readiness</h1>
            <p className="zt-subtitle">NIST SP 800-207 · 7-Pillar Assessment · Identity · Devices · Networks · Applications · Data · Infrastructure · Analytics</p>
          </div>
        </div>
        <Link to="/ispm" style={{ textDecoration: 'none', color: '#818cf8', fontSize: '0.82rem', fontWeight: 500, padding: '8px 14px', background: 'rgba(99,102,241,0.12)', borderRadius: 9, border: '1px solid rgba(99,102,241,0.3)' }}>← ISPM</Link>
      </div>

      {/* Main Layout */}
      <div className="zt-main">
        {/* Radar + Score */}
        <div className="zt-radar-card">
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
            <RadarChart pillars={ZT_DATA.pillars} />
            <div className="zt-maturity-row">
              {MATURITY_LEVELS.map((level, i) => (
                <div key={level} className={`zt-maturity-step ${i <= maturityIndex ? 'zt-maturity-active' : ''}`}
                  style={i <= maturityIndex ? { borderColor: maturityColor, color: maturityColor, background: `${maturityColor}15` } : {}}>
                  {level}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Pillar Breakdown */}
        <div className="zt-pillars-card">
          <h3>Pillar Scores — NIST SP 800-207</h3>
          {Object.entries(ZT_DATA.pillars).map(([pillar, score]) => (
            <PillarBar key={pillar} pillar={pillar} score={score} />
          ))}
        </div>

        {/* ZT Criteria */}
        <div className="zt-criteria-card">
          <h3>Zero Trust Identity Criteria</h3>
          {[
            ['Continuous Verification', ZT_DATA.criteria.continuous_verification_enabled],
            ['Least Privilege Enforced', ZT_DATA.criteria.least_privilege_enforced],
            ['MFA Everywhere', ZT_DATA.criteria.mfa_everywhere],
            ['Device Trust Required', ZT_DATA.criteria.device_trust_required],
            ['Session Risk Evaluated', ZT_DATA.criteria.session_risk_evaluated],
            ['PAW/PAM Workstations', ZT_DATA.criteria.privileged_access_workstations],
          ].map(([label, value]) => (
            <div key={String(label)} className="zt-criteria-row">
              {value ? <CheckCircle size={16} color="#10b981" /> : <XCircle size={16} color="#ef4444" />}
              <span style={{ color: value ? '#10b981' : '#94a3b8', fontSize: '0.84rem', marginLeft: 10 }}>{String(label)}</span>
              {!value && <span className="zt-criteria-gap">GAP</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Gap Analysis */}
      <div className="zt-gap-card">
        <h3><AlertTriangle size={16} /> Gap Analysis</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 12 }}>
          {ZT_DATA.gap_analysis.map(gap => (
            <div key={gap.pillar} className="zt-gap-item" style={{ borderColor: gap.priority === 'CRITICAL' ? 'rgba(239,68,68,0.3)' : 'rgba(245,158,11,0.25)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{gap.pillar} Pillar</strong>
                <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 5, background: gap.priority === 'CRITICAL' ? 'rgba(239,68,68,0.15)' : 'rgba(245,158,11,0.15)', color: gap.priority === 'CRITICAL' ? '#f87171' : '#fbbf24', fontWeight: 700 }}>{gap.priority}</span>
              </div>
              <div style={{ fontSize: '0.78rem', color: '#64748b', marginBottom: 8 }}>{gap.description}</div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                <span style={{ color: '#94a3b8' }}>Current: <strong style={{ color: '#e2e8f0' }}>{gap.score}</strong></span>
                <span style={{ color: '#94a3b8' }}>Gap: <strong style={{ color: '#ef4444' }}>-{gap.gap.toFixed(1)}</strong></span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Roadmap */}
      <div className="zt-roadmap-card">
        <h3><TrendingUp size={16} /> Zero Trust Improvement Roadmap</h3>
        <div className="zt-roadmap-phases">
          {ZT_DATA.roadmap.map(phase => (
            <div key={phase.phase} className="zt-phase">
              <div className="zt-phase-header">
                <span className="zt-phase-num">Phase {phase.phase}</span>
                <strong>{phase.title}</strong>
                <span className="zt-phase-time">{phase.timeline}</span>
                <span className="zt-phase-lift">+{phase.expected_score_lift} pts</span>
              </div>
              <ul className="zt-phase-actions">
                {phase.actions.map(a => <li key={a}>{a}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const ZT_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.zt-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; gap: 16px; flex-wrap: wrap; }
.zt-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #6366f1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.zt-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin: 0 0 2px; }
.zt-subtitle { font-size: 0.72rem; color: #64748b; margin: 0; }
.zt-main { display: grid; grid-template-columns: auto 1fr 1fr; gap: 16px; margin-bottom: 16px; align-items: start; }
@media (max-width: 1100px) { .zt-main { grid-template-columns: 1fr; } }
.zt-radar-card, .zt-pillars-card, .zt-criteria-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; }
.zt-radar-card { display: flex; justify-content: center; }
.zt-pillars-card h3, .zt-criteria-card h3 { font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 18px; }
.zt-maturity-row { display: flex; gap: 6px; flex-wrap: wrap; justify-content: center; }
.zt-maturity-step { padding: 4px 10px; border-radius: 7px; border: 1px solid rgba(255,255,255,0.1); color: #475569; font-size: 0.72rem; font-weight: 600; transition: all 0.2s; }
.zt-maturity-active { font-weight: 800 !important; }
.zt-criteria-row { display: flex; align-items: center; padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.zt-criteria-gap { margin-left: auto; padding: 2px 8px; border-radius: 4px; background: rgba(239,68,68,0.15); color: #f87171; font-size: 0.68rem; font-weight: 700; }
.zt-gap-card, .zt-roadmap-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; margin-bottom: 14px; }
.zt-gap-card h3, .zt-roadmap-card h3 { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.zt-gap-item { background: rgba(255,255,255,0.02); border: 1px solid; border-radius: 11px; padding: 14px; }
.zt-roadmap-phases { display: flex; flex-direction: column; gap: 12px; }
.zt-phase { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 11px; padding: 14px; }
.zt-phase-header { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; flex-wrap: wrap; }
.zt-phase-num { background: rgba(99,102,241,0.2); color: #818cf8; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.zt-phase-header strong { color: #e2e8f0; font-size: 0.88rem; flex: 1; }
.zt-phase-time { font-size: 0.75rem; color: #64748b; }
.zt-phase-lift { background: rgba(16,185,129,0.15); color: #34d399; padding: 3px 9px; border-radius: 5px; font-size: 0.73rem; font-weight: 700; }
.zt-phase-actions { margin: 0; padding-left: 18px; }
.zt-phase-actions li { font-size: 0.82rem; color: #94a3b8; margin-bottom: 4px; }
`;
