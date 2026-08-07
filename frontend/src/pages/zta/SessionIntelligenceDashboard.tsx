import React from 'react';
import { Link } from 'react-router-dom';
import { Server, Activity, AlertCircle, ShieldOff, Play } from 'lucide-react';

const SESSIONS = [
  { id: '1', identity: 'david.chen@corp.com', device: 'mac-dc-01', risk: 'LOW', anomalies: 0, uptime: '4h 12m', status: 'ACTIVE' },
  { id: '2', identity: 'maria.garcia@corp.com', device: 'win-mg-04', risk: 'MEDIUM', anomalies: 1, uptime: '1h 05m', status: 'ACTIVE' },
  { id: '3', identity: 'svc-data-sync', device: 'k8s-pod-77x', risk: 'HIGH', anomalies: 3, uptime: '14d 2h', status: 'ACTIVE' },
  { id: '4', identity: 'guest.vendor@ext.com', device: 'unknown', risk: 'CRITICAL', anomalies: 5, uptime: '0h 15m', status: 'REVOKED' }
];

export default function SessionIntelligenceDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{SI_STYLES}</style>
      <div className="si-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="si-header-icon"><Server size={24} /></div>
          <div>
            <h1 className="si-title">Session Intelligence</h1>
            <p className="si-subtitle">Monitor session health, risk context, and anomalies in real-time</p>
          </div>
        </div>
        <Link to="/zta" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ZTA</Link>
      </div>

      <div className="si-card">
        <h3 className="si-card-title"><Activity size={16} /> Active Sessions Watchlist</h3>
        <table className="si-table">
          <thead>
            <tr><th>Identity</th><th>Device</th><th>Session Uptime</th><th>Anomalies</th><th>Risk Level</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {SESSIONS.map(s => (
              <tr key={s.id} className="si-row">
                <td style={{ fontWeight: 500 }}>{s.identity}</td>
                <td style={{ color: '#94a3b8' }}>{s.device}</td>
                <td style={{ color: '#cbd5e1' }}>{s.uptime}</td>
                <td>
                  <span style={{ color: s.anomalies > 0 ? '#f59e0b' : '#64748b', fontWeight: s.anomalies > 0 ? 700 : 400 }}>
                    {s.anomalies}
                  </span>
                </td>
                <td>
                  <span className={`si-risk-badge si-risk-${s.risk.toLowerCase()}`}>{s.risk}</span>
                </td>
                <td>
                  {s.status === 'ACTIVE' ? (
                    <button className="si-btn-revoke"><ShieldOff size={12} /> Revoke</button>
                  ) : (
                    <span style={{ color: '#f87171', fontSize: '0.75rem', fontWeight: 600 }}>REVOKED</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const SI_STYLES = `
.si-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.si-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #06b6d4, #0891b2); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.si-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.si-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.si-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.si-card-title { font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; display: flex; align-items: center; gap: 8px; }
.si-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.si-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.si-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.si-row td { padding: 12px; }
.si-risk-badge { padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }
.si-risk-critical { background: rgba(239,68,68,0.15); color: #f87171; }
.si-risk-high { background: rgba(245,158,11,0.15); color: #fbbf24; }
.si-risk-medium { background: rgba(59,130,246,0.15); color: #60a5fa; }
.si-risk-low { background: rgba(16,185,129,0.15); color: #34d399; }
.si-btn-revoke { display: inline-flex; align-items: center; gap: 4px; padding: 6px 10px; background: rgba(239,68,68,0.1); color: #f87171; border: 1px solid rgba(239,68,68,0.3); border-radius: 6px; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: all 0.2s; }
.si-btn-revoke:hover { background: rgba(239,68,68,0.2); }
`;
