import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Shield, Users, AlertTriangle, CheckCircle, TrendingUp, TrendingDown,
  Activity, Lock, UserX, Eye, ChevronRight, Zap, RefreshCw, Brain,
  BarChart3, Globe, Key, ShieldAlert, Server, Fingerprint, Network
} from 'lucide-react';

// ─── Mock Data ─────────────────────────────────────────────────────────────

const mockDashboard = {
  total_identities: 847,
  human_identities: 612,
  service_accounts: 148,
  machine_identities: 87,
  privileged_identities: 43,
  dormant_identities: 67,
  orphaned_identities: 12,
  mfa_coverage_pct: 74.2,
  sso_coverage_pct: 68.5,
  passwordless_pct: 18.3,
  privileged_no_mfa_count: 7,
  overall_auth_score: 61.4,
  phishing_resistant_pct: 22.1,
  critical_risk_identities: 23,
  high_risk_identities: 89,
  medium_risk_identities: 201,
  low_risk_identities: 534,
  average_risk_score: 31.7,
  open_governance_findings: 156,
  critical_governance_findings: 18,
  high_governance_findings: 47,
  sod_violations: 8,
  excess_permission_count: 73,
  dormant_privileges: 7,
  admin_sprawl_detected: true,
  zero_trust_score: 42.8,
  zero_trust_maturity: 'INITIAL',
  nist_compliance_pct: 67.3,
  iso27001_compliance_pct: 71.2,
  soc2_compliance_pct: 68.0,
  critical_recommendations: 11,
  total_recommendations: 38,
};

// ─── Components ─────────────────────────────────────────────────────────────

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  trend?: number;
  color: string;
  link?: string;
  badge?: { text: string; color: string };
  urgent?: boolean;
}

