import React from 'react';
import { Link } from 'react-router-dom';
import { Users, AlertTriangle } from 'lucide-react';

const EXERCISES = [
  { id: '1', title: 'Operation Midnight Strike', scenario: 'Ransomware outbreak hitting core AD and spreading to backups.', status: 'COMPLETED', date: '2026-04-12' },
  { id: '2', title: 'Cloud Data Extortion', scenario: 'Compromised developer credentials leading to AWS S3 bucket exfiltration.', status: 'PLANNED', date: '2026-08-20' }
];

export default function TabletopExerciseDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{TT_STYLES}</style>
      <div className="tt-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="tt-header-icon"><Users size={24} /></div>
          <div>
            <h1 className="tt-title">Tabletop Exercises</h1>
            <p className="tt-subtitle">Crisis simulation scenarios and readiness validation</p>
          </div>
        </div>
        <Link to="/cyber-resilience" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Resilience Home</Link>
      </div>

      <div className="tt-card">
        <h3 className="tt-card-title"><AlertTriangle size={16} color="#f59e0b" /> Active & Planned Exercises</h3>
        <table className="tt-table">
          <thead>
            <tr><th>Exercise Title</th><th>Scenario Description</th><th>Status</th><th>Scheduled Date</th></tr>
          </thead>
          <tbody>
            {EXERCISES.map(e => (
              <tr key={e.id} className="tt-row">
                <td style={{ fontWeight: 600 }}>{e.title}</td>
                <td style={{ color: '#cbd5e1', maxWidth: 300, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{e.scenario}</td>
                <td>
                  <span className={`tt-status tt-${e.status.toLowerCase()}`}>
                    {e.status}
                  </span>
                </td>
                <td style={{ color: '#94a3b8' }}>{e.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const TT_STYLES = `
.tt-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.tt-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.tt-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.tt-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.tt-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.tt-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.tt-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.tt-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.tt-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.tt-row td { padding: 12px; }
.tt-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.tt-completed { background: rgba(16,185,129,0.15); color: #34d399; }
.tt-planned { background: rgba(59,130,246,0.15); color: #60a5fa; }
`;
