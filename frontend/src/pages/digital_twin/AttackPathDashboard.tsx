import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, Crosshair, ArrowRight } from 'lucide-react';

const ATTACK_PATHS = [
  { id: '1', title: 'Phishing -> Helpdesk Exec -> AWS Root', steps: ['External', 'Okta (Compromised)', 'AWS IAM Role', 'S3 Bucket (PII)'], risk: 'CRITICAL', simulated: true },
  { id: '2', title: 'Unpatched VPN -> Admin Subnet -> Domain Controller', steps: ['VPN', 'VLAN 40', 'Active Directory'], risk: 'HIGH', simulated: true }
];

export default function AttackPathDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ATP_STYLES}</style>
      <div className="atp-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="atp-header-icon"><ShieldAlert size={24} /></div>
          <div>
            <h1 className="atp-title">Attack Path Intelligence</h1>
            <p className="atp-subtitle">Discovered paths from external entry points to critical enterprise assets</p>
          </div>
        </div>
        <Link to="/digital-twin" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Digital Twin Home</Link>
      </div>

      <div className="atp-card">
        <h3 className="atp-card-title"><Crosshair size={16} color="#ef4444" /> Top Simulated Attack Choke Points</h3>
        <table className="atp-table">
          <thead>
            <tr><th>Threat Vector Sequence</th><th>Discovered Path</th><th>Risk Level</th></tr>
          </thead>
          <tbody>
            {ATTACK_PATHS.map(path => (
              <tr key={path.id} className="atp-row">
                <td style={{ fontWeight: 600 }}>{path.title}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
                    {path.steps.map((step, idx) => (
                      <React.Fragment key={idx}>
                        <span className="atp-step-badge">{step}</span>
                        {idx < path.steps.length - 1 && <ArrowRight size={12} color="#64748b" />}
                      </React.Fragment>
                    ))}
                  </div>
                </td>
                <td>
                  <span className={`atp-status atp-${path.risk.toLowerCase()}`}>
                    {path.risk}
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

const ATP_STYLES = `
.atp-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.atp-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.atp-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.atp-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.atp-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.atp-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.atp-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.atp-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.atp-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.atp-row td { padding: 12px; }
.atp-step-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; font-size: 0.7rem; color: #cbd5e1; }
.atp-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.atp-critical { background: rgba(239,68,68,0.2); color: #fca5a5; }
.atp-high { background: rgba(249,115,22,0.2); color: #fdba74; }
`;
