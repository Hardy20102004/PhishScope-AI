import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, AlertTriangle } from 'lucide-react';

const RISKS = [
  { id: '1', domain: 'Privileged Access (PAM)', risk_level: 'CRITICAL', details: 'Standing privileges detected on 3 AWS accounts' },
  { id: '2', domain: 'Federated Trusts', risk_level: 'HIGH', details: 'Expiring SAML certificate in B2B partner connection' },
  { id: '3', domain: 'Workload Identity (NHI)', risk_level: 'MEDIUM', details: 'Stale service account in Kubernetes prod cluster' }
];

export default function UnifiedRiskDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{URSK_STYLES}</style>
      <div className="ursk-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ursk-header-icon"><Activity size={24} /></div>
          <div>
            <h1 className="ursk-title">Unified Risk Posture</h1>
            <p className="ursk-subtitle">Aggregated threat and posture intelligence across all identity domains</p>
          </div>
        </div>
        <Link to="/identity-cc" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Command Center</Link>
      </div>

      <div className="ursk-card">
        <h3 className="ursk-card-title"><AlertTriangle size={16} color="#ef4444" /> Enterprise Identity Risk Vectors</h3>
        <table className="ursk-table">
          <thead>
            <tr><th>Identity Domain</th><th>Aggregated Risk Level</th><th>Primary Risk Vector</th></tr>
          </thead>
          <tbody>
            {RISKS.map(risk => (
              <tr key={risk.id} className="ursk-row">
                <td style={{ fontWeight: 600 }}>{risk.domain}</td>
                <td>
                  <span className={`ursk-status ursk-${risk.risk_level.toLowerCase()}`}>
                    {risk.risk_level}
                  </span>
                </td>
                <td style={{ color: '#cbd5e1' }}>{risk.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const URSK_STYLES = `
.ursk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ursk-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ursk-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ursk-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ursk-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.ursk-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.ursk-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.ursk-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.ursk-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.ursk-row td { padding: 12px; }
.ursk-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.ursk-critical { background: rgba(239,68,68,0.2); color: #fca5a5; }
.ursk-high { background: rgba(249,115,22,0.2); color: #fdba74; }
.ursk-medium { background: rgba(234,179,8,0.2); color: #fde047; }
`;