const KPICard: React.FC<KPICardProps> = ({
  title, value, subtitle, icon, trend, color, link, badge, urgent
}) => {
  const content = (
    <div className={`ispm-kpi-card ${urgent ? 'ispm-kpi-urgent' : ''}`} style={{ '--accent': color } as any}>
      <div className="ispm-kpi-header">
        <div className="ispm-kpi-icon" style={{ background: `${color}20`, color }}>
          {icon}
        </div>
        {badge && (
          <span className="ispm-kpi-badge" style={{ background: `${badge.color}20`, color: badge.color }}>
            {badge.text}
          </span>
        )}
        {urgent && <span className="ispm-kpi-alert-dot" />}
      </div>
      <div className="ispm-kpi-value">{value}</div>
      <div className="ispm-kpi-title">{title}</div>
      {subtitle && <div className="ispm-kpi-subtitle">{subtitle}</div>}
      {trend !== undefined && (
        <div className={`ispm-kpi-trend ${trend >= 0 ? 'up' : 'down'}`}>
          {trend >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
          <span>{Math.abs(trend)}% vs last month</span>
        </div>
      )}
    </div>
  );

  return link ? (
    <Link to={link} style={{ textDecoration: 'none' }}>{content}</Link>
  ) : content;
};

interface PostureRingProps {
  score: number;
  label: string;
  color: string;
  size?: number;
}

const PostureRing: React.FC<PostureRingProps> = ({ score, label, color, size = 120 }) => {
  const radius = (size - 20) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="ispm-posture-ring-wrapper">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="8" />
        <circle
          cx={size/2} cy={size/2} r={radius}
          fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size/2} ${size/2})`}
          style={{ transition: 'stroke-dashoffset 1s ease' }}
        />
        <text x={size/2} y={size/2 - 6} textAnchor="middle" fill="#fff" fontSize="20" fontWeight="700">
          {Math.round(score)}
        </text>
        <text x={size/2} y={size/2 + 12} textAnchor="middle" fill="rgba(255,255,255,0.5)" fontSize="10">
          {label}
        </text>
      </svg>
    </div>
  );
};

interface RiskBarProps {
  label: string;
  count: number;
  total: number;
  color: string;
}

const RiskBar: React.FC<RiskBarProps> = ({ label, count, total, color }) => {
  const pct = total > 0 ? (count / total) * 100 : 0;
  return (
    <div className="ispm-risk-bar-row">
      <div className="ispm-risk-bar-label">
        <span className="ispm-risk-dot" style={{ background: color }} />
        {label}
      </div>
      <div className="ispm-risk-bar-track">
        <div className="ispm-risk-bar-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="ispm-risk-bar-count">{count}</span>
    </div>
  );
};

// ─── Main Page ──────────────────────────────────────────────────────────────

export default function ISPMDashboard() {
  const [data, setData] = useState(mockDashboard);
  const [loading, setLoading] = useState(false);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  const refresh = () => {
    setLoading(true);
    setTimeout(() => {
      setData({ ...mockDashboard });
      setLastRefresh(new Date());
      setLoading(false);
    }, 900);
  };

  const riskTotal = data.critical_risk_identities + data.high_risk_identities +
    data.medium_risk_identities + data.low_risk_identities;

  return (
    <div className="ispm-page">
      <style>{ISPM_STYLES}</style>

      {/* Header */}
      <div className="ispm-header">
        <div className="ispm-header-left">
          <div className="ispm-header-icon">
            <Fingerprint size={28} />
          </div>
          <div>
            <h1 className="ispm-header-title">Identity Security Posture Management</h1>
            <p className="ispm-header-subtitle">
              Enterprise ISPM Platform · NIST SP 800-63 · NIST SP 800-207 Zero Trust ·
              Last updated {lastRefresh.toLocaleTimeString()}
            </p>
          </div>
        </div>
        <div className="ispm-header-actions">
          <button className="ispm-btn-secondary" onClick={refresh} disabled={loading}>
            <RefreshCw size={15} className={loading ? 'ispm-spin' : ''} />
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
          <Link to="/ispm/executive" className="ispm-btn-primary">
            <Brain size={15} />
            Executive View
          </Link>
          <Link to="/ispm/ai-assistant" className="ispm-btn-ai">
            <Zap size={15} />
            AI Assistant
          </Link>
        </div>
      </div>

      {/* Critical Alert Banner */}
      {data.privileged_no_mfa_count > 0 && (
        <div className="ispm-alert-banner">
          <AlertTriangle size={18} />
          <span>
            <strong>CRITICAL:</strong> {data.privileged_no_mfa_count} privileged accounts have no MFA.
            Immediate action required to prevent credential-based attacks.
          </span>
          <Link to="/ispm/authentication" className="ispm-alert-link">
            Remediate Now <ChevronRight size={14} />
          </Link>
        </div>
      )}

      {/* Posture Score Row */}
      <div className="ispm-posture-row">
        <div className="ispm-posture-card">
          <div className="ispm-posture-rings">
            <PostureRing score={data.mfa_coverage_pct} label="MFA" color="#6366f1" size={110} />
            <PostureRing score={data.zero_trust_score} label="Zero Trust" color="#8b5cf6" size={110} />
            <PostureRing score={data.overall_auth_score} label="Auth Score" color="#06b6d4" size={110} />
            <PostureRing score={data.nist_compliance_pct} label="NIST" color="#10b981" size={110} />
            <PostureRing score={data.iso27001_compliance_pct} label="ISO 27001" color="#f59e0b" size={110} />
          </div>
          <div className="ispm-posture-meta">
            <span className={`ispm-maturity-badge ispm-maturity-${data.zero_trust_maturity.toLowerCase()}`}>
              Zero Trust: {data.zero_trust_maturity} Maturity
            </span>
          </div>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="ispm-kpi-grid">
        <KPICard
          title="Total Identities" value={data.total_identities.toLocaleString()}
          subtitle={`${data.human_identities} human · ${data.service_accounts} service · ${data.machine_identities} machine`}
          icon={<Users size={20} />} color="#6366f1" trend={4.2}
          link="/ispm/inventory"
        />
        <KPICard
          title="Privileged Accounts" value={data.privileged_identities}
          subtitle={`${data.privileged_no_mfa_count} without MFA`}
          icon={<Key size={20} />} color="#ef4444"
          urgent={data.privileged_no_mfa_count > 0}
          badge={data.privileged_no_mfa_count > 0 ? { text: `${data.privileged_no_mfa_count} NO MFA`, color: '#ef4444' } : undefined}
          link="/ispm/authentication"
        />
        <KPICard
          title="Dormant Identities" value={data.dormant_identities}
          subtitle={`${data.orphaned_identities} orphaned accounts`}
          icon={<UserX size={20} />} color="#f97316"
          badge={{ text: 'HYGIENE RISK', color: '#f97316' }}
          link="/ispm/inventory"
        />
        <KPICard
          title="MFA Coverage" value={`${data.mfa_coverage_pct.toFixed(1)}%`}
          subtitle={`${data.passwordless_pct.toFixed(1)}% passwordless capable`}
          icon={<Shield size={20} />} color="#10b981" trend={2.8}
          link="/ispm/authentication"
        />
        <KPICard
          title="Critical Risk Identities" value={data.critical_risk_identities}
          subtitle={`${data.high_risk_identities} high risk`}
          icon={<ShieldAlert size={20} />} color="#ef4444"
          urgent={data.critical_risk_identities > 0}
          link="/ispm/risk"
        />
        <KPICard
          title="Governance Findings" value={data.open_governance_findings}
          subtitle={`${data.critical_governance_findings} critical`}
          icon={<AlertTriangle size={20} />} color="#f59e0b"
          badge={{ text: `${data.sod_violations} SoD`, color: '#f59e0b' }}
          link="/ispm/governance"
        />
        <KPICard
          title="Zero Trust Score" value={`${data.zero_trust_score.toFixed(1)}`}
          subtitle={data.zero_trust_maturity + ' maturity level'}
          icon={<Network size={20} />} color="#8b5cf6" trend={-1.3}
          link="/ispm/zero-trust"
        />
        <KPICard
          title="AI Recommendations" value={data.total_recommendations}
          subtitle={`${data.critical_recommendations} critical priority`}
          icon={<Brain size={20} />} color="#06b6d4"
          link="/ispm/ai-assistant"
        />
      </div>

      {/* Main Content Grid */}
      <div className="ispm-content-grid">
        {/* Risk Distribution */}
        <div className="ispm-section-card">
          <div className="ispm-section-header">
            <BarChart3 size={18} />
            <h3>Identity Risk Distribution</h3>
            <Link to="/ispm/risk" className="ispm-section-link">View All <ChevronRight size={13} /></Link>
          </div>
          <div className="ispm-risk-bars">
            <RiskBar label="Critical" count={data.critical_risk_identities} total={riskTotal} color="#ef4444" />
            <RiskBar label="High" count={data.high_risk_identities} total={riskTotal} color="#f97316" />
            <RiskBar label="Medium" count={data.medium_risk_identities} total={riskTotal} color="#f59e0b" />
            <RiskBar label="Low" count={data.low_risk_identities} total={riskTotal} color="#10b981" />
          </div>
          <div className="ispm-risk-avg">
            <span>Average Risk Score</span>
            <div className="ispm-risk-avg-bar">
              <div style={{ width: `${data.average_risk_score}%`, background: 'linear-gradient(90deg, #10b981, #f59e0b)' }} />
            </div>
            <strong>{data.average_risk_score.toFixed(1)}/100</strong>
          </div>
        </div>

        {/* Identity Type Breakdown */}
        <div className="ispm-section-card">
          <div className="ispm-section-header">
            <Users size={18} />
            <h3>Identity Inventory</h3>
            <Link to="/ispm/inventory" className="ispm-section-link">Inventory <ChevronRight size={13} /></Link>
          </div>
          <div className="ispm-identity-types">
            {[
              { label: 'Human Users', count: data.human_identities, icon: <Users size={16} />, color: '#6366f1' },
              { label: 'Service Accounts', count: data.service_accounts, icon: <Server size={16} />, color: '#8b5cf6' },
              { label: 'Machine Identities', count: data.machine_identities, icon: <Activity size={16} />, color: '#06b6d4' },
              { label: 'Privileged Accounts', count: data.privileged_identities, icon: <Key size={16} />, color: '#ef4444' },
              { label: 'Dormant Identities', count: data.dormant_identities, icon: <UserX size={16} />, color: '#f97316' },
              { label: 'Orphaned Accounts', count: data.orphaned_identities, icon: <AlertTriangle size={16} />, color: '#dc2626' },
            ].map(({ label, count, icon, color }) => (
              <div key={label} className="ispm-identity-type-row">
                <div className="ispm-identity-type-icon" style={{ background: `${color}20`, color }}>{icon}</div>
                <span className="ispm-identity-type-label">{label}</span>
                <div className="ispm-identity-type-bar">
                  <div style={{ width: `${(count / data.total_identities) * 100}%`, background: color, opacity: 0.7 }} />
                </div>
                <span className="ispm-identity-type-count">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Authentication Posture */}
        <div className="ispm-section-card">
          <div className="ispm-section-header">
            <Lock size={18} />
            <h3>Authentication Posture</h3>
            <Link to="/ispm/authentication" className="ispm-section-link">Details <ChevronRight size={13} /></Link>
          </div>
          <div className="ispm-auth-metrics">
            {[
              { label: 'MFA Coverage', pct: data.mfa_coverage_pct, color: '#6366f1', target: 95 },
              { label: 'SSO Coverage', pct: data.sso_coverage_pct, color: '#8b5cf6', target: 80 },
              { label: 'Passwordless', pct: data.passwordless_pct, color: '#06b6d4', target: 50 },
              { label: 'Phishing-Resistant', pct: data.phishing_resistant_pct, color: '#10b981', target: 80 },
            ].map(({ label, pct, color, target }) => (
              <div key={label} className="ispm-auth-metric">
                <div className="ispm-auth-metric-header">
                  <span>{label}</span>
                  <div>
                    <span style={{ color }}>{pct.toFixed(1)}%</span>
                    <span className="ispm-auth-target"> / {target}% target</span>
                  </div>
                </div>
                <div className="ispm-auth-bar">
                  <div style={{ width: `${Math.min(pct, 100)}%`, background: color }} />
                  <div className="ispm-auth-target-line" style={{ left: `${target}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Governance Findings */}
        <div className="ispm-section-card">
          <div className="ispm-section-header">
            <Eye size={18} />
            <h3>Governance Findings</h3>
            <Link to="/ispm/governance" className="ispm-section-link">All Findings <ChevronRight size={13} /></Link>
          </div>
          <div className="ispm-governance-chips">
            {[
              { label: 'SoD Violations', count: data.sod_violations, color: '#ef4444' },
              { label: 'Excess Permissions', count: data.excess_permission_count, color: '#f97316' },
              { label: 'Dormant Privileges', count: data.dormant_privileges, color: '#dc2626' },
              { label: 'Critical Findings', count: data.critical_governance_findings, color: '#7c3aed' },
              { label: 'Admin Sprawl', count: data.admin_sprawl_detected ? 1 : 0, color: '#f59e0b' },
            ].map(({ label, count, color }) => (
              <div key={label} className="ispm-governance-chip" style={{ borderColor: `${color}40`, background: `${color}10` }}>
                <span style={{ color }} className="ispm-chip-count">{count}</span>
                <span className="ispm-chip-label">{label}</span>
              </div>
            ))}
          </div>
          <div className="ispm-governance-total">
            <AlertTriangle size={14} />
            <span>{data.open_governance_findings} open findings requiring remediation</span>
          </div>
        </div>

        {/* Quick Navigation */}
        <div className="ispm-section-card ispm-nav-card">
          <div className="ispm-section-header">
            <Globe size={18} />
            <h3>ISPM Platform Navigation</h3>
          </div>
          <div className="ispm-nav-grid">
            {[
              { label: 'Identity Inventory', path: '/ispm/inventory', icon: <Users size={18} />, color: '#6366f1' },
              { label: 'Access Governance', path: '/ispm/governance', icon: <Eye size={18} />, color: '#f59e0b' },
              { label: 'Authentication', path: '/ispm/authentication', icon: <Lock size={18} />, color: '#10b981' },
              { label: 'Identity Risk', path: '/ispm/risk', icon: <ShieldAlert size={18} />, color: '#ef4444' },
              { label: 'Zero Trust', path: '/ispm/zero-trust', icon: <Network size={18} />, color: '#8b5cf6' },
              { label: 'Compliance', path: '/ispm/compliance', icon: <CheckCircle size={18} />, color: '#06b6d4' },
              { label: 'Historical Trends', path: '/ispm/trends', icon: <TrendingUp size={18} />, color: '#f97316' },
              { label: 'AI Assistant', path: '/ispm/ai-assistant', icon: <Brain size={18} />, color: '#6366f1' },
            ].map(({ label, path, icon, color }) => (
              <Link key={path} to={path} className="ispm-nav-item">
                <div className="ispm-nav-icon" style={{ background: `${color}20`, color }}>{icon}</div>
                <span>{label}</span>
                <ChevronRight size={13} className="ispm-nav-chevron" />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Styles ──────────────────────────────────────────────────────────────────

const ISPM_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.ispm-page {
  font-family: 'Inter', sans-serif;
  background: #0a0a12;
  min-height: 100vh;
  padding: 24px;
  color: #e2e8f0;
  background-image: radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.06) 0%, transparent 60%),
                    radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.05) 0%, transparent 60%);
}

