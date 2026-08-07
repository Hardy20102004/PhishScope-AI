import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Eye, AlertTriangle, ChevronRight, Filter, CheckCircle, XCircle, Shield, Key, Users, Clock } from 'lucide-react';

const FINDINGS = [
  { id: '1', finding_type: 'DORMANT_PRIVILEGE', severity: 'CRITICAL', title: 'Dormant Privileged Account: orphaned-svc-legacy', status: 'OPEN', affected_identity_name: 'orphaned-svc-legacy', detected_at: '2026-07-28', business_impact: 'CRITICAL', compliance_frameworks: ['NIST_AC-2', 'ISO27001_A.9.2.6'] },
  { id: '2', finding_type: 'ADMIN_SPRAWL', severity: 'HIGH', title: 'Administrative Account Sprawl Detected', status: 'OPEN', affected_identity_name: 'Tenant-Wide', detected_at: '2026-07-29', business_impact: 'HIGH', compliance_frameworks: ['NIST_AC-6(5)', 'CIS_CSC_5.3'] },
  { id: '3', finding_type: 'EXCESSIVE_PERMISSION', severity: 'HIGH', title: 'Excessive Permissions: svc-payroll-api', status: 'OPEN', affected_identity_name: 'svc-payroll-api', detected_at: '2026-07-27', business_impact: 'HIGH', compliance_frameworks: ['NIST_AC-6', 'ISO27001_A.9.4.1'] },
  { id: '4', finding_type: 'SOD_CONFLICT', severity: 'CRITICAL', title: 'SoD Conflict: Finance + Payroll Approval', status: 'OPEN', affected_identity_name: 'Maria Garcia', detected_at: '2026-07-26', business_impact: 'CRITICAL', compliance_frameworks: ['SOX_ITGC'] },
  { id: '5', finding_type: 'CERTIFICATION_OVERDUE', severity: 'MEDIUM', title: 'Access Certification Overdue: David Chen', status: 'OPEN', affected_identity_name: 'David Chen', detected_at: '2026-07-20', business_impact: 'MEDIUM', compliance_frameworks: ['SOX_ITGC', 'ISO27001_A.9.2.5'] },
  { id: '6', finding_type: 'EXCESSIVE_PERMISSION', severity: 'MEDIUM', title: 'Excessive Permissions: Zhang Wei', status: 'IN_REMEDIATION', affected_identity_name: 'Zhang Wei', detected_at: '2026-07-15', business_impact: 'MEDIUM', compliance_frameworks: ['NIST_AC-6'] },
  { id: '7', finding_type: 'DORMANT_PRIVILEGE', severity: 'HIGH', title: 'Dormant Privileged Account: David Chen', status: 'OPEN', affected_identity_name: 'David Chen', detected_at: '2026-07-29', business_impact: 'HIGH', compliance_frameworks: ['NIST_AC-2(3)'] },
  { id: '8', finding_type: 'ORPHANED_ACCESS', severity: 'HIGH', title: 'Orphaned Access: Legacy App Permissions', status: 'OPEN', affected_identity_name: 'Robert Johnson', detected_at: '2026-07-18', business_impact: 'HIGH', compliance_frameworks: ['NIST_AC-2'] },
];

const SEV_COLORS: Record<string, string> = { CRITICAL: '#ef4444', HIGH: '#f97316', MEDIUM: '#f59e0b', LOW: '#10b981' };
const STATUS_COLORS: Record<string, string> = { OPEN: '#ef4444', IN_REMEDIATION: '#f59e0b', RESOLVED: '#10b981', ACCEPTED_RISK: '#64748b' };
const TYPE_LABELS: Record<string, string> = {
  DORMANT_PRIVILEGE: 'Dormant Privilege', ADMIN_SPRAWL: 'Admin Sprawl',
  EXCESSIVE_PERMISSION: 'Excess Permission', SOD_CONFLICT: 'SoD Conflict',
  CERTIFICATION_OVERDUE: 'Cert Overdue', ORPHANED_ACCESS: 'Orphaned Access',
  POLICY_GAP: 'Policy Gap'
};

