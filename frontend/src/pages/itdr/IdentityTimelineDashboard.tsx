import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Clock, LogIn, Lock, MapPin, Database, ChevronDown } from 'lucide-react';

const EVENTS = [
  { id: '1', type: 'LOGIN_SUCCESS', time: '10:45:12 AM', ip: '192.168.1.5', location: 'Seattle, WA', device: 'MacBook Pro', details: 'Interactive login via Entra ID', icon: <LogIn size={14} color="#10b981" /> },
  { id: '2', type: 'MFA_CHALLENGE', time: '10:45:15 AM', ip: '192.168.1.5', location: 'Seattle, WA', device: 'MacBook Pro', details: 'FIDO2 WebAuthn Verification', icon: <Lock size={14} color="#3b82f6" /> },
  { id: '3', type: 'APP_ACCESS', time: '10:46:00 AM', ip: '192.168.1.5', location: 'Seattle, WA', device: 'MacBook Pro', details: 'Accessed Salesforce CRM', icon: <Database size={14} color="#6366f1" /> },
  { id: '4', type: 'LOGIN_FAILED', time: '11:15:22 AM', ip: '104.12.5.99', location: 'Moscow, RU', device: 'Unknown Browser', details: 'Invalid Password', icon: <Lock size={14} color="#ef4444" />, anomalous: true },
];

export default function IdentityTimelineDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{TL_STYLES}</style>
      <div className="tl-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="tl-header-icon"><Clock size={24} /></div>
          <div>
            <h1 className="tl-title">Identity Timeline</h1>
            <p className="tl-subtitle">Chronological sequence of authentication and authorization events</p>
          </div>
        </div>
        <Link to="/itdr" style={{ color: '#818cf8', textDecoration: 'none', fontSize: '0.85rem' }}>← ITDR</Link>
      </div>

      <div className="tl-search-bar">
        <div style={{ display: 'flex', gap: 12 }}>
          <input type="text" placeholder="Search identity (e.g. alice.security@corp.com)" className="tl-input" />
          <button className="tl-btn-primary">Load Timeline</button>
        </div>
      </div>

      <div className="tl-card">
        <h3 className="tl-card-title"><Activity size={16} /> Event Stream: <span style={{ color: '#fff' }}>alice.security</span></h3>
        
        <div className="tl-container">
          {EVENTS.map((ev, index) => (
            <div key={ev.id} className={`tl-event ${ev.anomalous ? 'tl-anomalous' : ''}`}>
              <div className="tl-connector" />
              <div className="tl-time">{ev.time}</div>
              <div className="tl-icon-wrapper">{ev.icon}</div>
              <div className="tl-content">
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                  <strong style={{ fontSize: '0.85rem', color: ev.anomalous ? '#fca5a5' : '#e2e8f0' }}>{ev.type.replace('_', ' ')}</strong>
                  {ev.anomalous && <span className="tl-badge-risk">ANOMALY</span>}
                </div>
                <p style={{ margin: '0 0 8px', fontSize: '0.8rem', color: '#94a3b8' }}>{ev.details}</p>
                <div style={{ display: 'flex', gap: 12, fontSize: '0.75rem', color: '#64748b' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><MapPin size={12} /> {ev.location} ({ev.ip})</span>
                  <span>Device: {ev.device}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div style={{ textAlign: 'center', marginTop: 16 }}>
          <button style={{ background: 'transparent', border: 'none', color: '#64748b', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 4, fontSize: '0.8rem' }}>
            Load More <ChevronDown size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}

const TL_STYLES = `
.tl-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.tl-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.tl-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.tl-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.tl-search-bar { background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 24px; }
.tl-input { flex: 1; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); padding: 8px 12px; border-radius: 8px; color: white; font-size: 0.85rem; outline: none; }
.tl-btn-primary { background: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.tl-btn-primary:hover { background: #2563eb; }
.tl-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.tl-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 24px; color: #94a3b8; }
.tl-container { position: relative; display: flex; flex-direction: column; gap: 16px; }
.tl-event { display: flex; gap: 16px; position: relative; }
.tl-connector { position: absolute; left: 104px; top: 24px; bottom: -16px; width: 2px; background: rgba(255,255,255,0.05); }
.tl-event:last-child .tl-connector { display: none; }
.tl-time { width: 80px; font-size: 0.75rem; color: #64748b; padding-top: 6px; text-align: right; }
.tl-icon-wrapper { width: 28px; height: 28px; border-radius: 50%; background: rgba(255,255,255,0.05); border: 2px solid #0a0a12; display: flex; align-items: center; justify-content: center; z-index: 2; margin-top: 2px; }
.tl-content { flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px 16px; border-radius: 8px; }
.tl-anomalous .tl-icon-wrapper { background: rgba(239,68,68,0.2); border-color: rgba(239,68,68,0.5); }
.tl-anomalous .tl-content { border-color: rgba(239,68,68,0.3); background: rgba(239,68,68,0.05); }
.tl-badge-risk { padding: 2px 6px; background: #ef4444; color: white; border-radius: 4px; font-size: 0.65rem; font-weight: 800; }
`;
