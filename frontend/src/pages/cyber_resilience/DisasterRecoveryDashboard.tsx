import React from 'react';
import { Link } from 'react-router-dom';
import { Server, CheckCircle, XCircle } from 'lucide-react';

const DR_TESTS = [
  { id: '1', scope: 'AWS Prod DB Failover', date: '2026-06-15', rto_target: '30m', actual_rto: '22m', outcome: 'SUCCESS' },
  { id: '2', scope: 'Identity Provider Restoration', date: '2026-05-10', rto_target: '15m', actual_rto: '28m', outcome: 'PARTIAL_SUCCESS' }
];

export default function DisasterRecoveryDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{DR_STYLES}</style>
      <div className="dr-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="dr-header-icon"><Server size={24} /></div>
          <div>
            <h1 className="dr-title">Disaster Recovery Readiness</h1>
            <p className="dr-subtitle">Infrastructure backup, failover testing, and RTO validation</p>
          </div>
        </div>
        <Link to="/cyber-resilience" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Resilience Home</Link>
      </div>

      <div className="dr-card">
        <h3 className="dr-card-title"><Server size={16} color="#8b5cf6" /> Historical DR Test Results</h3>
        <table className="dr-table">
          <thead>
            <tr><th>Test Scope</th><th>Test Date</th><th>Target RTO</th><th>Actual RTO</th><th>Outcome</th></tr>
          </thead>
          <tbody>
            {DR_TESTS.map(t => (
              <tr key={t.id} className="dr-row">
                <td style={{ fontWeight: 600 }}>{t.scope}</td>
                <td style={{ color: '#94a3b8' }}>{t.date}</td>
                <td><span className="dr-mono">{t.rto_target}</span></td>
                <td><span className={`dr-mono ${t.outcome === 'SUCCESS' ? 'dr-good' : 'dr-warn'}`}>{t.actual_rto}</span></td>
                <td>
                  <span className={`dr-badge dr-${t.outcome.toLowerCase()}`}>
                    {t.outcome === 'SUCCESS' ? <CheckCircle size={12} style={{marginRight: 4}}/> : null}
                    {t.outcome.replace('_', ' ')}
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

const DR_STYLES = `
.dr-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.dr-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #6d28d9); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.dr-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.dr-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.dr-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.dr-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.dr-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.dr-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.dr-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.dr-row td { padding: 12px; }
.dr-mono { font-family: monospace; font-size: 0.95rem; color: #e2e8f0; }
.dr-good { color: #34d399; }
.dr-warn { color: #fbbf24; }
.dr-badge { display: inline-flex; align-items: center; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.dr-success { background: rgba(16,185,129,0.15); color: #34d399; }
.dr-partial_success { background: rgba(245,158,11,0.15); color: #fbbf24; }
`;
