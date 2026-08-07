import React from 'react';
import { Link } from 'react-router-dom';
import { Fingerprint, MonitorSmartphone, Key } from 'lucide-react';

const PASSKEYS = [
  { id: '1', name: 'iPhone 15 Pro Max', user: 'alice.smith', type: 'Platform (Syncable)', provider: 'Apple Passkeys', created: '2025-11-20', status: 'ACTIVE' },
  { id: '2', name: 'YubiKey 5 NFC', user: 'admin.service', type: 'Roaming (Hardware)', provider: 'Yubico', created: '2023-05-12', status: 'ACTIVE' },
  { id: '3', name: 'Windows Hello', user: 'bob.jones', type: 'Platform (Device Bound)', provider: 'Microsoft', created: '2026-01-05', status: 'PENDING_ACTIVATION' }
];

export default function PasskeyDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PK_STYLES}</style>
      <div className="pk-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="pk-header-icon"><Fingerprint size={24} /></div>
          <div>
            <h1 className="pk-title">Passkey & FIDO2 Inventory</h1>
            <p className="pk-subtitle">Central visibility into modern, phishing-resistant authenticators</p>
          </div>
        </div>
        <Link to="/authn" style={{ color: '#a78bfa', textDecoration: 'none', fontSize: '0.85rem' }}>← AUTHN Dashboard</Link>
      </div>

      <div className="pk-card">
        <h3 className="pk-card-title">Registered Authenticators</h3>
        <table className="pk-table">
          <thead>
            <tr><th>Authenticator Name</th><th>Owner Identity</th><th>Type</th><th>Provider</th><th>Registration Date</th><th>Status</th></tr>
          </thead>
          <tbody>
            {PASSKEYS.map(pk => (
              <tr key={pk.id} className="pk-row">
                <td style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 8 }}>
                  {pk.type.includes('Roaming') ? <Key size={14} color="#a78bfa" /> : <MonitorSmartphone size={14} color="#60a5fa" />}
                  {pk.name}
                </td>
                <td style={{ color: '#cbd5e1' }}>{pk.user}</td>
                <td><span className="pk-type-badge">{pk.type}</span></td>
                <td style={{ color: '#94a3b8' }}>{pk.provider}</td>
                <td style={{ color: '#94a3b8' }}>{pk.created}</td>
                <td>
                  <span className={`pk-status pk-${pk.status.toLowerCase()}`}>
                    {pk.status.replace('_', ' ')}
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

const PK_STYLES = `
.pk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.pk-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #6d28d9); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.pk-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.pk-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.pk-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.pk-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.pk-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.pk-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.pk-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.pk-row td { padding: 12px; }
.pk-type-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 0.75rem; color: #cbd5e1; }
.pk-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.pk-active { background: rgba(16,185,129,0.15); color: #34d399; }
.pk-pending_activation { background: rgba(245,158,11,0.15); color: #fbbf24; }
`;
