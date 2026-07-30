import React from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle, Clock, Shield } from 'lucide-react';

const CAMPAIGNS = [
  { id: 'CMP-2026-Q3', name: 'Q3 2026 Engineering Access Review', status: 'ACTIVE', start: '2026-07-01', due: '2026-07-31', progress: 85, total: 1250, completed: 1062 },
  { id: 'CMP-2026-PRIV', name: 'Annual Privileged Access Certification', status: 'DRAFT', start: '-', due: '2026-08-15', progress: 0, total: 45, completed: 0 }
];

export default function CertificationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CERT_STYLES}</style>
      <div className="cert-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="cert-header-icon"><CheckCircle size={24} /></div>
          <div>
            <h1 className="cert-title">Access Certifications (UAR)</h1>
            <p className="cert-subtitle">Manage User Access Review campaigns and compliance tracking</p>
          </div>
        </div>
        <Link to="/iga" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← IGA</Link>
      </div>

      <div className="cert-card">
        <h3 className="cert-card-title">Active & Upcoming Campaigns</h3>
        <table className="cert-table">
          <thead>
            <tr><th>Campaign Name</th><th>Status</th><th>Start Date</th><th>Due Date</th><th>Progress</th><th>Action</th></tr>
          </thead>
          <tbody>
            {CAMPAIGNS.map(cmp => (
              <tr key={cmp.id} className="cert-row">
                <td style={{ fontWeight: 600 }}>{cmp.name}</td>
                <td><span className={`cert-status cert-${cmp.status.toLowerCase()}`}>{cmp.status}</span></td>
                <td style={{ color: '#94a3b8' }}>{cmp.start}</td>
                <td style={{ color: '#cbd5e1' }}>{cmp.due}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div style={{ width: 100, height: 6, background: 'rgba(255,255,255,0.1)', borderRadius: 3 }}>
                      <div style={{ width: `${cmp.progress}%`, height: '100%', background: '#8b5cf6', borderRadius: 3 }} />
                    </div>
                    <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{cmp.completed} / {cmp.total}</span>
                  </div>
                </td>
                <td>
                  <button className="cert-btn-view">Manage Campaign</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const CERT_STYLES = `
.cert-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.cert-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.cert-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.cert-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.cert-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.cert-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.cert-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.cert-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.cert-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.cert-row td { padding: 12px; }
.cert-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.cert-active { background: rgba(139,92,246,0.15); color: #a78bfa; }
.cert-draft { background: rgba(255,255,255,0.05); color: #94a3b8; }
.cert-btn-view { padding: 6px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #e2e8f0; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: background 0.2s; }
.cert-btn-view:hover { background: rgba(255,255,255,0.1); }
`;
