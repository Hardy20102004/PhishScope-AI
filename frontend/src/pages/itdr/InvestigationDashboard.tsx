import React from 'react';
import { Link } from 'react-router-dom';
import { Search, ShieldAlert, Crosshair, UserCheck, UserX } from 'lucide-react';

const INVESTIGATIONS = [
  { id: 'INV-101', title: 'Suspicious impossible travel for alice.security', identity: 'alice.security', status: 'IN_PROGRESS', created: '2026-07-30 08:00', assignee: 'SOC Analyst 1' },
  { id: 'INV-102', title: 'MFA Fatigue on Service Account', identity: 'svc-backup', status: 'NEW', created: '2026-07-30 10:15', assignee: 'Unassigned' },
  { id: 'INV-099', title: 'Password Spray from Tor Exit Nodes', identity: 'Multiple', status: 'MITIGATED', created: '2026-07-29 22:00', assignee: 'SOC Lead' }
];

export default function InvestigationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{INV_STYLES}</style>
      <div className="inv-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="inv-header-icon"><Search size={24} /></div>
          <div>
            <h1 className="inv-title">Identity Investigations</h1>
            <p className="inv-subtitle">Workspace for triaging and resolving identity threats</p>
          </div>
        </div>
        <Link to="/itdr" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ITDR</Link>
      </div>

      <div className="inv-card">
        <h3 className="inv-card-title"><ShieldAlert size={16} /> Open Identity Investigations</h3>
        <table className="inv-table">
          <thead>
            <tr><th>Case ID</th><th>Title</th><th>Target Identity</th><th>Status</th><th>Assignee</th><th>Created</th><th>Action</th></tr>
          </thead>
          <tbody>
            {INVESTIGATIONS.map(inv => (
              <tr key={inv.id} className="inv-row">
                <td style={{ fontWeight: 600, color: '#8b5cf6' }}>{inv.id}</td>
                <td style={{ fontWeight: 500 }}>{inv.title}</td>
                <td style={{ color: '#94a3b8' }}>{inv.identity}</td>
                <td><span className={`inv-status inv-${inv.status.toLowerCase()}`}>{inv.status.replace('_', ' ')}</span></td>
                <td style={{ color: '#cbd5e1' }}>{inv.assignee}</td>
                <td style={{ color: '#64748b', fontSize: '0.8rem' }}>{inv.created}</td>
                <td>
                  <button className="inv-btn-view">View Case</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const INV_STYLES = `
.inv-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.inv-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.inv-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.inv-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.inv-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.inv-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.inv-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.inv-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.inv-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.inv-row td { padding: 12px; }
.inv-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.inv-new { background: rgba(59,130,246,0.15); color: #60a5fa; }
.inv-in_progress { background: rgba(245,158,11,0.15); color: #fbbf24; }
.inv-mitigated { background: rgba(16,185,129,0.15); color: #34d399; }
.inv-btn-view { padding: 6px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #e2e8f0; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.inv-btn-view:hover { background: rgba(255,255,255,0.1); }
`;
