import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Shield, Lock, CheckCircle, XCircle, AlertTriangle, ChevronRight, Key, Fingerprint, Smartphone, Globe } from 'lucide-react';

const AUTH_DATA = {
  total_identities: 847,
  mfa_enabled_count: 628,
  mfa_coverage_pct: 74.2,
  sso_enabled_count: 580,
  sso_coverage_pct: 68.5,
  passwordless_count: 155,
  passwordless_coverage_pct: 18.3,
  phishing_resistant_pct: 22.1,
  no_mfa_privileged_count: 7,
  weak_auth_count: 219,
  password_only_count: 187,
  expired_certificates_count: 12,
  overall_auth_score: 61.4,
  mfa_method_distribution: {
    MFA_TOTP: 38, MFA_PUSH: 28, MFA_SMS: 15, MFA_HARDWARE_TOKEN: 10, PASSKEY: 5, CERTIFICATE: 4
  },
  auth_method_distribution: {
    PASSWORD: 22, SSO_SAML: 35, SSO_OIDC: 18, MFA_TOTP: 15, PASSKEY: 6, CERTIFICATE: 4
  }
};

const MethodBar: React.FC<{ label: string; pct: number; color: string; risk?: string }> = ({ label, pct, color, risk }) => (
  <div style={{ marginBottom: 12 }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', color: '#94a3b8', marginBottom: 5 }}>
      <span>{label}</span>
      <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
        {risk && <span style={{ fontSize: '0.7rem', padding: '2px 7px', borderRadius: 4, background: risk === 'HIGH' ? 'rgba(239,68,68,0.15)' : risk === 'MEDIUM' ? 'rgba(245,158,11,0.15)' : 'rgba(16,185,129,0.15)', color: risk === 'HIGH' ? '#f87171' : risk === 'MEDIUM' ? '#fbbf24' : '#34d399' }}>{risk}</span>}
        <span style={{ color }}>{pct.toFixed(1)}%</span>
      </div>
    </div>
    <div style={{ height: 8, background: 'rgba(255,255,255,0.08)', borderRadius: 4, overflow: 'hidden' }}>
      <div style={{ width: `${Math.min(pct, 100)}%`, height: '100%', background: color, borderRadius: 4, transition: 'width 0.8s ease' }} />
    </div>
  </div>
);

const GaugeRing: React.FC<{ value: number; label: string; target: number; color: string }> = ({ value, label, target, color }) => {
  const size = 130;
  const r = 50;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  const targetOffset = circ - (target / 100) * circ;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={65} cy={65} r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="10" />
        <circle cx={65} cy={65} r={r} fill="none" stroke={color} strokeWidth="10"
          strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
          transform="rotate(-90 65 65)" style={{ transition: 'stroke-dashoffset 1s ease' }} />
        <circle cx={65} cy={65} r={r} fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="2"
          strokeDasharray={`4 ${circ - 4}`} strokeDashoffset={targetOffset}
          transform="rotate(-90 65 65)" />
        <text x={65} y={58} textAnchor="middle" fill="#fff" fontSize="20" fontWeight="800">{value.toFixed(0)}%</text>
        <text x={65} y={72} textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="9">target: {target}%</text>
      </svg>
      <span style={{ fontSize: '0.78rem', color: '#94a3b8', textAlign: 'center' }}>{label}</span>
    </div>
  );
};