.ispm-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 16px;
  flex-wrap: wrap;
}
.ispm-header-left { display: flex; align-items: center; gap: 16px; }
.ispm-header-icon {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(99,102,241,0.35);
  flex-shrink: 0;
}
.ispm-header-title { font-size: 1.5rem; font-weight: 800; color: #fff; margin: 0 0 4px; }
.ispm-header-subtitle { font-size: 0.78rem; color: #64748b; margin: 0; }
.ispm-header-actions { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }

.ispm-btn-secondary {
  display: flex; align-items: center; gap: 7px;
  padding: 9px 16px; border-radius: 10px; font-size: 0.82rem; font-weight: 500;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
  color: #94a3b8; cursor: pointer; transition: all 0.2s;
}
.ispm-btn-secondary:hover { background: rgba(255,255,255,0.1); color: #e2e8f0; }
.ispm-btn-primary {
  display: flex; align-items: center; gap: 7px;
  padding: 9px 18px; border-radius: 10px; font-size: 0.82rem; font-weight: 600;
  background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.4);
  color: #818cf8; cursor: pointer; transition: all 0.2s; text-decoration: none;
}
.ispm-btn-primary:hover { background: rgba(99,102,241,0.3); color: #a5b4fc; }
.ispm-btn-ai {
  display: flex; align-items: center; gap: 7px;
  padding: 9px 18px; border-radius: 10px; font-size: 0.82rem; font-weight: 600;
  background: linear-gradient(135deg, rgba(99,102,241,0.4), rgba(139,92,246,0.4));
  border: 1px solid rgba(139,92,246,0.5);
  color: #c4b5fd; cursor: pointer; transition: all 0.2s; text-decoration: none;
}
.ispm-btn-ai:hover { background: linear-gradient(135deg, rgba(99,102,241,0.6), rgba(139,92,246,0.6)); }

.ispm-alert-banner {
  display: flex; align-items: center; gap: 12px;
  background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.35);
  border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;
  color: #fca5a5; font-size: 0.84rem;
  animation: ispm-pulse 2s infinite;
}
.ispm-alert-link {
  display: flex; align-items: center; gap: 4px; margin-left: auto;
  color: #f87171; font-weight: 600; text-decoration: none;
  white-space: nowrap; font-size: 0.82rem;
}
.ispm-alert-link:hover { color: #fca5a5; }

@keyframes ispm-pulse {
  0%, 100% { border-color: rgba(239,68,68,0.35); }
  50% { border-color: rgba(239,68,68,0.6); }
}

/* Posture Row */
.ispm-posture-row { margin-bottom: 20px; }
.ispm-posture-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 20px 28px;
  display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
}
.ispm-posture-rings { display: flex; gap: 24px; align-items: center; flex-wrap: wrap; flex: 1; }
.ispm-posture-ring-wrapper { display: flex; flex-direction: column; align-items: center; }
.ispm-posture-meta { margin-left: auto; }
.ispm-maturity-badge {
  padding: 6px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
}
.ispm-maturity-initial { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.ispm-maturity-advanced { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); }
.ispm-maturity-optimal { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.ispm-maturity-traditional { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

/* KPI Grid */
.ispm-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 14px;
  margin-bottom: 20px;
}
.ispm-kpi-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px; padding: 18px; position: relative; overflow: hidden;
  transition: all 0.25s; cursor: default;
}
.ispm-kpi-card:hover { background: rgba(255,255,255,0.055); transform: translateY(-2px); }
.ispm-kpi-urgent { border-color: rgba(239,68,68,0.3) !important; animation: ispm-pulse 2s infinite; }
.ispm-kpi-header { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.ispm-kpi-icon { width: 36px; height: 36px; border-radius: 9px; display: flex; align-items: center; justify-content: center; }
.ispm-kpi-badge { padding: 3px 9px; border-radius: 20px; font-size: 0.68rem; font-weight: 700; margin-left: auto; }
.ispm-kpi-alert-dot {
  position: absolute; top: 14px; right: 14px;
  width: 8px; height: 8px; border-radius: 50%; background: #ef4444;
  box-shadow: 0 0 0 3px rgba(239,68,68,0.25);
  animation: ispm-blink 1s infinite;
}
@keyframes ispm-blink { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }
.ispm-kpi-value { font-size: 1.8rem; font-weight: 800; color: #f1f5f9; line-height: 1; margin-bottom: 4px; }
.ispm-kpi-title { font-size: 0.78rem; font-weight: 500; color: #64748b; margin-bottom: 3px; }
.ispm-kpi-subtitle { font-size: 0.72rem; color: #475569; }
.ispm-kpi-trend { display: flex; align-items: center; gap: 4px; margin-top: 8px; font-size: 0.72rem; }
.ispm-kpi-trend.up { color: #10b981; }
.ispm-kpi-trend.down { color: #ef4444; }

/* Content Grid */
.ispm-content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
@media (max-width: 1100px) { .ispm-content-grid { grid-template-columns: 1fr; } }

.ispm-section-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 20px;
}
.ispm-section-header {
  display: flex; align-items: center; gap: 10px; margin-bottom: 18px;
  color: #94a3b8; font-size: 0.82rem;
}
.ispm-section-header h3 { font-size: 0.95rem; font-weight: 600; color: #e2e8f0; margin: 0; flex: 1; }
.ispm-section-link {
  display: flex; align-items: center; gap: 3px;
  color: #6366f1; font-size: 0.78rem; font-weight: 500; text-decoration: none; white-space: nowrap;
}
.ispm-section-link:hover { color: #818cf8; }

/* Risk Bars */
.ispm-risk-bars { display: flex; flex-direction: column; gap: 10px; margin-bottom: 16px; }
.ispm-risk-bar-row { display: flex; align-items: center; gap: 10px; }
.ispm-risk-bar-label { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #94a3b8; min-width: 70px; }
.ispm-risk-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.ispm-risk-bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; }
.ispm-risk-bar-fill { height: 100%; border-radius: 3px; transition: width 0.8s ease; }
.ispm-risk-bar-count { font-size: 0.8rem; font-weight: 600; color: #e2e8f0; min-width: 32px; text-align: right; }
.ispm-risk-avg { display: flex; align-items: center; gap: 10px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.8rem; color: #64748b; }
.ispm-risk-avg-bar { flex: 1; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; }
.ispm-risk-avg-bar div { height: 100%; border-radius: 3px; transition: width 0.8s ease; }
.ispm-risk-avg strong { color: #f1f5f9; font-weight: 700; }

/* Identity Types */
.ispm-identity-types { display: flex; flex-direction: column; gap: 10px; }
.ispm-identity-type-row { display: flex; align-items: center; gap: 10px; }
.ispm-identity-type-icon { width: 30px; height: 30px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ispm-identity-type-label { font-size: 0.8rem; color: #94a3b8; min-width: 130px; }
.ispm-identity-type-bar { flex: 1; height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; }
.ispm-identity-type-bar div { height: 100%; border-radius: 3px; transition: width 0.8s ease; }
.ispm-identity-type-count { font-size: 0.8rem; font-weight: 600; color: #e2e8f0; min-width: 36px; text-align: right; }

/* Auth Metrics */
.ispm-auth-metrics { display: flex; flex-direction: column; gap: 14px; }
.ispm-auth-metric {}
.ispm-auth-metric-header { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.8rem; }
.ispm-auth-metric-header span { color: #94a3b8; }
.ispm-auth-target { color: #475569; font-size: 0.75rem; }
.ispm-auth-bar { height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: visible; position: relative; }
.ispm-auth-bar div { height: 100%; border-radius: 3px; transition: width 0.8s ease; }
.ispm-auth-target-line { position: absolute; top: -3px; width: 2px; height: 12px; background: rgba(255,255,255,0.25); }

/* Governance Chips */
.ispm-governance-chips { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; }
.ispm-governance-chip {
  border-radius: 10px; padding: 10px 14px; border: 1px solid;
  display: flex; flex-direction: column; align-items: center; gap: 2px; min-width: 90px;
}
.ispm-chip-count { font-size: 1.5rem; font-weight: 800; line-height: 1; }
.ispm-chip-label { font-size: 0.7rem; color: #64748b; text-align: center; }
.ispm-governance-total {
  display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #f59e0b;
  padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06);
}

/* Nav Grid */
.ispm-nav-card { grid-column: 1 / -1; }
.ispm-nav-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(175px, 1fr)); gap: 10px; }
.ispm-nav-item {
  display: flex; align-items: center; gap: 10px; padding: 12px 14px;
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
  border-radius: 11px; text-decoration: none; color: #94a3b8;
  font-size: 0.82rem; font-weight: 500; transition: all 0.2s;
}
.ispm-nav-item:hover { background: rgba(255,255,255,0.07); color: #e2e8f0; transform: translateX(2px); }
.ispm-nav-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ispm-nav-chevron { margin-left: auto; opacity: 0.4; }
.ispm-nav-item:hover .ispm-nav-chevron { opacity: 0.8; }

.ispm-spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
`;
