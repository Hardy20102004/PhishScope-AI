import React from 'react';
import { Link } from 'react-router-dom';
import { Crosshair, ShieldX, Server, Globe } from 'lucide-react';

const ATTACKS = [
  { id: '1', type: 'PASSWORD_SPRAY', targets: 45, ips: ['185.15.2.4', '185.15.2.5'], count: 1250, severity: 'CRITICAL', first_seen: '2026-07-30 08:00' },
  { id: '2', type: 'CREDENTIAL_STUFFING', targets: 1, ips: ['45.3.2.1'], count: 300, severity: 'HIGH', first_seen: '2026-07-30 09:15' },
  { id: '3', type: 'MFA_FATIGUE', targets: 1, ips: ['104.22.33.11'], count: 15, severity: 'HIGH', first_seen: '2026-07-30 10:30' }
];

export default function CredentialDefenseDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CD_STYLES}</style>
      <div className="cd-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="cd-header-icon"><Crosshair size={24} /></div>
          <div>
            <h1 className="cd-title">Credential Attack Defense</h1>
            <p className="cd-subtitle">Monitor and block password spraying, stuffing, and MFA fatigue attacks</p>
          </div>
        </div>
        <Link to="/itdr" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ITDR</Link>
      </div>

      <div className="cd-card">
        <h3 className="cd-card-title"><ShieldX size={16} /> Active Attacks</h3>
        <table className="cd-table">
          <thead>
            <tr><th>Attack Type</th><th>Target Identities</th><th>Source IPs</th><th>Event Count</th><th>Severity</th><th>First Seen</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {ATTACKS.map(a => (
              <tr key={a.id} className="cd-row">
                <td style={{ fontWeight: 600, color: '#f87171' }}>{a.type.replace('_', ' ')}</td>
                <td>{a.targets} identities</td>
                <td>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {a.ips.map(ip => <span key={ip} style={{ fontSize: '0.8rem', color: '#94a3b8' }}>{ip}</span>)}
                  </div>
                </td>
                <td style={{ color: '#cbd5e1' }}>{a.count}</td>
                <td><span className={`cd-sev-badge cd-sev-${a.severity.toLowerCase()}`}>{a.severity}</span></td>
                <td style={{ color: '#64748b', fontSize: '0.8rem' }}>{a.first_seen}</td>
                <td>
                  <button className="cd-btn-block"><Globe size={12} /> Block IPs</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const CD_STYLES = `
.cd-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.cd-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.cd-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.cd-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.cd-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.cd-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.cd-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.cd-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.cd-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.cd-row td { padding: 12px; }
.cd-sev-badge { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.cd-sev-critical { background: rgba(239,68,68,0.15); color: #fca5a5; }
.cd-sev-high { background: rgba(249,115,22,0.15); color: #fdba74; }
.cd-btn-block { display: inline-flex; align-items: center; gap: 4px; padding: 6px 10px; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 6px; color: #fca5a5; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.cd-btn-block:hover { background: rgba(239,68,68,0.2); }
`;
