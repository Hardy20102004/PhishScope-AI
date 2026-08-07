import React from 'react';
import { Link } from 'react-router-dom';
import { Link as LinkIcon, Lock } from 'lucide-react';

const TRUSTS = [
  { id: '1', source: 'github-actions-deployer', target: 'arn:aws:iam::123:role/ProdDeploy', type: 'OIDC', permissions: 'AssumeRoleWithWebIdentity', risk: 'HIGH' },
  { id: '2', source: 'payments-api.internal', target: 'spiffe://cluster.local/ns/db/sa/postgres', type: 'SPIFFE', permissions: 'mTLS Connect', risk: 'LOW' }
];

export default function TrustRelationshipDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{TRUST_STYLES}</style>
      <div className="tr-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="tr-header-icon"><LinkIcon size={24} /></div>
          <div>
            <h1 className="tr-title">Trust Relationships</h1>
            <p className="tr-subtitle">Analyze cross-environment and federated identity trust mappings</p>
          </div>
        </div>
        <Link to="/nhi" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← NHI Dashboard</Link>
      </div>

      <div className="tr-card">
        <h3 className="tr-card-title"><Lock size={16} /> Federated & OIDC Trusts</h3>
        <table className="tr-table">
          <thead>
            <tr><th>Source Identity</th><th>Trust Type</th><th>Target Resource</th><th>Granted Permissions</th><th>Risk Level</th></tr>
          </thead>
          <tbody>
            {TRUSTS.map(tr => (
              <tr key={tr.id} className="tr-row">
                <td style={{ fontWeight: 600 }}>{tr.source}</td>
                <td><span className="tr-type-badge">{tr.type}</span></td>
                <td style={{ color: '#94a3b8', fontSize: '0.8rem', fontFamily: 'monospace' }}>{tr.target}</td>
                <td style={{ color: '#cbd5e1', fontSize: '0.8rem' }}>{tr.permissions}</td>
                <td><span className={`tr-risk tr-risk-${tr.risk.toLowerCase()}`}>{tr.risk}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const TRUST_STYLES = `
.tr-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.tr-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.tr-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.tr-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.tr-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.tr-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.tr-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.tr-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.tr-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.tr-row td { padding: 12px; }
.tr-type-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.75rem; }
.tr-risk { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.tr-risk-high { background: rgba(249,115,22,0.15); color: #fdba74; }
.tr-risk-low { background: rgba(16,185,129,0.15); color: #34d399; }
`;
