import React from 'react';
import { Link } from 'react-router-dom';
import { FileKey, Clock } from 'lucide-react';

const CERTS = [
  { id: '1', provider: 'Okta Primary IdP', thumbprint: 'a1:b2:c3:d4', valid_from: '2025-01-01', expires: '2028-01-01', status: 'VALID' },
  { id: '2', provider: 'Partner B2B Portal', thumbprint: 'e5:f6:07:18', valid_from: '2024-08-01', expires: '2026-08-07', status: 'EXPIRING_SOON' },
  { id: '3', provider: 'Legacy HR Connect', thumbprint: '99:aa:bb:cc', valid_from: '2020-01-01', expires: '2025-01-01', status: 'EXPIRED' }
];

export default function MetadataDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{META_STYLES}</style>
      <div className="meta-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="meta-header-icon"><FileKey size={24} /></div>
          <div>
            <h1 className="meta-title">Metadata & Certificates</h1>
            <p className="meta-subtitle">Track signing certificate lifecycles and metadata freshness</p>
          </div>
        </div>
        <Link to="/federation" style={{ color: '#38bdf8', textDecoration: 'none', fontSize: '0.85rem' }}>← Federation Dashboard</Link>
      </div>

      <div className="meta-card">
        <h3 className="meta-card-title"><Clock size={16} /> Certificate Expiration Tracking</h3>
        <table className="meta-table">
          <thead>
            <tr><th>Federation Provider</th><th>Thumbprint</th><th>Valid From</th><th>Expires At</th><th>Status</th></tr>
          </thead>
          <tbody>
            {CERTS.map(cert => (
              <tr key={cert.id} className="meta-row">
                <td style={{ fontWeight: 600 }}>{cert.provider}</td>
                <td style={{ color: '#94a3b8', fontFamily: 'monospace' }}>{cert.thumbprint}</td>
                <td style={{ color: '#cbd5e1' }}>{cert.valid_from}</td>
                <td style={{ color: '#cbd5e1', fontWeight: cert.status !== 'VALID' ? 700 : 400 }}>{cert.expires}</td>
                <td>
                  <span className={`meta-status meta-${cert.status.toLowerCase()}`}>
                    {cert.status.replace('_', ' ')}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const META_STYLES = `
.meta-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.meta-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.meta-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.meta-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.meta-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.meta-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.meta-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.meta-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.meta-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.meta-row td { padding: 12px; }
.meta-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.meta-valid { background: rgba(16,185,129,0.15); color: #34d399; }
.meta-expiring_soon { background: rgba(249,115,22,0.2); color: #fdba74; }
.meta-expired { background: rgba(239,68,68,0.2); color: #fca5a5; }
`;