export default function AccessGovernanceDashboard() {
  const [filter, setFilter] = useState('ALL');
  const [selected, setSelected] = useState<string | null>(null);

  const filtered = filter === 'ALL' ? FINDINGS : FINDINGS.filter(f => f.severity === filter || f.finding_type === filter || f.status === filter);
  const selectedFinding = selected ? FINDINGS.find(f => f.id === selected) : null;

  const summary = {
    total: FINDINGS.length,
    critical: FINDINGS.filter(f => f.severity === 'CRITICAL').length,
    high: FINDINGS.filter(f => f.severity === 'HIGH').length,
    sod: FINDINGS.filter(f => f.finding_type === 'SOD_CONFLICT').length,
    excess: FINDINGS.filter(f => f.finding_type === 'EXCESSIVE_PERMISSION').length,
    dormant: FINDINGS.filter(f => f.finding_type === 'DORMANT_PRIVILEGE').length,
    open: FINDINGS.filter(f => f.status === 'OPEN').length,
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{GOV_STYLES}</style>
      <div className="gov-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="gov-icon"><Eye size={24} /></div>
          <div>
            <h1 className="gov-title">Access Governance</h1>
            <p className="gov-subtitle">SoD Conflicts · Excess Permissions · Dormant Privilege · Policy Gaps · Certification Overdue</p>
          </div>
        </div>
        <Link to="/ispm" style={{ textDecoration: 'none', color: '#818cf8', fontSize: '0.82rem', fontWeight: 500, padding: '8px 14px', background: 'rgba(99,102,241,0.12)', borderRadius: 9, border: '1px solid rgba(99,102,241,0.3)' }}>← ISPM</Link>
      </div>

      {/* Summary Cards */}
      <div className="gov-summary-grid">
        {[
          { label: 'Open Findings', value: summary.open, color: '#ef4444', icon: <AlertTriangle size={18} /> },
          { label: 'Critical', value: summary.critical, color: '#dc2626', icon: <Shield size={18} /> },
          { label: 'High', value: summary.high, color: '#f97316', icon: <AlertTriangle size={18} /> },
          { label: 'SoD Violations', value: summary.sod, color: '#7c3aed', icon: <Users size={18} /> },
          { label: 'Excess Permissions', value: summary.excess, color: '#f59e0b', icon: <Key size={18} /> },
          { label: 'Dormant Privileges', value: summary.dormant, color: '#ef4444', icon: <Clock size={18} /> },
        ].map(({ label, value, color, icon }) => (
          <div key={label} className="gov-summary-card" style={{ borderColor: `${color}30` }}>
            <div style={{ color, marginBottom: 6 }}>{icon}</div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color }}>{value}</div>
            <div style={{ fontSize: '0.72rem', color: '#64748b' }}>{label}</div>
          </div>
        ))}
      </div>

      {/* Filter Bar */}
      <div className="gov-filter-bar">
        {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'SOD_CONFLICT', 'EXCESSIVE_PERMISSION', 'DORMANT_PRIVILEGE', 'OPEN', 'IN_REMEDIATION'].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`gov-filter-btn ${filter === f ? 'gov-filter-active' : ''}`}>{f.replace(/_/g, ' ')}</button>
        ))}
      </div>

      {/* Findings Table */}
      <div className="gov-table-wrapper">
        <table className="gov-table">
          <thead>
            <tr>
              <th>Severity</th><th>Type</th><th>Finding</th><th>Identity</th>
              <th>Status</th><th>Frameworks</th><th>Detected</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(f => (
              <tr key={f.id} className={`gov-row ${selected === f.id ? 'gov-row-selected' : ''}`} onClick={() => setSelected(selected === f.id ? null : f.id)}>
                <td>
                  <span className="gov-sev-badge" style={{ background: `${SEV_COLORS[f.severity]}18`, color: SEV_COLORS[f.severity], borderColor: `${SEV_COLORS[f.severity]}40` }}>
                    {f.severity}
                  </span>
                </td>
                <td><span className="gov-type-badge">{TYPE_LABELS[f.finding_type] || f.finding_type}</span></td>
                <td><span className="gov-title-cell">{f.title}</span></td>
                <td><span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>{f.affected_identity_name}</span></td>
                <td>
                  <span className="gov-status-badge" style={{ background: `${STATUS_COLORS[f.status]}18`, color: STATUS_COLORS[f.status], borderColor: `${STATUS_COLORS[f.status]}40` }}>
                    {f.status.replace('_', ' ')}
                  </span>
                </td>
                <td>
                  <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                    {f.compliance_frameworks.slice(0, 2).map(fw => (
                      <span key={fw} className="gov-fw-badge">{fw}</span>
                    ))}
                  </div>
                </td>
                <td><span style={{ color: '#64748b', fontSize: '0.78rem' }}>{f.detected_at}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedFinding && (
        <div className="gov-detail-panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 14 }}>
            <div>
              <span className="gov-sev-badge" style={{ background: `${SEV_COLORS[selectedFinding.severity]}18`, color: SEV_COLORS[selectedFinding.severity], borderColor: `${SEV_COLORS[selectedFinding.severity]}40`, marginRight: 10 }}>{selectedFinding.severity}</span>
              <strong style={{ color: '#e2e8f0' }}>{selectedFinding.title}</strong>
            </div>
            <button onClick={() => setSelected(null)} style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontSize: '1rem' }}>✕</button>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: 12, marginBottom: 14 }}>
            {[['Finding Type', TYPE_LABELS[selectedFinding.finding_type]], ['Affected Identity', selectedFinding.affected_identity_name], ['Business Impact', selectedFinding.business_impact], ['Status', selectedFinding.status], ['Detected', selectedFinding.detected_at]].map(([k, v]) => (
              <div key={k}>
                <div style={{ fontSize: '0.7rem', color: '#64748b', marginBottom: 2 }}>{k}</div>
                <strong style={{ fontSize: '0.85rem', color: '#e2e8f0' }}>{v}</strong>
              </div>
            ))}
          </div>
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: 6 }}>Compliance Frameworks</div>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {selectedFinding.compliance_frameworks.map(fw => <span key={fw} className="gov-fw-badge">{fw}</span>)}
            </div>
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="gov-action-btn">Mark In Remediation</button>
            <button className="gov-action-btn">Accept Risk</button>
            <button className="gov-action-btn gov-action-resolve">Mark Resolved</button>
          </div>
        </div>
      )}
    </div>
  );
}

