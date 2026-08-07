import React from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Users, CheckCircle, Shield, AlertTriangle, Key, ArrowRight } from 'lucide-react';

const IGA_DATA = {
  pending_access_requests: 142,
  active_campaigns: 2,
  sod_violations: 4,
  recent_onboards: 18,
  recent_offboards: 5,
  recent_requests: [
    { id: 'REQ-889', requester: 'alice.smith', role: 'AWS Prod DB Admin', status: 'PENDING_APPROVAL', time: '10 mins ago' },
    { id: 'REQ-888', requester: 'bob.jones', role: 'GitHub Admin', status: 'APPROVED', time: '1 hour ago' },
    { id: 'REQ-887', requester: 'charlie.brown', role: 'Financial Reports', status: 'PROVISIONED', time: '3 hours ago' }
  ]
};

export default function IGADashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{IGA_STYLES}</style>
      
      {/* Header */}
      <div className="iga-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="iga-header-icon"><BookOpen size={24} /></div>
          <div>
            <h1 className="iga-title">Identity Governance & Administration (IGA)</h1>
            <p className="iga-subtitle">Lifecycle Management · Access Certification · SoD Governance</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/iga/requests" className="iga-btn"><CheckCircle size={14} /> View Approvals</Link>
          <Link to="/iga/assistant" className="iga-btn iga-btn-ai">Ask IGA AI</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="iga-grid-5">
        {[
          { label: 'Pending Access Requests', value: IGA_DATA.pending_access_requests, color: '#3b82f6' },
          { label: 'Active Cert Campaigns', value: IGA_DATA.active_campaigns, color: '#8b5cf6' },
          { label: 'Active SoD Violations', value: IGA_DATA.sod_violations, color: '#ef4444' },
          { label: 'Recent Onboards (7d)', value: IGA_DATA.recent_onboards, color: '#10b981' },
          { label: 'Recent Offboards (7d)', value: IGA_DATA.recent_offboards, color: '#f59e0b' }
        ].map(k => (
          <div key={k.label} className="iga-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="iga-main-layout">
        <div className="iga-left-col">
          {/* Recent Access Requests */}
          <div className="iga-card">
            <h3 className="iga-card-title"><Key size={16} /> Recent Access Requests</h3>
            <div className="iga-list">
              {IGA_DATA.recent_requests.map((req) => (
                <div key={req.id} className="iga-list-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{req.role}</strong>
                    <span className={`iga-badge iga-badge-${req.status.toLowerCase()}`}>{req.status.replace('_', ' ')}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Requested by: {req.requester}</p>
                    <span style={{ fontSize: '0.7rem', color: '#64748b' }}>{req.time}</span>
                  </div>
                </div>
              ))}
            </div>
            <Link to="/iga/requests" style={{ display: 'block', textAlign: 'center', marginTop: 12, color: '#3b82f6', fontSize: '0.8rem', textDecoration: 'none' }}>View All Requests →</Link>
          </div>
        </div>
        
        <div className="iga-right-col">
          {/* Quick Actions / Navigation */}
          <div className="iga-card">
            <h3 className="iga-card-title">IGA Modules</h3>
            <div className="iga-module-links">
              <Link to="/iga/lifecycle" className="iga-mod-link"><Users size={16} /> JML Lifecycle</Link>
              <Link to="/iga/requests" className="iga-mod-link"><Key size={16} /> Access Requests</Link>
              <Link to="/iga/certifications" className="iga-mod-link"><CheckCircle size={16} /> Access Certifications</Link>
              <Link to="/iga/entitlements" className="iga-mod-link"><Shield size={16} /> Entitlement Inventory</Link>
              <Link to="/iga/sod" className="iga-mod-link"><AlertTriangle size={16} /> Segregation of Duties</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const IGA_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.iga-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.iga-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #14b8a6, #0d9488); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.iga-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.iga-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.iga-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.iga-btn:hover { background: rgba(255,255,255,0.1); }
.iga-btn-ai { background: rgba(20,184,166,0.15); border-color: rgba(20,184,166,0.3); color: #5eead4; }
.iga-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 16px; }
.iga-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.iga-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .iga-main-layout { grid-template-columns: 1fr; } }
.iga-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.iga-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.iga-list { display: flex; flex-direction: column; gap: 10px; }
.iga-list-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; transition: all 0.2s; }
.iga-list-item:hover { background: rgba(255,255,255,0.04); }
.iga-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.iga-badge-pending_approval { color: #fdba74; background: rgba(249,115,22,0.2); }
.iga-badge-approved { color: #60a5fa; background: rgba(59,130,246,0.2); }
.iga-badge-provisioned { color: #34d399; background: rgba(16,185,129,0.2); }
.iga-module-links { display: flex; flex-direction: column; gap: 8px; }
.iga-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.iga-mod-link:hover { background: rgba(20,184,166,0.1); border-color: rgba(20,184,166,0.3); color: #fff; }
`;
