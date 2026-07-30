import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, FileText, CheckCircle, Clock } from 'lucide-react';

const POLICIES = [
  { id: '1', name: 'Require MFA for Privileged Access', status: 'ACTIVE', priority: 10, effect: 'CHALLENGE', updated: '2026-07-28' },
  { id: '2', name: 'Block High Risk Sessions', status: 'ACTIVE', priority: 20, effect: 'DENY', updated: '2026-07-25' },
  { id: '3', name: 'Require Managed Device for Prod AWS', status: 'ACTIVE', priority: 30, effect: 'DENY', updated: '2026-07-20' },
  { id: '4', name: 'Step-up Auth on Anomalous Location', status: 'INACTIVE', priority: 40, effect: 'CHALLENGE', updated: '2026-07-15' },
];

const APPROVALS = [
  { id: '1', policy: 'Step-up Auth on Anomalous Location', requested_by: 'alice.security', status: 'PENDING', justification: 'Rolling out phase 2 location checks.' }
];

export default function PolicyGovernanceDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PG_STYLES}</style>
      <div className="pg-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="pg-header-icon"><Shield size={24} /></div>
          <div>
            <h1 className="pg-title">Policy Governance</h1>
            <p className="pg-subtitle">Manage Zero Trust policies and approval workflows</p>
          </div>
        </div>
        <Link to="/zta" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ZTA</Link>
      </div>

      <div className="pg-grid">
        <div className="pg-card">
          <h3 className="pg-card-title"><FileText size={16} /> Active Policies</h3>
          <table className="pg-table">
            <thead>
              <tr><th>Name</th><th>Priority</th><th>Effect</th><th>Status</th></tr>
            </thead>
            <tbody>
              {POLICIES.map(p => (
                <tr key={p.id} className="pg-row">
                  <td style={{ fontWeight: 500 }}>{p.name}</td>
                  <td style={{ color: '#94a3b8' }}>{p.priority}</td>
                  <td><span className={`pg-effect pg-${p.effect.toLowerCase()}`}>{p.effect}</span></td>
                  <td>
                    <span className={`pg-status ${p.status === 'ACTIVE' ? 'active' : 'inactive'}`}>
                      {p.status === 'ACTIVE' ? <CheckCircle size={12} /> : <Clock size={12} />} {p.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="pg-card">
          <h3 className="pg-card-title"><Clock size={16} /> Pending Approvals</h3>
          {APPROVALS.map(a => (
            <div key={a.id} className="pg-approval-item">
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{a.policy}</strong>
                <span className="pg-badge-pending">PENDING</span>
              </div>
              <p style={{ margin: '0 0 6px', fontSize: '0.8rem', color: '#94a3b8' }}>Requested by: <strong>{a.requested_by}</strong></p>
              <p style={{ margin: 0, fontSize: '0.8rem', color: '#64748b', fontStyle: 'italic' }}>"{a.justification}"</p>
              <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
                <button className="pg-btn pg-btn-approve">Approve</button>
                <button className="pg-btn pg-btn-deny">Deny</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const PG_STYLES = `
.pg-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.pg-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.pg-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.pg-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.pg-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .pg-grid { grid-template-columns: 1fr; } }
.pg-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.pg-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.pg-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.pg-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.pg-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.pg-row td { padding: 12px; }
.pg-effect { padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.pg-challenge { background: rgba(245,158,11,0.15); color: #fbbf24; }
.pg-deny { background: rgba(239,68,68,0.15); color: #f87171; }
.pg-status { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 500; }
.pg-status.active { background: rgba(16,185,129,0.1); color: #34d399; }
.pg-status.inactive { background: rgba(255,255,255,0.05); color: #94a3b8; }
.pg-approval-item { padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; }
.pg-badge-pending { padding: 2px 6px; background: rgba(245,158,11,0.15); color: #fbbf24; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.pg-btn { padding: 6px 12px; border-radius: 6px; border: none; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.pg-btn:hover { opacity: 0.8; }
.pg-btn-approve { background: #10b981; color: #fff; }
.pg-btn-deny { background: rgba(239,68,68,0.2); color: #fca5a5; }
`;