export default function AuthenticationDashboard() {
  const total = AUTH_DATA.total_identities;
  const mfaDist = AUTH_DATA.mfa_method_distribution;
  const mfaTotal = Object.values(mfaDist).reduce((a, b) => a + b, 0);
  const authDist = AUTH_DATA.auth_method_distribution;
  const authTotal = Object.values(authDist).reduce((a, b) => a + b, 0);

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{AUTH_STYLES}</style>
      <div className="auth-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="auth-icon"><Lock size={24} /></div>
          <div>
            <h1 className="auth-title">Authentication Assessment</h1>
            <p className="auth-subtitle">MFA Coverage · SSO · Passwordless · NIST SP 800-63B AAL Assessment</p>
          </div>
        </div>
        <Link to="/ispm" style={{ textDecoration: 'none' }} className="auth-back-btn">← ISPM Dashboard</Link>
      </div>

      {/* Critical Alert */}
      {AUTH_DATA.no_mfa_privileged_count > 0 && (
        <div className="auth-alert-banner">
          <AlertTriangle size={16} />
          <strong>CRITICAL:</strong> {AUTH_DATA.no_mfa_privileged_count} privileged identities have no MFA. Immediate enforcement required (MITRE T1078).
        </div>
      )}

      {/* Score + Gauges */}
      <div className="auth-main-card">
        <div className="auth-score-section">
          <div className="auth-overall-score">
            <div style={{ fontSize: '3rem', fontWeight: 800, color: '#6366f1', lineHeight: 1 }}>
              {AUTH_DATA.overall_auth_score.toFixed(0)}
            </div>
            <div style={{ fontSize: '0.82rem', color: '#64748b' }}>Authentication Score /100</div>
            <div style={{ marginTop: 8 }}>
              <span className={`auth-grade auth-grade-${AUTH_DATA.overall_auth_score >= 80 ? 'good' : AUTH_DATA.overall_auth_score >= 60 ? 'fair' : 'poor'}`}>
                {AUTH_DATA.overall_auth_score >= 80 ? 'Good' : AUTH_DATA.overall_auth_score >= 60 ? 'Fair' : 'Needs Improvement'}
              </span>
            </div>
          </div>
        </div>
        <div className="auth-gauges">
          <GaugeRing value={AUTH_DATA.mfa_coverage_pct} label="MFA Coverage" target={95} color="#6366f1" />
          <GaugeRing value={AUTH_DATA.sso_coverage_pct} label="SSO Coverage" target={80} color="#8b5cf6" />
          <GaugeRing value={AUTH_DATA.passwordless_coverage_pct} label="Passwordless" target={50} color="#06b6d4" />
          <GaugeRing value={AUTH_DATA.phishing_resistant_pct} label="Phishing-Resistant" target={80} color="#10b981" />
        </div>
      </div>

      {/* Risk Stats */}
      <div className="auth-risk-stats">
        {[
          { label: 'No MFA (Privileged)', value: AUTH_DATA.no_mfa_privileged_count, color: '#ef4444', icon: <Key size={16} /> },
          { label: 'Password Only', value: AUTH_DATA.password_only_count, color: '#f97316', icon: <Lock size={16} /> },
          { label: 'Weak Auth', value: AUTH_DATA.weak_auth_count, color: '#f59e0b', icon: <AlertTriangle size={16} /> },
          { label: 'Expired Certs', value: AUTH_DATA.expired_certificates_count, color: '#dc2626', icon: <XCircle size={16} /> },
          { label: 'MFA Enabled', value: AUTH_DATA.mfa_enabled_count, color: '#10b981', icon: <CheckCircle size={16} /> },
          { label: 'SSO Enabled', value: AUTH_DATA.sso_enabled_count, color: '#8b5cf6', icon: <Globe size={16} /> },
        ].map(({ label, value, color, icon }) => (
          <div key={label} className="auth-risk-stat" style={{ borderColor: `${color}30` }}>
            <div style={{ color, marginBottom: 6 }}>{icon}</div>
            <div style={{ fontSize: '1.6rem', fontWeight: 800, color }}>{value}</div>
            <div style={{ fontSize: '0.72rem', color: '#64748b', textAlign: 'center' }}>{label}</div>
          </div>
        ))}
      </div>

      {/* Distribution Charts */}
      <div className="auth-distributions">
        <div className="auth-dist-card">
          <h3><Smartphone size={16} /> MFA Method Distribution</h3>
          {Object.entries(mfaDist).map(([method, count]) => {
            const riskMap: Record<string, string> = { MFA_SMS: 'HIGH', MFA_PUSH: 'MEDIUM', MFA_TOTP: 'MEDIUM', MFA_HARDWARE_TOKEN: 'LOW', PASSKEY: 'LOW', CERTIFICATE: 'LOW' };
            const colorMap: Record<string, string> = { MFA_SMS: '#ef4444', MFA_PUSH: '#f59e0b', MFA_TOTP: '#8b5cf6', MFA_HARDWARE_TOKEN: '#10b981', PASSKEY: '#06b6d4', CERTIFICATE: '#6366f1' };
            return (
              <MethodBar key={method} label={method.replace(/_/g, ' ')} pct={(count / mfaTotal) * 100} color={colorMap[method] || '#6366f1'} risk={riskMap[method]} />
            );
          })}
        </div>
        <div className="auth-dist-card">
          <h3><Globe size={16} /> Auth Method Distribution</h3>
          {Object.entries(authDist).map(([method, count]) => {
            const colorMap: Record<string, string> = { PASSWORD: '#ef4444', SSO_SAML: '#8b5cf6', SSO_OIDC: '#6366f1', MFA_TOTP: '#10b981', PASSKEY: '#06b6d4', CERTIFICATE: '#f59e0b' };
            const riskMap: Record<string, string> = { PASSWORD: 'HIGH', SSO_SAML: 'LOW', SSO_OIDC: 'LOW', MFA_TOTP: 'MEDIUM', PASSKEY: 'LOW', CERTIFICATE: 'LOW' };
            return (
              <MethodBar key={method} label={method.replace(/_/g, ' ')} pct={(count / authTotal) * 100} color={colorMap[method] || '#6366f1'} risk={riskMap[method]} />
            );
          })}
        </div>
      </div>

      {/* NIST AAL Table */}
      <div className="auth-aal-card">
        <h3><Fingerprint size={16} /> NIST SP 800-63B Authentication Assurance Level Coverage</h3>
        <table className="auth-aal-table">
          <thead><tr><th>Level</th><th>Description</th><th>Methods</th><th>Coverage</th><th>Status</th></tr></thead>
          <tbody>
            <tr>
              <td><span className="aal-badge aal-1">AAL1</span></td>
              <td>Single-factor authentication</td>
              <td>Password, PIN</td>
              <td>100%</td>
              <td><CheckCircle size={14} color="#10b981" /></td>
            </tr>
            <tr>
              <td><span className="aal-badge aal-2">AAL2</span></td>
              <td>Multi-factor authentication</td>
              <td>TOTP, Push, SMS</td>
              <td>{AUTH_DATA.mfa_coverage_pct.toFixed(1)}%</td>
              <td><AlertTriangle size={14} color="#f59e0b" /></td>
            </tr>
            <tr>
              <td><span className="aal-badge aal-3">AAL3</span></td>
              <td>Hardware-based, phishing-resistant</td>
              <td>FIDO2, Hardware Token, Certificate</td>
              <td>{AUTH_DATA.phishing_resistant_pct.toFixed(1)}%</td>
              <td><XCircle size={14} color="#ef4444" /></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

const AUTH_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.auth-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; gap: 16px; flex-wrap: wrap; }
.auth-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #06b6d4); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.auth-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin: 0 0 2px; }
.auth-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.auth-back-btn { color: #818cf8; font-size: 0.82rem; font-weight: 500; padding: 8px 14px; background: rgba(99,102,241,0.12); border-radius: 9px; border: 1px solid rgba(99,102,241,0.3); }
.auth-alert-banner { display: flex; align-items: center; gap: 10px; background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.35); border-radius: 11px; padding: 12px 16px; margin-bottom: 16px; color: #fca5a5; font-size: 0.83rem; }
.auth-main-card { display: flex; gap: 20px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 24px; margin-bottom: 16px; align-items: center; flex-wrap: wrap; }
.auth-score-section { display: flex; align-items: center; justify-content: center; min-width: 160px; }
.auth-overall-score { text-align: center; }
.auth-grade { display: inline-block; padding: 4px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; }
.auth-grade-good { background: rgba(16,185,129,0.15); color: #34d399; }
.auth-grade-fair { background: rgba(245,158,11,0.15); color: #fbbf24; }
.auth-grade-poor { background: rgba(239,68,68,0.15); color: #f87171; }
.auth-gauges { display: flex; gap: 24px; flex-wrap: wrap; justify-content: center; flex: 1; }
.auth-risk-stats { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.auth-risk-stat { display: flex; flex-direction: column; align-items: center; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; min-width: 100px; flex: 1; }
.auth-distributions { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
@media (max-width: 768px) { .auth-distributions { grid-template-columns: 1fr; } }
.auth-dist-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; }
.auth-dist-card h3 { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.auth-aal-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; }
.auth-aal-card h3 { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.auth-aal-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.auth-aal-table th { color: #64748b; font-weight: 500; padding: 9px 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.07); }
.auth-aal-table td { color: #94a3b8; padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.aal-badge { padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.aal-1 { background: rgba(100,116,139,0.2); color: #94a3b8; }
.aal-2 { background: rgba(245,158,11,0.15); color: #fbbf24; }
.aal-3 { background: rgba(16,185,129,0.15); color: #34d399; }
`;
