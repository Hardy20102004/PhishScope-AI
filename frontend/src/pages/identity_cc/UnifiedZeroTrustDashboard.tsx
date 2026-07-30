import React from 'react';
import { Link } from 'react-router-dom';
import { Lock, ShieldCheck, Activity } from 'lucide-react';

const ZT_METRICS = [
  { module: 'Authentication', metric: 'Continuous Validation', status: 'Healthy', score: 95 },
  { module: 'Privileged Access', metric: 'JIT Provisioning', status: 'Warning', score: 72 },
  { module: 'Workload Identity', metric: 'mTLS Enforcement', status: 'Healthy', score: 100 }
];

export default function UnifiedZeroTrustDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{UZT_STYLES}</style>
      <div className="uzt-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="uzt-header-icon"><Lock size={24} /></div>
          <div>
            <h1 className="uzt-title">Unified Zero Trust Operations</h1>
            <p className="uzt-subtitle">Enterprise-wide continuous verification metrics</p>
          </div>
        </div>
        <Link to="/identity-cc" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Command Center</Link>
      </div>

      <div className="uzt-card">
        <h3 className="uzt-card-title"><ShieldCheck size={16} /> Zero Trust Posture Alignment</h3>
        <table className="uzt-table">
          <thead>
            <tr><th>Security Domain</th><th>Core ZT Metric</th><th>Alignment Score</th><th>Status</th></tr>
          </thead>
          <tbody>
            {ZT_METRICS.map((zt, i) => (
              <tr key={i} className="uzt-row">
                <td style={{ fontWeight: 600 }}>{zt.module}</td>
                <td style={{ color: '#94a3b8' }}>{zt.metric}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div className="uzt-bar-bg">
                      <div className="uzt-bar-fill" style={{ width: \`\${zt.score}%\`, background: zt.score < 80 ? '#f59e0b' : '#10b981' }}></div>
                    </div>
                    <span style={{ fontWeight: 700 }}>{zt.score}</span>
                  </div>
                </td>
                <td>
                  <span className={\`uzt-status uzt-\${zt.status.toLowerCase()}\`}>
                    {zt.status}
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

const UZT_STYLES = \`
.uzt-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.uzt-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.uzt-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.uzt-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.uzt-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.uzt-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.uzt-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.uzt-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.uzt-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.uzt-row td { padding: 12px; }
.uzt-bar-bg { flex: 1; max-width: 120px; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; }
.uzt-bar-fill { height: 100%; border-radius: 3px; }
.uzt-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.uzt-healthy { background: rgba(16,185,129,0.15); color: #34d399; }
.uzt-warning { background: rgba(245,158,11,0.15); color: #fbbf24; }
\`;
