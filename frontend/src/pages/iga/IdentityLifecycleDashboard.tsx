import React from 'react';
import { Link } from 'react-router-dom';
import { Users, UserPlus, UserMinus, ArrowRightLeft } from 'lucide-react';

const EVENTS = [
  { id: '1', type: 'JOINER', identity: 'eve.davis', source: 'Workday HR', date: '2026-08-01', status: 'PROCESSING', meta: 'Dept: Engineering' },
  { id: '2', type: 'MOVER', identity: 'alice.smith', source: 'Workday HR', date: '2026-07-29', status: 'COMPLETED', meta: 'New Dept: Security' },
  { id: '3', type: 'LEAVER', identity: 'contractor_45', source: 'SAP Fieldglass', date: '2026-07-30', status: 'PENDING', meta: 'Contract Expired' }
];

export default function IdentityLifecycleDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{JML_STYLES}</style>
      <div className="jml-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="jml-header-icon"><Users size={24} /></div>
          <div>
            <h1 className="jml-title">Joiner, Mover, Leaver (JML)</h1>
            <p className="jml-subtitle">Monitor identity lifecycle events across HR and directory systems</p>
          </div>
        </div>
        <Link to="/iga" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← IGA</Link>
      </div>

      <div className="jml-card">
        <h3 className="jml-card-title">Recent Lifecycle Events</h3>
        <table className="jml-table">
          <thead>
            <tr><th>Event Type</th><th>Target Identity</th><th>Source System</th><th>Effective Date</th><th>Metadata</th><th>Status</th></tr>
          </thead>
          <tbody>
            {EVENTS.map(ev => (
              <tr key={ev.id} className="jml-row">
                <td>
                  <span className={`jml-type-badge jml-type-${ev.type.toLowerCase()}`}>
                    {ev.type === 'JOINER' && <UserPlus size={12} />}
                    {ev.type === 'MOVER' && <ArrowRightLeft size={12} />}
                    {ev.type === 'LEAVER' && <UserMinus size={12} />}
                    {ev.type}
                  </span>
                </td>
                <td style={{ fontWeight: 600 }}>{ev.identity}</td>
                <td style={{ color: '#94a3b8' }}>{ev.source}</td>
                <td style={{ color: '#cbd5e1' }}>{ev.date}</td>
                <td style={{ color: '#94a3b8', fontSize: '0.8rem' }}>{ev.meta}</td>
                <td><span className={`jml-status jml-${ev.status.toLowerCase()}`}>{ev.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const JML_STYLES = `
.jml-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.jml-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.jml-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.jml-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.jml-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.jml-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.jml-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.jml-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.jml-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.jml-row td { padding: 12px; }
.jml-type-badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.jml-type-joiner { background: rgba(16,185,129,0.15); color: #34d399; }
.jml-type-mover { background: rgba(59,130,246,0.15); color: #60a5fa; }
.jml-type-leaver { background: rgba(239,68,68,0.15); color: #f87171; }
.jml-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.jml-pending { background: rgba(245,158,11,0.15); color: #fbbf24; }
.jml-processing { background: rgba(59,130,246,0.15); color: #60a5fa; }
.jml-completed { background: rgba(16,185,129,0.15); color: #34d399; }
`;
