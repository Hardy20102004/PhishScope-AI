import React from 'react';
import { Link } from 'react-router-dom';
import { PlayCircle, Settings, ShieldCheck } from 'lucide-react';

const PLAYBOOKS = [
  { id: '1', name: 'Ransomware Containment', version: '2.4.1', type: 'Incident Response', requires_approval: true },
  { id: '2', name: 'AWS JIT Elevation', version: '1.2.0', type: 'Identity Governance', requires_approval: true },
  { id: '3', name: 'Malicious IP Block (Firewall)', version: '3.0.1', type: 'Automated Remediation', requires_approval: false }
];

export default function PlaybookDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{PLY_STYLES}</style>
      <div className="ply-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ply-header-icon"><PlayCircle size={24} /></div>
          <div>
            <h1 className="ply-title">Playbook Governance</h1>
            <p className="ply-subtitle">Standard Operating Procedures and Automation Flows</p>
          </div>
        </div>
        <Link to="/orchestration" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Orchestration Hub</Link>
      </div>

      <div className="ply-card">
        <h3 className="ply-card-title"><Settings size={16} color="#8b5cf6" /> Active Playbook Definitions</h3>
        <table className="ply-table">
          <thead>
            <tr><th>Playbook Name</th><th>Category</th><th>Version</th><th>Approval Gate</th></tr>
          </thead>
          <tbody>
            {PLAYBOOKS.map(pb => (
              <tr key={pb.id} className="ply-row">
                <td style={{ fontWeight: 600 }}>{pb.name}</td>
                <td style={{ color: '#94a3b8' }}>{pb.type}</td>
                <td><span className="ply-version">v{pb.version}</span></td>
                <td>
                  {pb.requires_approval ? (
                    <span className="ply-status ply-manual"><ShieldCheck size={12} /> Human Review</span>
                  ) : (
                    <span className="ply-status ply-auto">Fully Autonomous</span>
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

const PLY_STYLES = `
.ply-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ply-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #6d28d9); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.ply-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.ply-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.ply-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.ply-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.ply-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.ply-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.ply-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.ply-row td { padding: 12px; }
.ply-version { padding: 2px 6px; background: rgba(255,255,255,0.05); border-radius: 4px; font-family: monospace; font-size: 0.75rem; color: #cbd5e1; }
.ply-status { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.ply-manual { background: rgba(245,158,11,0.15); color: #fbbf24; }
.ply-auto { background: rgba(16,185,129,0.15); color: #34d399; }
`;
