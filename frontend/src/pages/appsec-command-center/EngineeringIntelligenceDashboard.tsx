import React, { useState, useEffect } from 'react';
import api from '../../services/api';

interface EngineeringProductivityMetric {
  id: string;
  application_id: string;
  mean_time_to_remediate_days: number;
  deployment_frequency_per_week: number;
  security_friction_score: number;
}

const MetricCard: React.FC<{ label: string; value: string; color: string }> = ({ label, value, color }) => (
  <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '20px', flex: 1 }}>
    <p style={{ color: '#64748b', fontSize: '12px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>{label}</p>
    <p style={{ color, fontSize: '32px', fontWeight: 700 }}>{value}</p>
  </div>
);

export const EngineeringIntelligenceDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<EngineeringProductivityMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/api/v1/appsec-command-center/engineering-intelligence')
      .then(r => setMetrics(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ padding: '24px', fontFamily: 'Inter, sans-serif' }}>
      <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '8px', color: '#f1f5f9' }}>
        DevSecOps Intelligence & Engineering Productivity
      </h1>
      <p style={{ color: '#64748b', marginBottom: '32px' }}>Real-time engineering metrics and security operational KPIs</p>

      {loading ? (
        <p style={{ color: '#94a3b8' }}>Loading metrics...</p>
      ) : metrics.length === 0 ? (
        <p style={{ color: '#64748b' }}>No DevSecOps intelligence data available.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {metrics.map(m => (
            <div key={m.id}>
              <h2 style={{ color: '#94a3b8', marginBottom: '12px', fontSize: '14px' }}>Application: <strong style={{ color: '#60a5fa' }}>{m.application_id}</strong></h2>
              <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                <MetricCard label="Mean Time To Remediate" value={`${m.mean_time_to_remediate_days.toFixed(1)} days`} color={m.mean_time_to_remediate_days > 7 ? '#ef4444' : '#4ade80'} />
                <MetricCard label="Deployment Frequency" value={`${m.deployment_frequency_per_week.toFixed(1)} / week`} color="#60a5fa" />
                <MetricCard label="Security Friction Score" value={m.security_friction_score.toFixed(1)} color={m.security_friction_score > 50 ? '#ef4444' : '#4ade80'} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
