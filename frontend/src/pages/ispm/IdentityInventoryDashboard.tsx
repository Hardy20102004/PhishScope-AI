import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
  Users, Search, Filter, Shield, AlertTriangle, UserX, Server,
  Key, Activity, ChevronRight, Download, RefreshCw, Eye, Brain,
  CheckCircle, XCircle, Clock, Fingerprint, Cpu, Zap
} from 'lucide-react';

const IDENTITY_TYPES = ['ALL', 'HUMAN', 'SERVICE_ACCOUNT', 'MACHINE', 'PRIVILEGED', 'MANAGED_IDENTITY'];
const STATUS_TYPES = ['ALL', 'ACTIVE', 'DORMANT', 'DISABLED', 'ORPHANED'];
const RISK_LEVELS = ['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];

const MOCK_IDENTITIES = [
  { id: '1', display_name: 'John Smith', email: 'john.smith@corp.com', identity_type: 'HUMAN', source_provider: 'ENTRA_ID', status: 'ACTIVE', is_privileged: true, mfa_enabled: false, risk_level: 'CRITICAL', current_risk_score: 87.3, department: 'IT Security', job_title: 'Senior Admin', last_login_at: '2026-07-25', days_since_last_login: 5 },
  { id: '2', display_name: 'Maria Garcia', email: 'maria.garcia@corp.com', identity_type: 'HUMAN', source_provider: 'OKTA', status: 'ACTIVE', is_privileged: false, mfa_enabled: true, risk_level: 'LOW', current_risk_score: 18.2, department: 'Finance', job_title: 'CFO', last_login_at: '2026-07-30', days_since_last_login: 0 },
  { id: '3', display_name: 'svc-payroll-api', email: null, identity_type: 'SERVICE_ACCOUNT', source_provider: 'AWS_IAM', status: 'ACTIVE', is_privileged: true, mfa_enabled: false, risk_level: 'HIGH', current_risk_score: 72.1, department: 'IT', job_title: 'Service Account', last_login_at: '2026-07-28', days_since_last_login: 2 },
  { id: '4', display_name: 'David Chen', email: 'david.chen@corp.com', identity_type: 'HUMAN', source_provider: 'ACTIVE_DIRECTORY', status: 'DORMANT', is_privileged: true, mfa_enabled: true, risk_level: 'HIGH', current_risk_score: 65.8, department: 'Engineering', job_title: 'DevOps Lead', last_login_at: '2026-05-01', days_since_last_login: 90 },
  { id: '5', display_name: 'machine-k8s-node-01', email: null, identity_type: 'MACHINE', source_provider: 'KUBERNETES_RBAC', status: 'ACTIVE', is_privileged: false, mfa_enabled: false, risk_level: 'MEDIUM', current_risk_score: 42.5, department: 'Infrastructure', job_title: 'Workload Identity', last_login_at: '2026-07-30', days_since_last_login: 0 },
  { id: '6', display_name: 'Sarah Williams', email: 'sarah.williams@corp.com', identity_type: 'HUMAN', source_provider: 'ENTRA_ID', status: 'ACTIVE', is_privileged: false, mfa_enabled: true, risk_level: 'LOW', current_risk_score: 12.4, department: 'HR', job_title: 'HR Director', last_login_at: '2026-07-29', days_since_last_login: 1 },
  { id: '7', display_name: 'svc-monitoring-agent', email: null, identity_type: 'SERVICE_ACCOUNT', source_provider: 'GCP_IAM', status: 'ACTIVE', is_privileged: false, mfa_enabled: false, risk_level: 'MEDIUM', current_risk_score: 38.1, department: 'Operations', job_title: 'Service Account', last_login_at: '2026-07-30', days_since_last_login: 0 },
  { id: '8', display_name: 'Robert Johnson', email: 'robert.johnson@corp.com', identity_type: 'HUMAN', source_provider: 'OKTA', status: 'DISABLED', is_privileged: false, mfa_enabled: false, risk_level: 'LOW', current_risk_score: 5.0, department: 'Sales', job_title: 'Account Manager', last_login_at: '2026-01-15', days_since_last_login: 196 },
  { id: '9', display_name: 'app-oauth-github', email: null, identity_type: 'APPLICATION', source_provider: 'ENTRA_ID', status: 'ACTIVE', is_privileged: false, mfa_enabled: false, risk_level: 'MEDIUM', current_risk_score: 45.2, department: 'Engineering', job_title: 'App Identity', last_login_at: '2026-07-30', days_since_last_login: 0 },
  { id: '10', display_name: 'Zhang Wei', email: 'zhang.wei@corp.com', identity_type: 'HUMAN', source_provider: 'ACTIVE_DIRECTORY', status: 'ACTIVE', is_privileged: true, mfa_enabled: true, risk_level: 'MEDIUM', current_risk_score: 35.7, department: 'Security', job_title: 'Security Architect', last_login_at: '2026-07-30', days_since_last_login: 0 },
  { id: '11', display_name: 'orphaned-svc-legacy', email: null, identity_type: 'SERVICE_ACCOUNT', source_provider: 'ACTIVE_DIRECTORY', status: 'ORPHANED', is_privileged: true, mfa_enabled: false, risk_level: 'CRITICAL', current_risk_score: 94.1, department: 'Unknown', job_title: 'Service Account', last_login_at: '2025-12-01', days_since_last_login: 241 },
  { id: '12', display_name: 'Ana Rodriguez', email: 'ana.rodriguez@corp.com', identity_type: 'HUMAN', source_provider: 'OKTA', status: 'ACTIVE', is_privileged: false, mfa_enabled: true, risk_level: 'LOW', current_risk_score: 9.8, department: 'Legal', job_title: 'General Counsel', last_login_at: '2026-07-29', days_since_last_login: 1 },
];

const RISK_COLORS: Record<string, string> = {
  CRITICAL: '#ef4444', HIGH: '#f97316', MEDIUM: '#f59e0b', LOW: '#10b981'
};
const STATUS_COLORS: Record<string, string> = {
  ACTIVE: '#10b981', DORMANT: '#f97316', DISABLED: '#64748b', ORPHANED: '#ef4444', LOCKED: '#dc2626'
};
const TYPE_ICONS: Record<string, React.ReactNode> = {
  HUMAN: <Users size={14} />,
  SERVICE_ACCOUNT: <Server size={14} />,
  MACHINE: <Cpu size={14} />,
  APPLICATION: <Activity size={14} />,
  PRIVILEGED: <Key size={14} />,
  MANAGED_IDENTITY: <Fingerprint size={14} />,
};
const PROVIDER_LABELS: Record<string, string> = {
  ENTRA_ID: 'Entra ID', OKTA: 'Okta', ACTIVE_DIRECTORY: 'AD',
  AWS_IAM: 'AWS IAM', GCP_IAM: 'GCP IAM', KUBERNETES_RBAC: 'K8s RBAC'
};

export default function IdentityInventoryDashboard() {
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [selected, setSelected] = useState<string | null>(null);

  const filtered = useMemo(() => MOCK_IDENTITIES.filter(id => {
    const matchSearch = !search || id.display_name.toLowerCase().includes(search.toLowerCase()) ||
      (id.email && id.email.toLowerCase().includes(search.toLowerCase()));
    const matchType = typeFilter === 'ALL' || id.identity_type === typeFilter ||
      (typeFilter === 'PRIVILEGED' && id.is_privileged);
    const matchStatus = statusFilter === 'ALL' || id.status === statusFilter;
    const matchRisk = riskFilter === 'ALL' || id.risk_level === riskFilter;
    return matchSearch && matchType && matchStatus && matchRisk;
  }), [search, typeFilter, statusFilter, riskFilter]);

  const selectedIdentity = selected ? MOCK_IDENTITIES.find(i => i.id === selected) : null;

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{INV_STYLES}</style>

      {/* Header */}
      <div className="inv-header">
        <div className="inv-header-left">
          <div className="inv-header-icon"><Users size={24} /></div>
          <div>
            <h1 className="inv-title">Identity Inventory</h1>
            <p className="inv-subtitle">{MOCK_IDENTITIES.length} identities · Entra ID · Active Directory · Okta · AWS IAM · GCP IAM · Kubernetes</p>
          </div>
        </div>
        <div className="inv-header-actions">
          <button className="inv-btn-outline"><RefreshCw size={14} /> Sync</button>
          <button className="inv-btn-outline"><Download size={14} /> Export</button>
          <Link to="/ispm" className="inv-btn-back"><ChevronRight size={14} style={{ transform: 'rotate(180deg)' }} /> ISPM</Link>
        </div>
      </div>

      {/* Stats Row */}
      <div className="inv-stats-row">
        {[
          { label: 'Total', value: MOCK_IDENTITIES.length, color: '#6366f1' },
          { label: 'Human', value: MOCK_IDENTITIES.filter(i => i.identity_type === 'HUMAN').length, color: '#8b5cf6' },
          { label: 'Service', value: MOCK_IDENTITIES.filter(i => i.identity_type === 'SERVICE_ACCOUNT').length, color: '#06b6d4' },
          { label: 'Machine', value: MOCK_IDENTITIES.filter(i => i.identity_type === 'MACHINE').length, color: '#10b981' },
          { label: 'Privileged', value: MOCK_IDENTITIES.filter(i => i.is_privileged).length, color: '#f97316' },
          { label: 'Dormant', value: MOCK_IDENTITIES.filter(i => i.status === 'DORMANT').length, color: '#ef4444' },
          { label: 'Orphaned', value: MOCK_IDENTITIES.filter(i => i.status === 'ORPHANED').length, color: '#dc2626' },
          { label: 'No MFA', value: MOCK_IDENTITIES.filter(i => !i.mfa_enabled && i.status === 'ACTIVE').length, color: '#f59e0b' },
        ].map(({ label, value, color }) => (
          <div key={label} className="inv-stat-chip" style={{ borderColor: `${color}30` }}>
            <span style={{ color, fontSize: '1.4rem', fontWeight: 800 }}>{value}</span>
            <span style={{ fontSize: '0.72rem', color: '#64748b' }}>{label}</span>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="inv-filters">
        <div className="inv-search-box">
          <Search size={15} />
          <input
            placeholder="Search identities by name or email..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <div className="inv-filter-group">
          <Filter size={14} />
          {[['Type', IDENTITY_TYPES, typeFilter, setTypeFilter],
            ['Status', STATUS_TYPES, statusFilter, setStatusFilter],
            ['Risk', RISK_LEVELS, riskFilter, setRiskFilter]].map(
            ([label, options, value, setter]: any) => (
              <select key={label} value={value} onChange={e => setter(e.target.value)} className="inv-select">
                <option value="ALL">{label}: All</option>
                {(options as string[]).filter(o => o !== 'ALL').map(o => (
                  <option key={o} value={o}>{o}</option>
                ))}
              </select>
            )
          )}
        </div>
        <span className="inv-result-count">{filtered.length} results</span>
      </div>

      {/* Table */}
      <div className="inv-table-wrapper">
        <table className="inv-table">
          <thead>
            <tr>
              <th>Identity</th>
              <th>Type</th>
              <th>Provider</th>
              <th>Status</th>
              <th>MFA</th>
              <th>Risk</th>
              <th>Risk Score</th>
              <th>Last Login</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(identity => (
              <tr key={identity.id} className={`inv-row ${selected === identity.id ? 'inv-row-selected' : ''}`}
                onClick={() => setSelected(selected === identity.id ? null : identity.id)}>
                <td>
                  <div className="inv-identity-cell">
                    <div className="inv-avatar" style={{ background: `${RISK_COLORS[identity.risk_level]}20` }}>
                      {TYPE_ICONS[identity.identity_type] || <Users size={14} />}
                    </div>
                    <div>
                      <div className="inv-name">
                        {identity.display_name}
                        {identity.is_privileged && (
                          <span className="inv-priv-badge"><Key size={10} /> Privileged</span>
                        )}
                      </div>
                      <div className="inv-email">{identity.email || '—'}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <span className="inv-type-badge">
                    {TYPE_ICONS[identity.identity_type]}
                    {identity.identity_type.replace('_', ' ')}
                  </span>
                </td>
                <td>
                  <span className="inv-provider-badge">
                    {PROVIDER_LABELS[identity.source_provider] || identity.source_provider}
                  </span>
                </td>
                <td>
                  <span className="inv-status-badge" style={{
                    background: `${STATUS_COLORS[identity.status]}18`,
                    color: STATUS_COLORS[identity.status],
                    borderColor: `${STATUS_COLORS[identity.status]}40`
                  }}>
                    {identity.status}
                  </span>
                </td>
                <td>
                  {identity.mfa_enabled ? (
                    <CheckCircle size={16} color="#10b981" />
                  ) : (
                    <XCircle size={16} color={identity.is_privileged ? '#ef4444' : '#f59e0b'} />
                  )}
                </td>
                <td>
                  <span className="inv-risk-badge" style={{
                    background: `${RISK_COLORS[identity.risk_level]}18`,
                    color: RISK_COLORS[identity.risk_level],
                    borderColor: `${RISK_COLORS[identity.risk_level]}40`
                  }}>
                    {identity.risk_level}
                  </span>
                </td>
                <td>
                  <div className="inv-score-cell">
                    <div className="inv-score-bar">
                      <div style={{
                        width: `${identity.current_risk_score}%`,
                        background: RISK_COLORS[identity.risk_level]
                      }} />
                    </div>
                    <span>{identity.current_risk_score.toFixed(1)}</span>
                  </div>
                </td>
                <td>
                  <div className="inv-login-cell">
                    <Clock size={12} />
                    {identity.days_since_last_login === 0 ? 'Today' :
                      identity.days_since_last_login < 7 ? `${identity.days_since_last_login}d ago` :
                      identity.last_login_at}
                  </div>
                </td>
                <td>
                  <div className="inv-actions">
                    <button className="inv-action-btn" title="View Details"><Eye size={14} /></button>
                    <button className="inv-action-btn" title="AI Analysis"><Brain size={14} /></button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Detail Panel */}
      {selectedIdentity && (
        <div className="inv-detail-panel">
          <div className="inv-detail-header">
            <div className="inv-detail-avatar">
              {TYPE_ICONS[selectedIdentity.identity_type]}
            </div>
            <div>
              <h3>{selectedIdentity.display_name}</h3>
              <p>{selectedIdentity.job_title} · {selectedIdentity.department}</p>
            </div>
            <button onClick={() => setSelected(null)} className="inv-detail-close">✕</button>
          </div>
          <div className="inv-detail-grid">
            {[
              ['Provider', PROVIDER_LABELS[selectedIdentity.source_provider] || selectedIdentity.source_provider],
              ['Status', selectedIdentity.status],
              ['Type', selectedIdentity.identity_type],
              ['MFA', selectedIdentity.mfa_enabled ? 'Enabled ✓' : 'NOT ENABLED ✗'],
              ['Privileged', selectedIdentity.is_privileged ? 'Yes' : 'No'],
              ['Risk Level', selectedIdentity.risk_level],
              ['Risk Score', `${selectedIdentity.current_risk_score.toFixed(1)}/100`],
              ['Days Since Login', `${selectedIdentity.days_since_last_login} days`],
            ].map(([k, v]) => (
              <div key={k} className="inv-detail-row">
                <span>{k}</span>
                <strong style={{ color: k === 'MFA' && !selectedIdentity.mfa_enabled ? '#ef4444' : '#e2e8f0' }}>{v}</strong>
              </div>
            ))}
          </div>
          <div className="inv-detail-actions">
            <button className="inv-detail-btn"><Brain size={14} /> AI Risk Analysis</button>
            <button className="inv-detail-btn"><Eye size={14} /> View Relationships</button>
          </div>
        </div>
      )}
    </div>
  );
}

const INV_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.inv-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; gap: 16px; flex-wrap: wrap; }
.inv-header-left { display: flex; align-items: center; gap: 14px; }
.inv-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.inv-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin: 0 0 2px; }
.inv-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.inv-header-actions { display: flex; gap: 8px; align-items: center; }
.inv-btn-outline { display: flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 9px; font-size: 0.8rem; font-weight: 500; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; cursor: pointer; }
.inv-btn-outline:hover { background: rgba(255,255,255,0.09); color: #e2e8f0; }
.inv-btn-back { display: flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 9px; font-size: 0.8rem; font-weight: 500; background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.35); color: #818cf8; text-decoration: none; }

.inv-stats-row { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.inv-stat-chip { display: flex; flex-direction: column; align-items: center; padding: 12px 18px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 11px; gap: 3px; min-width: 70px; }

.inv-filters { display: flex; gap: 10px; margin-bottom: 16px; align-items: center; flex-wrap: wrap; }
.inv-search-box { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 9px 14px; flex: 1; min-width: 200px; color: #94a3b8; }
.inv-search-box input { background: none; border: none; color: #e2e8f0; font-size: 0.83rem; outline: none; flex: 1; }
.inv-filter-group { display: flex; align-items: center; gap: 8px; color: #64748b; }
.inv-select { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 8px 12px; color: #94a3b8; font-size: 0.8rem; cursor: pointer; outline: none; }
.inv-result-count { font-size: 0.78rem; color: #64748b; white-space: nowrap; }

.inv-table-wrapper { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; overflow: auto; }
.inv-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.inv-table thead tr { border-bottom: 1px solid rgba(255,255,255,0.08); }
.inv-table th { padding: 12px 14px; text-align: left; color: #64748b; font-weight: 500; font-size: 0.75rem; white-space: nowrap; }
.inv-row { border-bottom: 1px solid rgba(255,255,255,0.04); cursor: pointer; transition: background 0.15s; }
.inv-row:hover { background: rgba(255,255,255,0.04); }
.inv-row-selected { background: rgba(99,102,241,0.08) !important; }
.inv-row td { padding: 12px 14px; vertical-align: middle; }

.inv-identity-cell { display: flex; align-items: center; gap: 10px; }
.inv-avatar { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8; flex-shrink: 0; }
.inv-name { color: #e2e8f0; font-weight: 500; font-size: 0.83rem; display: flex; align-items: center; gap: 6px; }
.inv-email { color: #64748b; font-size: 0.72rem; margin-top: 1px; }
.inv-priv-badge { display: inline-flex; align-items: center; gap: 3px; padding: 2px 7px; border-radius: 4px; font-size: 0.65rem; font-weight: 700; background: rgba(239,68,68,0.15); color: #f87171; }

.inv-type-badge { display: inline-flex; align-items: center; gap: 5px; padding: 4px 9px; border-radius: 7px; background: rgba(255,255,255,0.06); color: #94a3b8; font-size: 0.73rem; white-space: nowrap; }
.inv-provider-badge { display: inline-block; padding: 3px 8px; border-radius: 5px; background: rgba(99,102,241,0.12); color: #818cf8; font-size: 0.72rem; }
.inv-status-badge, .inv-risk-badge { display: inline-block; padding: 3px 9px; border-radius: 6px; border: 1px solid; font-size: 0.72rem; font-weight: 600; }
.inv-score-cell { display: flex; align-items: center; gap: 8px; }
.inv-score-bar { width: 60px; height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; }
.inv-score-bar div { height: 100%; border-radius: 3px; transition: width 0.5s; }
.inv-score-cell span { font-size: 0.78rem; color: #94a3b8; }
.inv-login-cell { display: flex; align-items: center; gap: 5px; color: #64748b; font-size: 0.78rem; }
.inv-actions { display: flex; gap: 6px; }
.inv-action-btn { display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 7px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; cursor: pointer; transition: all 0.15s; }
.inv-action-btn:hover { background: rgba(99,102,241,0.15); color: #818cf8; }

.inv-detail-panel { margin-top: 16px; background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.25); border-radius: 14px; padding: 20px; }
.inv-detail-header { display: flex; align-items: center; gap: 14px; margin-bottom: 16px; }
.inv-detail-avatar { width: 42px; height: 42px; background: rgba(99,102,241,0.2); border-radius: 11px; display: flex; align-items: center; justify-content: center; color: #818cf8; }
.inv-detail-header h3 { font-size: 1rem; font-weight: 700; color: #e2e8f0; margin: 0 0 3px; }
.inv-detail-header p { font-size: 0.78rem; color: #64748b; margin: 0; }
.inv-detail-close { margin-left: auto; background: none; border: none; color: #64748b; cursor: pointer; font-size: 1rem; }
.inv-detail-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px; margin-bottom: 16px; }
.inv-detail-row { display: flex; flex-direction: column; gap: 2px; }
.inv-detail-row span { font-size: 0.72rem; color: #64748b; }
.inv-detail-row strong { font-size: 0.85rem; font-weight: 600; }
.inv-detail-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.inv-detail-btn { display: flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 9px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: #94a3b8; font-size: 0.8rem; cursor: pointer; transition: all 0.15s; }
.inv-detail-btn:hover { background: rgba(99,102,241,0.15); color: #818cf8; }
`;
