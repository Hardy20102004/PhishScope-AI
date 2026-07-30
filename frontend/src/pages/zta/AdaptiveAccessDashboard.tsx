import React from 'react';
import { Link } from 'react-router-dom';
import { Lock, Shield, CheckCircle, XCircle, AlertTriangle, Key } from 'lucide-react';

const DECISIONS = [
  { id: '1', time: '10:45:12', identity: 'maria.garcia@corp.com', resource: 'Finance ERP (Production)', decision: 'ALLOW', policy: 'POL-FIN-01', rationale: 'Device managed, MFA verified, IP trusted' },
  { id: '2', time: '10:44:30', identity: 'david.chen@corp.com', resource: 'AWS Prod Console', decision: 'STEP_UP_AUTH', policy: 'POL-AWS-05', rationale: 'Anomalous location detected, require FIDO2' },
  { id: '3', time: '10:42:15', identity: 'machine-k8s-02', resource: 'Customer DB API', decision: 'DENY', policy: 'POL-DATA-02', rationale: 'Workload identity mismatch, failed attestation' },
  { id: '4', time: '10:40:01', identity: 'app-oauth-github', resource: 'Source Code Repo', decision: 'ALLOW', policy: 'POL-DEV-01', rationale: 'OIDC token valid, scope matched' }
];

export default function AdaptiveAccessDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{AA_STYLES}</style>
      <div className="aa-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="aa-header-icon"><Lock size={24} /></div>
          <div>
            <h1 className="aa-title">Adaptive Access</h1>
            <p className="aa-subtitle">Context-aware access decisions and policy enforcements</p>
          </div>
        </div>
        <Link to="/zta" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ZTA</Link>
      </div>

      <div className="aa-table-card">
        <h3 className="aa-card-title">Recent Access Decisions</h3>
        <table className="aa-table">
          <thead>
            <tr>
              <th>Time</th><th>Identity</th><th>Requested Resource</th><th>Decision</th><th>Matched Policy</th><th>Rationale</th>
            </tr>
          </thead>
          <tbody>
            {DECISIONS.map(d => (
              <tr key={d.id} className="aa-row">
                <td style={{ color: '#64748b' }}>{d.time}</td>
                <td style={{ fontWeight: 500 }}>{d.identity}</td>
                <td style={{ color: '#94a3b8' }}>{d.resource}</td>
                <td>
                  <span className={`aa-decision aa-${d.decision.toLowerCase()}`}>
                    {d.decision === 'ALLOW' && <CheckCircle size={14} />}
                    {d.decision === 'DENY' && <XCircle size={14} />}
                    {d.decision === 'STEP_UP_AUTH' && <Key size={14} />}
                    {d.decision.replace(/_/g, ' ')}
                  </span>
                </td>
                <td><span className="aa-policy">{d.policy}</span></td>
                <td style={{ color: '#64748b', fontSize: '0.8rem' }}>{d.rationale}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const AA_STYLES = `
.aa-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.aa-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.aa-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.aa-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.aa-table-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.aa-card-title { font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.aa-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.aa-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.aa-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.aa-row td { padding: 12px; }
.aa-decision { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
.aa-allow { background: rgba(16,185,129,0.15); color: #34d399; }
.aa-deny { background: rgba(239,68,68,0.15); color: #f87171; }
.aa-step_up_auth { background: rgba(245,158,11,0.15); color: #fbbf24; }
.aa-policy { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.8rem; color: #cbd5e1; }
`;
