import React, { useState, useEffect } from 'react';
import api from '../../services/api';

interface AppSecExecutiveMetric {
  id: string;
  enterprise_risk_score: number;
  compliance_posture: number;
  total_critical_vulnerabilities: number;
}

export const AppSecExecutiveBoard: React.FC = () => {
  const [metrics, setMetrics] = useState<AppSecExecutiveMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [proposing, setProposing] = useState(false);

  useEffect(() => {
    api.get('/api/v1/appsec-command-center/executive-summary')
      .then(r => setMetrics(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleProposeDecision = async () => {
    setProposing(true);
    try {
      await api.post('/api/v1/appsec-command-center/governance', {
        policy_name: "Enforce SAST Blocking Across Enterprise",
        proposed_change: "Modify CI/CD pipeline template to block merge requests with HIGH/CRITICAL SAST findings."
      });
      alert('✅ Governance Decision Proposed Successfully!\n\nAwaiting Architect Approval.');
    } catch {
      alert('❌ Failed to propose decision. Please try again.');
    } finally {
      setProposing(false);
    }
  };

  const m = metrics[0];

  return (
    <div style={{ padding: '24px', fontFamily: 'Inter, sans-serif' }}>
      <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '8px', color: '#f1f5f9' }}>
        AppSec Executive & Board Presentation
      </h1>
      <p style={{ color: '#64748b', marginBottom: '32px' }}>Enterprise-wide application security posture for executive leadership</p>

      {loading ? (
        <p style={{ color: '#94a3b8' }}>Loading executive metrics...</p>
      ) : !m ? (
        <p style={{ color: '#64748b' }}>No executive metrics available.</p>
      ) : (
        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
          {[
            { label: 'Enterprise Risk Score', value: `${m.enterprise_risk_score.toFixed(1)} / 100`, color: m.enterprise_risk_score > 50 ? '#ef4444' : '#4ade80', sub: m.enterprise_risk_score > 50 ? 'Elevated Risk' : 'Acceptable Risk' },
            { label: 'Compliance Posture', value: `${m.compliance_posture.toFixed(1)}%`, color: m.compliance_posture < 80 ? '#ef4444' : '#4ade80', sub: m.compliance_posture < 80 ? 'Below Target' : 'On Target' },
            { label: 'Critical Vulnerabilities', value: String(m.total_critical_vulnerabilities), color: m.total_critical_vulnerabilities > 0 ? '#ef4444' : '#4ade80', sub: m.total_critical_vulnerabilities > 0 ? 'Immediate Action' : 'Clear' },
          ].map(card => (
            <div key={card.label} style={{ flex: 1, minWidth: '200px', background: '#1e293b', border: `1px solid ${card.color}33`, borderRadius: '16px', padding: '28px', textAlign: 'center' }}>
              <p style={{ color: '#64748b', fontSize: '12px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '16px' }}>{card.label}</p>
              <p style={{ color: card.color, fontSize: '40px', fontWeight: 800, marginBottom: '8px' }}>{card.value}</p>
              <span style={{ background: card.color + '22', color: card.color, borderRadius: '99px', padding: '4px 12px', fontSize: '12px', fontWeight: 600 }}>{card.sub}</span>
            </div>
          ))}
        </div>
      )}

      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '16px', padding: '28px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 700, color: '#f1f5f9', marginBottom: '8px' }}>Strategic Governance</h2>
        <p style={{ color: '#64748b', marginBottom: '20px' }}>
          Propose a human-governed strategic policy adjustment impacting the entire application portfolio. All changes require explicit architect approval before enforcement.
        </p>
        <button
          onClick={handleProposeDecision}
          disabled={proposing}
          style={{
            background: proposing ? '#334155' : 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            color: '#fff', border: 'none', borderRadius: '10px', padding: '12px 28px',
            fontSize: '14px', fontWeight: 600, cursor: proposing ? 'not-allowed' : 'pointer',
            opacity: proposing ? 0.7 : 1, transition: 'all 0.2s'
          }}
        >
          {proposing ? 'Proposing...' : '🔒 Propose Enterprise Policy Change'}
        </button>
      </div>
    </div>
  );
};