const GOV_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.gov-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; gap: 16px; flex-wrap: wrap; }
.gov-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b, #f97316); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.gov-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin: 0 0 2px; }
.gov-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.gov-summary-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px; margin-bottom: 16px; }
.gov-summary-card { display: flex; flex-direction: column; align-items: center; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.gov-filter-bar { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 14px; }
.gov-filter-btn { padding: 6px 12px; border-radius: 7px; font-size: 0.75rem; font-weight: 500; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); color: #64748b; cursor: pointer; transition: all 0.15s; }
.gov-filter-btn:hover { background: rgba(255,255,255,0.08); color: #94a3b8; }
.gov-filter-active { background: rgba(99,102,241,0.15) !important; border-color: rgba(99,102,241,0.4) !important; color: #818cf8 !important; }
.gov-table-wrapper { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; overflow: auto; margin-bottom: 14px; }
.gov-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.gov-table th { color: #64748b; font-weight: 500; padding: 11px 13px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.07); font-size: 0.75rem; }
.gov-row { border-bottom: 1px solid rgba(255,255,255,0.04); cursor: pointer; transition: background 0.15s; }
.gov-row:hover { background: rgba(255,255,255,0.04); }
.gov-row-selected { background: rgba(99,102,241,0.07) !important; }
.gov-row td { padding: 11px 13px; vertical-align: middle; }
.gov-sev-badge, .gov-status-badge { display: inline-block; padding: 3px 9px; border-radius: 6px; border: 1px solid; font-size: 0.72rem; font-weight: 700; }
.gov-type-badge { padding: 3px 9px; border-radius: 6px; background: rgba(255,255,255,0.06); color: #94a3b8; font-size: 0.72rem; white-space: nowrap; }
.gov-title-cell { color: #e2e8f0; font-size: 0.82rem; font-weight: 500; }
.gov-fw-badge { padding: 2px 7px; border-radius: 4px; background: rgba(99,102,241,0.12); color: #818cf8; font-size: 0.68rem; font-weight: 600; }
.gov-detail-panel { background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.25); border-radius: 14px; padding: 20px; }
.gov-action-btn { padding: 8px 16px; border-radius: 9px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: #94a3b8; font-size: 0.8rem; cursor: pointer; transition: all 0.15s; }
.gov-action-btn:hover { background: rgba(255,255,255,0.1); color: #e2e8f0; }
.gov-action-resolve { background: rgba(16,185,129,0.12) !important; border-color: rgba(16,185,129,0.3) !important; color: #34d399 !important; }
`;
