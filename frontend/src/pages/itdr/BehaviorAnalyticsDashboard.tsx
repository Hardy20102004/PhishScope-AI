import React from 'react';
import { Link } from 'react-router-dom';
import { Map, Activity, Fingerprint, ShieldAlert, Navigation } from 'lucide-react';

const BASELINES = [
  { id: '1', identity: 'alice.security', locations: ['Seattle, WA', 'Portland, OR'], devices: ['MacBook Pro (Corp)', 'iPhone 13'], velocity: '2.5 / hr', status: 'STABLE' },
  { id: '2', identity: 'bob.devops', locations: ['Austin, TX'], devices: ['ThinkPad X1'], velocity: '4.2 / hr', status: 'ANOMALOUS' },
  { id: '3', identity: 'svc-data-sync', locations: ['AWS us-east-1'], devices: ['K8s Node'], velocity: '120 / hr', status: 'STABLE' }
];

export default function BehaviorAnalyticsDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{BA_STYLES}</style>
      <div className="ba-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ba-header-icon"><Map size={24} /></div>
          <div>
            <h1 className="ba-title">Behavioral Analytics</h1>
            <p className="ba-subtitle">Identity baselines, anomalous velocity, and unusual locations</p>
          </div>
        </div>
        <Link to="/itdr" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ITDR</Link>
      </div>

      <div className="ba-card">
        <h3 className="ba-card-title"><Fingerprint size={16} /> Monitored Identity Baselines</h3>
        <table className="ba-table">
          <thead>
            <tr><th>Identity</th><th>Frequent Locations</th><th>Known Devices</th><th>Auth Velocity (Avg)</th><th>Current Status</th></tr>
          </thead>
          <tbody>
            {BASELINES.map(b => (
              <tr key={b.id} className="ba-row">
                <td style={{ fontWeight: 600 }}>{b.identity}</td>
                <td>
                  <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                    {b.locations.map((loc, i) => <span key={i} className="ba-pill"><Navigation size={10} /> {loc}</span>)}
                  </div>
                </td>
                <td style={{ color: '#94a3b8', fontSize: '0.8rem' }}>{b.devices.join(', ')}</td>
                <td style={{ color: '#cbd5e1' }}>{b.velocity}</td>
                <td>
                  <span className={`ba-status-badge ba-status-${b.status.toLowerCase()}`}>
                    {b.status === 'ANOMALOUS' && <ShieldAlert size={12} />}
                    {b.status}
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

const BA_STYLES = `
.ba-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ba-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ba-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ba-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ba-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.ba-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.ba-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.ba-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.ba-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.ba-row td { padding: 12px; }
.ba-pill { display: inline-flex; align-items: center; gap: 4px; padding: 2px 6px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 0.75rem; color: #cbd5e1; }
.ba-status-badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.ba-status-stable { background: rgba(16,185,129,0.15); color: #34d399; }
.ba-status-anomalous { background: rgba(245,158,11,0.15); color: #fbbf24; }
`;
