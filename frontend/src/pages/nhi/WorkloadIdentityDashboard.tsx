import React from 'react';
import { Link } from 'react-router-dom';
import { Server, Activity } from 'lucide-react';

const WORKLOADS = [
  { id: '1', name: 'payment-processor-pod', type: 'K8S_SERVICE_ACCOUNT', cluster: 'us-east-prod-01', namespace: 'payments', status: 'ACTIVE' },
  { id: '2', name: 'image-resizer-lambda', type: 'SERVERLESS_FUNCTION', cluster: 'AWS Lambda', namespace: 'media', status: 'ACTIVE' }
];

export default function WorkloadIdentityDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{WL_STYLES}</style>
      <div className="wl-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="wl-header-icon"><Server size={24} /></div>
          <div>
            <h1 className="wl-title">Workload Identities</h1>
            <p className="wl-subtitle">Ephemeral and dynamic identities for containers and serverless functions</p>
          </div>
        </div>
        <Link to="/nhi" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← NHI Dashboard</Link>
      </div>

      <div className="wl-card">
        <h3 className="wl-card-title"><Activity size={16} /> Active Workloads</h3>
        <table className="wl-table">
          <thead>
            <tr><th>Workload Identity</th><th>Type</th><th>Cluster / Environment</th><th>Namespace</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            {WORKLOADS.map(wl => (
              <tr key={wl.id} className="wl-row">
                <td style={{ fontWeight: 600 }}>{wl.name}</td>
                <td><span className="wl-type-badge">{wl.type.replace(/_/g, ' ')}</span></td>
                <td style={{ color: '#94a3b8' }}>{wl.cluster}</td>
                <td style={{ color: '#cbd5e1' }}>{wl.namespace}</td>
                <td><span className={`wl-status wl-${wl.status.toLowerCase()}`}>{wl.status}</span></td>
                <td>
                  <button className="wl-btn-view">Inspect</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const WL_STYLES = `
.wl-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.wl-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.wl-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.wl-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.wl-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.wl-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.wl-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.wl-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.wl-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.wl-row td { padding: 12px; }
.wl-type-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.75rem; }
.wl-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.wl-active { background: rgba(16,185,129,0.15); color: #34d399; }
.wl-btn-view { padding: 6px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #e2e8f0; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.wl-btn-view:hover { background: rgba(255,255,255,0.1); }
`;
