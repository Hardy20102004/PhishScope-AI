import React from 'react';
import { Link } from 'react-router-dom';
import { Users, Shield, Server, Search, Filter } from 'lucide-react';

const IDENTITIES = [
  { id: '1', name: 'Global Admin Service', principal: 'global_admin@corp.com', platform: 'Entra ID', type: 'SERVICE_ACCOUNT', standing: true, risk: 'LOW' },
  { id: '2', name: 'AWS Prod DB Admin', principal: 'aws-prod-dba', platform: 'AWS IAM', type: 'ADMINISTRATOR', standing: false, risk: 'LOW' },
  { id: '3', name: 'K8s Cluster Admin', principal: 'cluster-admin-01', platform: 'Kubernetes', type: 'MACHINE_IDENTITY', standing: true, risk: 'HIGH' },
  { id: '4', name: 'Emergency Break-Glass', principal: 'breakglass_01@corp.com', platform: 'Entra ID', type: 'BREAK_GLASS', standing: true, risk: 'LOW' }
];

export default function PrivilegedIdentityDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PI_STYLES}</style>
      <div className="pi-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="pi-header-icon"><Users size={24} /></div>
          <div>
            <h1 className="pi-title">Privileged Identity Inventory</h1>
            <p className="pi-subtitle">Discovery and oversight of all administrative and service accounts</p>
          </div>
        </div>
        <Link to="/pam" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← PAM</Link>
      </div>

      <div className="pi-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
          <h3 className="pi-card-title">Discovered Identities</h3>
          <div style={{ display: 'flex', gap: 10 }}>
            <div className="pi-search-box">
              <Search size={14} color="#64748b" />
              <input type="text" placeholder="Search identities..." />
            </div>
            <button className="pi-filter-btn"><Filter size={14} /> Filter</button>
          </div>
        </div>
        
        <table className="pi-table">
          <thead>
            <tr><th>Display Name</th><th>Principal</th><th>Platform</th><th>Type</th><th>Standing Access</th><th>Risk</th></tr>
          </thead>
          <tbody>
            {IDENTITIES.map(id => (
              <tr key={id.id} className="pi-row">
                <td style={{ fontWeight: 600 }}>{id.name}</td>
                <td style={{ color: '#94a3b8' }}>{id.principal}</td>
                <td><span className="pi-platform-badge">{id.platform}</span></td>
                <td style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>{id.type.replace('_', ' ')}</td>
                <td>
                  {id.standing ? 
                    <span className="pi-standing-yes">YES</span> : 
                    <span className="pi-standing-no">JIT ONLY</span>}
                </td>
                <td><span className={`pi-risk-badge pi-risk-${id.risk.toLowerCase()}`}>{id.risk}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const PI_STYLES = `
.pi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.pi-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.pi-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.pi-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.pi-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.pi-card-title { font-size: 1rem; font-weight: 600; margin: 0; }
.pi-search-box { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); }
.pi-search-box input { background: transparent; border: none; outline: none; color: white; font-size: 0.8rem; }
.pi-filter-btn { display: flex; align-items: center; gap: 6px; padding: 6px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; cursor: pointer; }
.pi-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.pi-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.pi-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.pi-row td { padding: 12px; }
.pi-platform-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 0.75rem; }
.pi-standing-yes { padding: 3px 8px; background: rgba(239,68,68,0.15); color: #f87171; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }
.pi-standing-no { padding: 3px 8px; background: rgba(16,185,129,0.15); color: #34d399; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }
.pi-risk-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.pi-risk-high { background: rgba(245,158,11,0.15); color: #fbbf24; }
.pi-risk-low { background: rgba(59,130,246,0.15); color: #60a5fa; }
`;
