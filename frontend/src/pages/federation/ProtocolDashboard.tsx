import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, AlertTriangle } from 'lucide-react';

const PROTOCOLS = [
  { id: '1', trust: 'Salesforce (Prod)', type: 'SAML 2.0', signed_asserts: true, encrypted_asserts: false, risk: 'HIGH' },
  { id: '2', trust: 'Workday HR', type: 'SAML 2.0', signed_asserts: true, encrypted_asserts: true, risk: 'LOW' },
  { id: '3', trust: 'Internal Wiki', type: 'OIDC', allowed_redirects: ['https://wiki.internal.corp/*', 'http://localhost'], risk: 'CRITICAL' }
];

export default function ProtocolDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PROT_STYLES}</style>
      <div className="prot-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="prot-header-icon"><ShieldAlert size={24} /></div>
          <div>
            <h1 className="prot-title">Protocol Validation</h1>
            <p className="prot-subtitle">Detect SAML/OIDC misconfigurations and security vulnerabilities</p>
          </div>
        </div>
        <Link to="/federation" style={{ color: '#38bdf8', textDecoration: 'none', fontSize: '0.85rem' }}>← Federation Dashboard</Link>
      </div>

      <div className="prot-card">
        <h3 className="prot-card-title"><AlertTriangle size={16} color="#ef4444" /> Security Violations Detected</h3>
        <table className="prot-table">
          <thead>
            <tr><th>Trust Configuration</th><th>Protocol</th><th>Security Flags</th><th>Risk Level</th></tr>
          </thead>
          <tbody>
            {PROTOCOLS.map(prot => (
              <tr key={prot.id} className="prot-row">
                <td style={{ fontWeight: 600 }}>{prot.trust}</td>
                <td>{prot.type}</td>
                <td>
                  <ul style={{ margin: 0, paddingLeft: 16, color: '#cbd5e1', fontSize: '0.8rem' }}>
                    {prot.type === 'SAML 2.0' && !prot.encrypted_asserts && <li>Unencrypted Assertions</li>}
                    {prot.type === 'OIDC' && prot.allowed_redirects?.some(u => u.includes('*')) && <li>Wildcard in Redirect URIs</li>}
                    {prot.type === 'OIDC' && prot.allowed_redirects?.some(u => u.includes('localhost')) && <li>Localhost Redirect Allowed</li>}
                    {prot.encrypted_asserts && <li style={{ color: '#10b981' }}>Securely Configured</li>}
                  </ul>
                </td>
                <td>
                  <span className={`prot-risk prot-risk-${prot.risk.toLowerCase()}`}>{prot.risk}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const PROT_STYLES = `
.prot-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.prot-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.prot-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.prot-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.prot-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.prot-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.prot-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.prot-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.prot-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.prot-row td { padding: 12px; }
.prot-risk { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.prot-risk-critical { background: rgba(239,68,68,0.2); color: #fca5a5; }
.prot-risk-high { background: rgba(249,115,22,0.2); color: #fdba74; }
.prot-risk-low { background: rgba(16,185,129,0.15); color: #34d399; }
`;
