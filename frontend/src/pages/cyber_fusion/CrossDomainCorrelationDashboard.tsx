import React from 'react';
import { Link } from 'react-router-dom';
import { Share2, AlertOctagon } from 'lucide-react';

const CORRELATIONS = [
  { id: '1', title: 'Suspicious Okta Login -> AWS EC2 Spawn -> C2 Beacon', severity: 'CRITICAL', modules: ['Identity', 'Cloud', 'Network'] },
  { id: '2', title: 'Stale Service Account -> Vault Secrets Access', severity: 'HIGH', modules: ['Identity', 'AppSec'] },
  { id: '3', title: 'GitHub Repo Public -> Hardcoded AWS Key', severity: 'CRITICAL', modules: ['AppSec', 'Cloud'] }
];

export default function CrossDomainCorrelationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CDC_STYLES}</style>
      <div className="cdc-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="cdc-header-icon"><Share2 size={24} /></div>
          <div>
            <h1 className="cdc-title">Cross-Domain Correlation Engine</h1>
            <p className="cdc-subtitle">Attack chains bridging disparate security platforms</p>
          </div>
        </div>
        <Link to="/cyber-fusion" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Cyber Fusion Center</Link>
      </div>

      <div className="cdc-card">
        <h3 className="cdc-card-title"><AlertOctagon size={16} color="#ef4444" /> Active Multi-Domain Threat Chains</h3>
        <table className="cdc-table">
          <thead>
            <tr><th>Correlated Threat Sequence</th><th>Cross-Domain Breadth</th><th>Risk Severity</th></tr>
          </thead>
          <tbody>
            {CORRELATIONS.map(cor => (
              <tr key={cor.id} className="cdc-row">
                <td style={{ fontWeight: 600 }}>{cor.title}</td>
                <td>
                  <div style={{ display: 'flex', gap: 6 }}>
                    {cor.modules.map(mod => (
                      <span key={mod} className="cdc-module-badge">{mod}</span>
                    ))}
                  </div>
                </td>
                <td>
                  <span className={`cdc-status cdc-${cor.severity.toLowerCase()}`}>
                    {cor.severity}
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

const CDC_STYLES = `
.cdc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.cdc-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.cdc-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.cdc-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.cdc-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.cdc-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.cdc-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.cdc-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.cdc-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.cdc-row td { padding: 12px; }
.cdc-module-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; font-size: 0.7rem; color: #cbd5e1; }
.cdc-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.cdc-critical { background: rgba(239,68,68,0.2); color: #fca5a5; }
.cdc-high { background: rgba(249,115,22,0.2); color: #fdba74; }
`;
