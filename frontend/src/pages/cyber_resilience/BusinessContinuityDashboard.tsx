import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Clock } from 'lucide-react';

const SERVICES = [
  { id: '1', name: 'Global Identity Auth', tier: 'MISSION_CRITICAL', rto: '15m', rpo: '5m', deps: 12 },
  { id: '2', name: 'Customer Payment Gateway', tier: 'MISSION_CRITICAL', rto: '30m', rpo: '15m', deps: 8 },
  { id: '3', name: 'Internal HR Portal', tier: 'SUPPORTING', rto: '24h', rpo: '12h', deps: 3 }
];

export default function BusinessContinuityDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{BCP_STYLES}</style>
      <div className="bcp-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="bcp-header-icon"><Activity size={24} /></div>
          <div>
            <h1 className="bcp-title">Business Continuity</h1>
            <p className="bcp-subtitle">Critical services, dependencies, and recovery objectives</p>
          </div>
        </div>
        <Link to="/cyber-resilience" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Resilience Home</Link>
      </div>

      <div className="bcp-card">
        <h3 className="bcp-card-title"><Clock size={16} color="#3b82f6" /> Recovery Objectives (RTO / RPO)</h3>
        <table className="bcp-table">
          <thead>
            <tr><th>Business Service</th><th>Criticality Tier</th><th>RTO</th><th>RPO</th><th>Mapped Dependencies</th></tr>
          </thead>
          <tbody>
            {SERVICES.map(s => (
              <tr key={s.id} className="bcp-row">
                <td style={{ fontWeight: 600 }}>{s.name}</td>
                <td>
                  <span className={`bcp-badge bcp-${s.tier.toLowerCase()}`}>
                    {s.tier.replace('_', ' ')}
                  </span>
                </td>
                <td><span className="bcp-mono">{s.rto}</span></td>
                <td><span className="bcp-mono">{s.rpo}</span></td>
                <td style={{ color: '#94a3b8' }}>{s.deps} Assets</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const BCP_STYLES = `
.bcp-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.bcp-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.bcp-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.bcp-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.bcp-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.bcp-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.bcp-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.bcp-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.bcp-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.bcp-row td { padding: 12px; }
.bcp-mono { font-family: monospace; font-size: 0.95rem; color: #e2e8f0; }
.bcp-badge { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.bcp-mission_critical { background: rgba(239,68,68,0.15); color: #f87171; }
.bcp-supporting { background: rgba(148,163,184,0.15); color: #cbd5e1; }
`;
