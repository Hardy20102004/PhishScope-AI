import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, ShieldAlert } from 'lucide-react';

const ATTACK_SURFACE = [
  { id: '1', asset: 'AWS Prod EKS Cluster', type: 'Cloud Workload', vulnerabilities: 12, misconfigurations: 3, risk: 'HIGH' },
  { id: '2', asset: 'Customer Portal API', type: 'AppSec (DAST)', vulnerabilities: 4, misconfigurations: 0, risk: 'MEDIUM' },
  { id: '3', asset: 'Azure AD Tenant', type: 'Identity Posture', vulnerabilities: 0, misconfigurations: 1, risk: 'CRITICAL' }
];

export default function AttackSurfaceDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{UAS_STYLES}</style>
      <div className="uas-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="uas-header-icon"><Activity size={24} /></div>
          <div>
            <h1 className="uas-title">Unified Attack Surface</h1>
            <p className="uas-subtitle">Aggregated vulnerabilities and misconfigurations across Cloud, App, and Identity</p>
          </div>
        </div>
        <Link to="/cyber-fusion" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Cyber Fusion Center</Link>
      </div>

      <div className="uas-card">
        <h3 className="uas-card-title"><ShieldAlert size={16} color="#3b82f6" /> Enterprise Exposure Map</h3>
        <table className="uas-table">
          <thead>
            <tr><th>Asset / Domain</th><th>Asset Type</th><th>Vulns</th><th>Misconfigs</th><th>Aggregated Risk</th></tr>
          </thead>
          <tbody>
            {ATTACK_SURFACE.map(asset => (
              <tr key={asset.id} className="uas-row">
                <td style={{ fontWeight: 600 }}>{asset.asset}</td>
                <td style={{ color: '#94a3b8' }}>{asset.type}</td>
                <td style={{ color: asset.vulnerabilities > 0 ? '#ef4444' : '#10b981' }}>{asset.vulnerabilities}</td>
                <td style={{ color: asset.misconfigurations > 0 ? '#f59e0b' : '#10b981' }}>{asset.misconfigurations}</td>
                <td>
                  <span className={`uas-status uas-${asset.risk.toLowerCase()}`}>
                    {asset.risk}
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

const UAS_STYLES = `
.uas-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.uas-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.uas-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.uas-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.uas-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.uas-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.uas-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.uas-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.uas-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.uas-row td { padding: 12px; }
.uas-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.uas-critical { background: rgba(239,68,68,0.2); color: #fca5a5; }
.uas-high { background: rgba(249,115,22,0.2); color: #fdba74; }
.uas-medium { background: rgba(234,179,8,0.2); color: #fde047; }
`;
