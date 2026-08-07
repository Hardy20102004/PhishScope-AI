import React from 'react';
import { Link } from 'react-router-dom';
import { CheckSquare, User, Cpu } from 'lucide-react';

const TASKS = [
  { id: '1', title: 'Review AWS Network Isolation', assigned: 'Analyst (Sarah J.)', is_ai: false, status: 'IN_PROGRESS' },
  { id: '2', title: 'Correlate Okta Logs with CloudTrail', assigned: 'AI Agent (Brain)', is_ai: true, status: 'COMPLETED' },
  { id: '3', title: 'Approve JIT Privilege Escalation', assigned: 'SOC Manager', is_ai: false, status: 'OPEN' }
];

export default function TaskDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{TSK_STYLES}</style>
      <div className="tsk-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="tsk-header-icon"><CheckSquare size={24} /></div>
          <div>
            <h1 className="tsk-title">Task Coordination</h1>
            <p className="tsk-subtitle">Unified assignment tracking for human analysts and AI agents</p>
          </div>
        </div>
        <Link to="/orchestration" style={{ color: '#60a5fa', textDecoration: 'none', fontSize: '0.85rem' }}>← Orchestration Hub</Link>
      </div>

      <div className="tsk-card">
        <h3 className="tsk-card-title">Active Assignments</h3>
        <table className="tsk-table">
          <thead>
            <tr><th>Task Description</th><th>Assignee</th><th>Status</th></tr>
          </thead>
          <tbody>
            {TASKS.map(task => (
              <tr key={task.id} className="tsk-row">
                <td style={{ fontWeight: 600 }}>{task.title}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: task.is_ai ? '#a855f7' : '#94a3b8' }}>
                    {task.is_ai ? <Cpu size={14} /> : <User size={14} />}
                    {task.assigned}
                  </div>
                </td>
                <td>
                  <span className={`tsk-status tsk-${task.status.toLowerCase()}`}>
                    {task.status}
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

const TSK_STYLES = `
.tsk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.tsk-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.tsk-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.tsk-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.tsk-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.tsk-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.tsk-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.tsk-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.tsk-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.tsk-row td { padding: 12px; }
.tsk-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.tsk-open { background: rgba(59,130,246,0.15); color: #60a5fa; }
.tsk-in_progress { background: rgba(245,158,11,0.15); color: #fbbf24; }
.tsk-completed { background: rgba(16,185,129,0.15); color: #34d399; }
`;
