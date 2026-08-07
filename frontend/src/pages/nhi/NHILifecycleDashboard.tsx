import React from 'react';
import { Link } from 'react-router-dom';
import { RefreshCw, History } from 'lucide-react';

const EVENTS = [
  { id: '1', identity: 'prod-db-service-acc', event: 'ROTATED', actor: 'Vault Auto-Rotator', time: '2025-10-01 04:00' },
  { id: '2', identity: 'legacy-app-svc', event: 'REVOKED', actor: 'alice.smith (Admin)', time: '2026-07-30 09:15' }
];

export default function NHILifecycleDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{LIFECYCLE_STYLES}</style>
      <div className="nhil-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="nhil-header-icon"><RefreshCw size={24} /></div>
          <div>
            <h1 className="nhil-title">Lifecycle & Rotation</h1>
            <p className="nhil-subtitle">Audit log for machine identity creation, rotation, and revocation</p>
          </div>
        </div>
        <Link to="/nhi" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← NHI Dashboard</Link>
      </div>

      <div className="nhil-card">
        <h3 className="nhil-card-title"><History size={16} /> Recent Lifecycle Events</h3>
        <table className="nhil-table">
          <thead>
            <tr><th>Target Identity</th><th>Event Type</th><th>Actor</th><th>Timestamp</th></tr>
          </thead>
          <tbody>
            {EVENTS.map(ev => (
              <tr key={ev.id} className="nhil-row">
                <td style={{ fontWeight: 600 }}>{ev.identity}</td>
                <td><span className={`nhil-evt nhil-evt-${ev.event.toLowerCase()}`}>{ev.event}</span></td>
                <td style={{ color: '#94a3b8' }}>{ev.actor}</td>
                <td style={{ color: '#cbd5e1' }}>{ev.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const LIFECYCLE_STYLES = `
.nhil-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.nhil-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.nhil-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.nhil-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.nhil-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.nhil-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.nhil-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.nhil-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.nhil-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.nhil-row td { padding: 12px; }
.nhil-evt { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.nhil-evt-rotated { background: rgba(59,130,246,0.15); color: #60a5fa; }
.nhil-evt-revoked { background: rgba(239,68,68,0.15); color: #fca5a5; }
`;
