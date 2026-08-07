import React from 'react';
import { Link } from 'react-router-dom';
import { Play, ShieldAlert, Cpu } from 'lucide-react';

const SIMULATIONS = [
  { id: '1', scenario: 'Revoke AWS IAM over-permissioned roles', status: 'COMPLETED', impact: 'Risk reduced by 42%', risk: 'LOW' },
  { id: '2', scenario: 'Simulate Zero-Day exploit on edge VPN', status: 'RUNNING', impact: 'Calculating...', risk: 'HIGH' }
];

export default function ScenarioSimulationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{SIM_STYLES}</style>
      <div className="sim-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="sim-header-icon"><Play size={24} /></div>
          <div>
            <h1 className="sim-title">Scenario Simulation</h1>
            <p className="sim-subtitle">Predictive 'what-if' modeling of defensive configurations</p>
          </div>
        </div>
        <Link to="/digital-twin" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Digital Twin Home</Link>
      </div>

      <div className="sim-card">
        <h3 className="sim-card-title"><Cpu size={16} color="#f59e0b" /> Active & Recent Simulations</h3>
        <table className="sim-table">
          <thead>
            <tr><th>Hypothesis / Scenario</th><th>Simulation Status</th><th>Predicted Impact</th></tr>
          </thead>
          <tbody>
            {SIMULATIONS.map(sim => (
              <tr key={sim.id} className="sim-row">
                <td style={{ fontWeight: 600 }}>{sim.scenario}</td>
                <td>
                  <span className={`sim-status sim-${sim.status.toLowerCase()}`}>
                    {sim.status}
                  </span>
                </td>
                <td style={{ color: '#94a3b8' }}>{sim.impact}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const SIM_STYLES = `
.sim-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.sim-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.sim-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.sim-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.sim-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.sim-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.sim-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.sim-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.sim-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.sim-row td { padding: 12px; }
.sim-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.sim-completed { background: rgba(16,185,129,0.15); color: #34d399; }
.sim-running { background: rgba(59,130,246,0.15); color: #60a5fa; }
`;
