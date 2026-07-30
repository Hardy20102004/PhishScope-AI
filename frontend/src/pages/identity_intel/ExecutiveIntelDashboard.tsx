import React from 'react';
import { Link } from 'react-router-dom';
import { Fingerprint, TrendingUp } from 'lucide-react';

const EXEC_METRICS = {
  strategic_risk_index: 42.5,
  zero_trust_alignment: 85,
  mfa_coverage: 94,
  pam_coverage: 88,
  orphaned_accounts: 12
};

export default function ExecutiveIntelDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{EXEC_STYLES}</style>
      <div className="exec-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="exec-header-icon"><Fingerprint size={24} /></div>
          <div>
            <h1 className="exec-title">Executive Identity Intelligence</h1>
            <p className="exec-subtitle">C-Level strategic view of enterprise identity posture</p>
          </div>
        </div>
        <Link to="/identity-intel" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Intelligence Dashboard</Link>
      </div>

      <div className="exec-grid">
        <div className="exec-card" style={{ gridColumn: 'span 2' }}>
          <h3 className="exec-card-title"><TrendingUp size={16} color="#8b5cf6" /> Strategic Risk Index (Lower is Better)</h3>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
            <span style={{ fontSize: '3.5rem', fontWeight: 800, color: EXEC_METRICS.strategic_risk_index < 50 ? '#10b981' : '#ef4444' }}>
              {EXEC_METRICS.strategic_risk_index}
            </span>
            <span style={{ color: '#94a3b8', fontSize: '0.9rem' }}>/ 100</span>
          </div>
          <p style={{ margin: '8px 0 0', fontSize: '0.8rem', color: '#64748b' }}>Combined aggregate of Auth, PAM, IGA, and Federation risks.</p>
        </div>
        
        <div className="exec-card">
          <h3 className="exec-card-title">Zero Trust Alignment</h3>
          <span style={{ fontSize: '2rem', fontWeight: 700, color: '#38bdf8' }}>{EXEC_METRICS.zero_trust_alignment}%</span>
        </div>
        
        <div className="exec-card">
          <h3 className="exec-card-title">MFA Coverage</h3>
          <span style={{ fontSize: '2rem', fontWeight: 700, color: '#10b981' }}>{EXEC_METRICS.mfa_coverage}%</span>
        </div>
        
        <div className="exec-card">
          <h3 className="exec-card-title">Privileged Access Coverage</h3>
          <span style={{ fontSize: '2rem', fontWeight: 700, color: '#f59e0b' }}>{EXEC_METRICS.pam_coverage}%</span>
        </div>
        
        <div className="exec-card">
          <h3 className="exec-card-title">Orphaned Accounts</h3>
          <span style={{ fontSize: '2rem', fontWeight: 700, color: '#ef4444' }}>{EXEC_METRICS.orphaned_accounts}</span>
        </div>
      </div>
    </div>
  );
}

const EXEC_STYLES = `
.exec-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.exec-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #6d28d9); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.exec-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.exec-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.exec-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.exec-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px; }
.exec-card-title { font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 12px; display: flex; alignItems: center; gap: 8px; }
@media (max-width: 900px) { .exec-grid { grid-template-columns: 1fr 1fr; } .exec-card[style] { grid-column: span 2; } }
`;
