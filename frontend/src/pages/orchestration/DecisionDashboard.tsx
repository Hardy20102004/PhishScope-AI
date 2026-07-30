import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, BrainCircuit, ThumbsUp, ThumbsDown } from 'lucide-react';

const DECISIONS = [
  { id: '1', ai_recommendation: 'Isolate compromised EC2 instance (i-0b22a) from production VPC', reason: 'Active C2 beaconing detected', status: 'PENDING' },
  { id: '2', ai_recommendation: 'Revoke standing privileges for vendor_admin group', reason: 'Zero Trust policy violation', status: 'AUTHORIZED' },
  { id: '3', ai_recommendation: 'Block inbound IP block 192.168.x.x at WAF', reason: 'Sustained DDoS attempt', status: 'AUTHORIZED' }
];

export default function DecisionDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{DCS_STYLES}</style>
      <div className="dcs-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="dcs-header-icon"><ShieldCheck size={24} /></div>
          <div>
            <h1 className="dcs-title">Decision Intelligence & Governance</h1>
            <p className="dcs-subtitle">AI recommendations awaiting human authorization</p>
          </div>
        </div>
        <Link to="/orchestration" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Orchestration Hub</Link>
      </div>

      <div className="dcs-card">
        <h3 className="dcs-card-title"><BrainCircuit size={16} color="#f59e0b" /> AI Decision Log</h3>
        <table className="dcs-table">
          <thead>
            <tr><th>AI Recommendation</th><th>Explainable Reasoning</th><th>Human Authorization</th></tr>
          </thead>
          <tbody>
            {DECISIONS.map(dec => (
              <tr key={dec.id} className="dcs-row">
                <td style={{ fontWeight: 600 }}>{dec.ai_recommendation}</td>
                <td style={{ color: '#94a3b8' }}>{dec.reason}</td>
                <td>
                  {dec.status === 'PENDING' ? (
                    <div style={{ display: 'flex', gap: 8 }}>
                      <button className="dcs-btn dcs-btn-auth"><ThumbsUp size={14} /> Approve</button>
                      <button className="dcs-btn dcs-btn-deny"><ThumbsDown size={14} /> Deny</button>
                    </div>
                  ) : (
                    <span className="dcs-status-auth"><ShieldCheck size={14} /> {dec.status}</span>
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

const DCS_STYLES = `
.dcs-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.dcs-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.dcs-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.dcs-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.dcs-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.dcs-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.dcs-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.dcs-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.dcs-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.dcs-row td { padding: 12px; }
.dcs-btn { display: inline-flex; align-items: center; gap: 4px; padding: 6px 12px; border: none; border-radius: 6px; font-size: 0.75rem; font-weight: 600; cursor: pointer; color: white; transition: opacity 0.2s; }
.dcs-btn:hover { opacity: 0.9; }
.dcs-btn-auth { background: #10b981; }
.dcs-btn-deny { background: #ef4444; }
.dcs-status-auth { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; background: rgba(16,185,129,0.15); border-radius: 6px; color: #34d399; font-weight: 700; font-size: 0.75rem; }
`;
