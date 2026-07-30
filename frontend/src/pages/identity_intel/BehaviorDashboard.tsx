import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, MapPin, Monitor, Clock } from 'lucide-react';

const BEHAVIORS = [
  { id: '1', user: 'david.smith (Admin)', deviation: 'ANOMALOUS', reason: 'Unusual time + unusual location (AWS Prod)', updated: '2 mins ago' },
  { id: '2', user: 'sarah.connor', deviation: 'SLIGHT_DEVIATION', reason: 'New mobile device enrolled', updated: '1 hr ago' },
  { id: '3', user: 'service.build', deviation: 'NORMAL', reason: 'Matches expected automated pipeline schedule', updated: '4 hrs ago' }
];

export default function BehaviorDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{BEH_STYLES}</style>
      <div className="beh-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="beh-header-icon"><Activity size={24} /></div>
          <div>
            <h1 className="beh-title">Behavior Analytics</h1>
            <p className="beh-subtitle">Monitor user behavior baselines and track deviations</p>
          </div>
        </div>
        <Link to="/identity-intel" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Intelligence Dashboard</Link>
      </div>

      <div className="beh-card">
        <h3 className="beh-card-title">Behavioral Profiles & Baselines</h3>
        <table className="beh-table">
          <thead>
            <tr><th>Identity</th><th>Current Deviation State</th><th>Reason / Context</th><th>Last Correlated</th></tr>
          </thead>
          <tbody>
            {BEHAVIORS.map(beh => (
              <tr key={beh.id} className="beh-row">
                <td style={{ fontWeight: 600 }}>{beh.user}</td>
                <td>
                  <span className={`beh-status beh-${beh.deviation.toLowerCase()}`}>
                    {beh.deviation.replace('_', ' ')}
                  </span>
                </td>
                <td style={{ color: '#cbd5e1' }}>{beh.reason}</td>
                <td style={{ color: '#94a3b8' }}>{beh.updated}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const BEH_STYLES = `
.beh-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.beh-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.beh-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.beh-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.beh-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.beh-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.beh-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.beh-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.beh-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.beh-row td { padding: 12px; }
.beh-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.beh-normal { background: rgba(16,185,129,0.15); color: #34d399; }
.beh-slight_deviation { background: rgba(245,158,11,0.15); color: #fbbf24; }
.beh-anomalous { background: rgba(239,68,68,0.2); color: #fca5a5; }
`;
