import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, CheckCircle, XCircle, AlertCircle, Plus } from 'lucide-react';

const REQUESTS = [
  { id: '1', requester: 'alice.security', role: 'AWS Prod DB Admin', duration: '2h', status: 'ACTIVE', activated: '2026-07-30 10:00' },
  { id: '2', requester: 'bob.devops', role: 'K8s Cluster Admin', duration: '4h', status: 'PENDING_APPROVAL', activated: '-' },
  { id: '3', requester: 'charlie.net', role: 'Network Admin', duration: '1h', status: 'REJECTED', activated: '-' },
  { id: '4', requester: 'david.eng', role: 'Entra Global Admin', duration: '1h', status: 'EXPIRED', activated: '2026-07-29 14:00' }
];

export default function JITAccessDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{JIT_STYLES}</style>
      <div className="jit-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="jit-header-icon"><Clock size={24} /></div>
          <div>
            <h1 className="jit-title">Just-In-Time (JIT) Access</h1>
            <p className="jit-subtitle">Manage temporary privilege elevation requests and active sessions</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <button className="jit-btn-primary"><Plus size={16} /> New Request</button>
          <Link to="/pam" style={{ color: '#818cf8', textDecoration: 'none', alignSelf: 'center', fontSize: '0.85rem', marginLeft: 8 }}>← PAM</Link>
        </div>
      </div>

      <div className="jit-card">
        <h3 className="jit-card-title">JIT Elevation Requests</h3>
        <table className="jit-table">
          <thead>
            <tr><th>Requester</th><th>Requested Role</th><th>Duration</th><th>Status</th><th>Activated At</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {REQUESTS.map(req => (
              <tr key={req.id} className="jit-row">
                <td style={{ fontWeight: 500 }}>{req.requester}</td>
                <td><span className="jit-role-badge">{req.role}</span></td>
                <td style={{ color: '#94a3b8' }}>{req.duration}</td>
                <td>
                  <span className={`jit-status jit-${req.status.toLowerCase()}`}>
                    {req.status === 'ACTIVE' && <CheckCircle size={12} />}
                    {req.status === 'PENDING_APPROVAL' && <Clock size={12} />}
                    {req.status === 'REJECTED' && <XCircle size={12} />}
                    {req.status === 'EXPIRED' && <AlertCircle size={12} />}
                    {req.status.replace('_', ' ')}
                  </span>
                </td>
                <td style={{ color: '#64748b' }}>{req.activated}</td>
                <td>
                  {req.status === 'PENDING_APPROVAL' && (
                    <div style={{ display: 'flex', gap: 6 }}>
                      <button className="jit-action-btn jit-btn-approve">Approve</button>
                      <button className="jit-action-btn jit-btn-reject">Reject</button>
                    </div>
                  )}
                  {req.status === 'ACTIVE' && (
                    <button className="jit-action-btn jit-btn-revoke">Revoke</button>
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

const JIT_STYLES = `
.jit-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.jit-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.jit-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.jit-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.jit-btn-primary { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; background: #10b981; border: none; border-radius: 8px; color: white; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.jit-btn-primary:hover { background: #059669; }
.jit-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.jit-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.jit-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.jit-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.jit-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.jit-row td { padding: 12px; }
.jit-role-badge { padding: 4px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.8rem; }
.jit-status { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
.jit-active { background: rgba(16,185,129,0.15); color: #34d399; }
.jit-pending_approval { background: rgba(245,158,11,0.15); color: #fbbf24; }
.jit-rejected { background: rgba(239,68,68,0.15); color: #f87171; }
.jit-expired { background: rgba(255,255,255,0.05); color: #94a3b8; }
.jit-action-btn { padding: 4px 10px; border-radius: 4px; border: none; font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.jit-action-btn:hover { opacity: 0.8; }
.jit-btn-approve { background: #10b981; color: white; }
.jit-btn-reject { background: rgba(239,68,68,0.2); color: #fca5a5; }
.jit-btn-revoke { background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
`;
