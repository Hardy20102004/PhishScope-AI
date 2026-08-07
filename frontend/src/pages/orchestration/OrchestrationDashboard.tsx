import React from 'react';
import { Link } from 'react-router-dom';
import { GitBranch, Activity, CheckSquare, Sparkles, PlayCircle, ShieldCheck } from 'lucide-react';

const ORCH_METRICS = {
  active_workflows: 34,
  pending_approvals: 12,
  automated_tasks: 1245,
  playbooks_active: 8,
  ai_decisions_made: 420
};

export default function OrchestrationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{ORCH_STYLES}</style>
      
      {/* Header */}
      <div className="orch-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="orch-header-icon"><GitBranch size={24} /></div>
          <div>
            <h1 className="orch-title">AI Security Orchestration & SOAR</h1>
            <p className="orch-subtitle">Human-governed workflow automation and decision intelligence.</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/orchestration/assistant" className="orch-btn orch-btn-ai"><Sparkles size={14} /> AI Orchestrator</Link>
          <Link to="/orchestration/playbooks" className="orch-btn"><PlayCircle size={14} /> Playbooks</Link>
        </div>
      </div>

      {/* Primary KPI Row */}
      <div className="orch-grid-5">
        {[
          { label: 'Active Workflows', value: ORCH_METRICS.active_workflows, color: '#3b82f6' },
          { label: 'Pending Approvals', value: ORCH_METRICS.pending_approvals, color: '#f59e0b' },
          { label: 'Tasks Automated (24h)', value: ORCH_METRICS.automated_tasks, color: '#10b981' },
          { label: 'Active Playbooks', value: ORCH_METRICS.playbooks_active, color: '#8b5cf6' },
          { label: 'AI Decisions (24h)', value: ORCH_METRICS.ai_decisions_made, color: '#ec4899' }
        ].map(k => (
          <div key={k.label} className="orch-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.6rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="orch-main-layout">
        <div className="orch-modules-grid">
          <ModuleCard title="Workflow Engine" icon={<Activity />} link="/orchestration/workflows" desc="End-to-end incident and governance workflows." color="#3b82f6" />
          <ModuleCard title="Playbook Management" icon={<PlayCircle />} link="/orchestration/playbooks" desc="Standard operating procedures & automation." color="#8b5cf6" />
          <ModuleCard title="Task Coordination" icon={<CheckSquare />} link="/orchestration/tasks" desc="Analyst assignments and AI agent tasks." color="#10b981" />
          <ModuleCard title="Decision Intelligence" icon={<ShieldCheck />} link="/orchestration/decisions" desc="Explainable AI recommendations & human approvals." color="#f59e0b" />
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ title, icon, link, desc, color }: any) {
  return (
    <Link to={link} className="orch-mod-card" style={{ '--mod-color': color } as React.CSSProperties}>
      <div className="orch-mod-icon" style={{ color }}>{icon}</div>
      <div className="orch-mod-content">
        <h3 className="orch-mod-title">{title}</h3>
        <p className="orch-mod-desc">{desc}</p>
      </div>
    </Link>
  );
}

const ORCH_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.orch-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.orch-header-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #4f46e5, #3730a3); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.orch-title { font-size: 1.45rem; font-weight: 800; margin: 0 0 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.orch-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.orch-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.orch-btn:hover { background: rgba(255,255,255,0.1); }
.orch-btn-ai { background: rgba(236,72,153,0.15); border-color: rgba(236,72,153,0.3); color: #f472b6; }
.orch-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 24px; }
.orch-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.orch-modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.orch-mod-card { display: flex; align-items: flex-start; gap: 16px; padding: 20px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; text-decoration: none; transition: all 0.2s; }
.orch-mod-card:hover { background: rgba(255,255,255,0.04); border-color: var(--mod-color); transform: translateY(-2px); }
.orch-mod-icon { padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; }
.orch-mod-content { flex: 1; }
.orch-mod-title { margin: 0 0 4px; font-size: 0.95rem; font-weight: 700; color: #f8fafc; }
.orch-mod-desc { margin: 0; font-size: 0.75rem; color: #94a3b8; line-height: 1.4; }
`;
