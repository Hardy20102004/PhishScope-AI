import React from 'react';
import { Link } from 'react-router-dom';
import { Key, AlertTriangle, CheckCircle } from 'lucide-react';

const CERTS = [
  { id: '1', name: 'payments-api.internal', issuer: 'DigiCert Global Root CA', expires: '2026-08-13', status: 'EXPIRING_SOON' },
  { id: '2', name: 'auth-gateway.internal', issuer: 'Let\'s Encrypt Authority X3', expires: '2027-01-20', status: 'VALID' },
  { id: '3', name: 'legacy-db-ssl', issuer: 'Internal PKI', expires: '2026-07-01', status: 'EXPIRED' }
];

export default function CertificateDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CERT_STYLES}</style>
      <div className="cert-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="cert-header-icon"><Key size={24} /></div>
          <div>
            <h1 className="cert-title">Certificate Governance</h1>
            <p className="cert-subtitle">Track SSL/TLS certificates and mutual TLS (mTLS) identities</p>
          </div>
        </div>
        <Link to="/nhi" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← NHI Dashboard</Link>
      </div>

      <div className="cert-card">
        <h3 className="cert-card-title">Certificate Inventory</h3>
        <table className="cert-table">
          <thead>
            <tr><th>Common Name (CN)</th><th>Issuer</th><th>Expiration Date</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            {CERTS.map(cert => (
              <tr key={cert.id} className="cert-row">
                <td style={{ fontWeight: 600 }}>{cert.name}</td>
                <td style={{ color: '#94a3b8' }}>{cert.issuer}</td>
                <td style={{ color: '#cbd5e1' }}>{cert.expires}</td>
                <td>
                  <span className={`cert-status cert-${cert.status.toLowerCase()}`}>
                    {cert.status.replace('_', ' ')}
                  </span>
                </td>
                <td>
                  <button className="cert-btn-view">Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const CERT_STYLES = `
.cert-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.cert-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.cert-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.cert-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.cert-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.cert-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.cert-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.cert-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.cert-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.cert-row td { padding: 12px; }
.cert-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.cert-valid { background: rgba(16,185,129,0.15); color: #34d399; }
.cert-expiring_soon { background: rgba(245,158,11,0.15); color: #fbbf24; }
.cert-expired { background: rgba(239,68,68,0.15); color: #f87171; }
.cert-btn-view { padding: 6px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #e2e8f0; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.cert-btn-view:hover { background: rgba(255,255,255,0.1); }
`;
