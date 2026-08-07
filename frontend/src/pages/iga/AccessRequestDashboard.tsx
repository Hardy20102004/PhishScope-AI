import React from 'react';
import { Link } from 'react-router-dom';
import { Key, CheckCircle, XCircle } from 'lucide-react';

const REQUESTS = [
  { id: 'REQ-889', requester: 'alice.smith', target: 'alice.smith', entitlement: 'AWS Prod DB Admin', justification: 'Need access for Q3 deployment.', status: 'PENDING_APPROVAL', time: '2026-07-30 10:15' },
  { id: 'REQ-890', requester: 'manager.bob', target: 'new.contractor', entitlement: 'VPN Access', justification: 'Onboarding external vendor.', status: 'APPROVED', time: '2026-07-30 11:00' }
];

export default function AccessRequestDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{AR_STYLES}</style>
      <div className="ar-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ar-header-icon"><Key size={24} /></div>
          <div>
            <h1 className="ar-title">Access Requests</h1>
            <p className="ar-subtitle">Manage, approve, and audit entitlement requests</p>
          </div>
        </div>
        <Link to="/iga" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← IGA</Link>
      </div>

      <div className="ar-card">
        <h3 className="ar-card-title">Pending & Recent Requests</h3>
        <table className="ar-table">
          <thead>
            <tr><th>Request ID</th><th>Requester</th><th>Target</th><th>Requested Entitlement</th><th>Justification</th><th>Status</th><th>Submitted</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {REQUESTS.map(req => (
              <tr key={req.id} className="ar-row">
                <td style={{ fontWeight: 600, color: '#818cf8' }}>{req.id}</td>
                <td>{req.requester}</td>
                <td style={{ color: '#94a3b8' }}>{req.target}</td>
                <td><span className="ar-ent-badge">{req.entitlement}</span></td>
                <td style={{ fontSize: '0.8rem', color: '#cbd5e1', maxWidth: 200, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{req.justification}</td>
                <td><span className={`ar-status ar-${req.status.toLowerCase()}`}>{req.status.replace('_', ' ')}</span></td>
                <td style={{ color: '#64748b', fontSize: '0.8rem' }}>{req.time}</td>
                <td>
                  {req.status === 'PENDING_APPROVAL' && (
                    <div style={{ display: 'flex', gap: 6 }}>
                      <button className="ar-btn ar-btn-approve"><CheckCircle size={12} /> Approve</button>
                      <button className="ar-btn ar-btn-reject"><XCircle size={12} /> Reject</button>
                    </div>
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

const AR_STYLES = `
.ar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ar-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ar-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ar-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ar-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.ar-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.ar-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.ar-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.ar-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.ar-row td { padding: 12px; }
.ar-ent-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.75rem; }
.ar-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.ar-pending_approval { background: rgba(245,158,11,0.15); color: #fbbf24; }
.ar-approved { background: rgba(59,130,246,0.15); color: #60a5fa; }
.ar-btn { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 4px; border: none; font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.ar-btn:hover { opacity: 0.8; }
.ar-btn-approve { background: #10b981; color: white; }
.ar-btn-reject { background: rgba(239,68,68,0.2); color: #fca5a5; }
`;
