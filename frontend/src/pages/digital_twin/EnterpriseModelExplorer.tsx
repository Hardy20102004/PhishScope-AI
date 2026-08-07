import React from 'react';
import { Link } from 'react-router-dom';
import { Network, Database, Cloud, Users, ShieldAlert } from 'lucide-react';

const NODES = [
  { id: '1', name: 'AWS Prod EKS', type: 'Cloud', risk: 'HIGH', connections: 24 },
  { id: '2', name: 'Okta Primary Directory', type: 'Identity', risk: 'MEDIUM', connections: 145 },
  { id: '3', name: 'Customer DB (RDS)', type: 'Data', risk: 'CRITICAL', connections: 8 }
];

export default function EnterpriseModelExplorer() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{EXP_STYLES}</style>
      <div className="exp-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="exp-header-icon"><Network size={24} /></div>
          <div>
            <h1 className="exp-title">Enterprise Model Explorer</h1>
            <p className="exp-subtitle">Graph-based visualization of assets, identities, and trust relationships</p>
          </div>
        </div>
        <Link to="/digital-twin" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Digital Twin Home</Link>
      </div>

      <div className="exp-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 className="exp-card-title"><Database size={16} color="#3b82f6" /> Asset Graph Topology (Preview)</h3>
          <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Total Nodes: 14,502 | Edges: 42,109</span>
        </div>
        
        {/* Placeholder for actual 3D Graph (e.g. ForceGraph3D) */}
        <div className="exp-graph-placeholder">
          <div className="exp-placeholder-text">Interactive 3D Graph Rendering Canvas</div>
          <div style={{ display: 'flex', gap: 16, marginTop: 16 }}>
            <span className="exp-badge"><Cloud size={14} color="#0ea5e9"/> Cloud (AWS/Azure/GCP)</span>
            <span className="exp-badge"><Users size={14} color="#8b5cf6"/> Identity (Okta/AD)</span>
            <span className="exp-badge"><ShieldAlert size={14} color="#ef4444"/> Critical Risk Node</span>
          </div>
        </div>

        <table className="exp-table" style={{ marginTop: 24 }}>
          <thead>
            <tr><th>Critical Node</th><th>Domain</th><th>Connected Edges</th><th>Twin Risk Level</th></tr>
          </thead>
          <tbody>
            {NODES.map(node => (
              <tr key={node.id} className="exp-row">
                <td style={{ fontWeight: 600 }}>{node.name}</td>
                <td style={{ color: '#94a3b8' }}>{node.type}</td>
                <td>{node.connections}</td>
                <td>
                  <span className={`exp-status exp-${node.risk.toLowerCase()}`}>
                    {node.risk}
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

const EXP_STYLES = `
.exp-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.exp-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.exp-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.exp-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.exp-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.exp-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0; }
.exp-graph-placeholder { height: 300px; background: rgba(0,0,0,0.4); border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.exp-placeholder-text { font-size: 0.9rem; color: #64748b; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; }
.exp-badge { display: flex; align-items: center; gap: 6px; padding: 4px 10px; background: rgba(255,255,255,0.05); border-radius: 16px; font-size: 0.75rem; color: #cbd5e1; }
.exp-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.exp-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.exp-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.exp-row td { padding: 12px; }
.exp-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.exp-critical { background: rgba(239,68,68,0.2); color: #fca5a5; }
.exp-high { background: rgba(249,115,22,0.2); color: #fdba74; }
.exp-medium { background: rgba(234,179,8,0.2); color: #fde047; }
`;
