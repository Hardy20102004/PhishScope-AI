import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Shield, Monitor, Network, Users, CheckCircle, XCircle, ChevronRight, AlertTriangle } from 'lucide-react';

const LOGS = [
  { id: '1', time: '10:42:15', type: 'IDENTITY', entity: 'david.chen@corp.com', status: 'VALID', rationale: 'Identity active, MFA recent', confidence: 0.98 },
  { id: '2', time: '10:42:14', type: 'DEVICE', entity: 'mac-dc-01', status: 'INVALID', rationale: 'Device unmanaged, OS outdated', confidence: 0.95 },
  { id: '3', time: '10:42:11', type: 'NETWORK', entity: 'IP: 192.168.1.45', status: 'VALID', rationale: 'Known corporate VPN', confidence: 0.99 },
  { id: '4', time: '10:42:08', type: 'SESSION', entity: 'sess_9a8b7c', status: 'INVALID', rationale: 'Anomalous velocity detected', confidence: 0.88 },
  { id: '5', time: '10:42:05', type: 'IDENTITY', entity: 'svc-payroll-api', status: 'VALID', rationale: 'Service account behavior nominal', confidence: 0.92 }
];

export default function ContinuousVerificationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CV_STYLES}</style>
      <div className="cv-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="cv-header-icon"><Activity size={24} /></div>
          <div>
            <h1 className="cv-title">Continuous Verification</h1>
            <p className="cv-subtitle">Real-time telemetry across Identity, Device, Network, and Session</p>
          </div>
        </div>
        <Link to="/zta" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ZTA</Link>
      </div>

      <div className="cv-table-card">
        <h3 className="cv-card-title">Live Verification Stream</h3>
        <table className="cv-table">
          <thead>
            <tr>
              <th>Time</th><th>Type</th><th>Entity</th><th>Status</th><th>Rationale</th><th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {LOGS.map(log => (
              <tr key={log.id} className="cv-row">
                <td style={{ color: '#64748b' }}>{log.time}</td>
                <td>
                  <span className="cv-type-badge">
                    {log.type === 'IDENTITY' && <Users size={12} />}
                    {log.type === 'DEVICE' && <Monitor size={12} />}
                    {log.type === 'NETWORK' && <Network size={12} />}
                    {log.type === 'SESSION' && <Activity size={12} />}
                    {log.type}
                  </span>
                </td>
                <td style={{ fontWeight: 500 }}>{log.entity}</td>
                <td>
                  {log.status === 'VALID' ? 
                    <span className="cv-status valid"><CheckCircle size={14} /> VALID</span> : 
                    <span className="cv-status invalid"><XCircle size={14} /> INVALID</span>}
                </td>
                <td style={{ color: '#94a3b8' }}>{log.rationale}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <div style={{ width: 40, height: 4, background: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                      <div style={{ width: `${log.confidence * 100}%`, height: '100%', background: '#6366f1' }} />
                    </div>
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{log.confidence.toFixed(2)}</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const CV_STYLES = `
.cv-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.cv-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.cv-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.cv-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.cv-table-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.cv-card-title { font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.cv-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.cv-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.cv-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.cv-row td { padding: 12px; }
.cv-type-badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; background: rgba(255,255,255,0.05); border-radius: 6px; font-size: 0.75rem; color: #cbd5e1; }
.cv-status { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
.cv-status.valid { background: rgba(16,185,129,0.15); color: #34d399; }
.cv-status.invalid { background: rgba(239,68,68,0.15); color: #f87171; }
`;
