import React, { useState, useEffect } from 'react';
import api from '../../services/api';

interface AppSecConsolidatedFinding {
  id: string;
  application_id: string;
  source_scanner: string;
  severity: string;
  cwe_id: string;
  title: string;
  is_remediated: boolean;
  created_at: string;
}

const severityColor = (s: string) => {
  if (s === 'CRITICAL' || s === 'HIGH') return '#ef4444';
  if (s === 'MEDIUM') return '#f59e0b';
  return '#6b7280';
};

export const UnifiedAppSecDashboard: React.FC = () => {
  const [findings, setFindings] = useState<AppSecConsolidatedFinding[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/api/v1/appsec-command-center/consolidated-findings')
      .then(r => setFindings(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ padding: '24px', fontFamily: 'Inter, sans-serif' }}>
      <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '24px', color: '#f1f5f9' }}>
        Unified Application Security Command Center
      </h1>
      {loading ? (
        <p style={{ color: '#94a3b8' }}>Loading findings...</p>
      ) : (
        <div style={{ background: '#1e293b', borderRadius: '12px', overflow: 'hidden', border: '1px solid #334155' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#0f172a' }}>
                {['Application', 'Scanner', 'Severity', 'CWE ID', 'Vulnerability', 'Status', 'Date'].map(h => (
                  <th key={h} style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: 600, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {findings.length === 0 ? (
                <tr><td colSpan={7} style={{ padding: '24px', textAlign: 'center', color: '#64748b' }}>No consolidated findings available</td></tr>
              ) : findings.map((f, i) => (
                <tr key={f.id} style={{ borderTop: '1px solid #334155', background: i % 2 === 0 ? 'transparent' : '#0f172a22' }}>
                  <td style={{ padding: '12px 16px', color: '#f1f5f9', fontWeight: 600 }}>{f.application_id}</td>
                  <td style={{ padding: '12px 16px' }}>
                    <span style={{ background: '#1d4ed833', color: '#60a5fa', border: '1px solid #1d4ed855', borderRadius: '6px', padding: '2px 8px', fontSize: '12px' }}>{f.source_scanner}</span>
                  </td>
                  <td style={{ padding: '12px 16px' }}>
                    <span style={{ background: severityColor(f.severity) + '22', color: severityColor(f.severity), border: `1px solid ${severityColor(f.severity)}55`, borderRadius: '6px', padding: '2px 8px', fontSize: '12px', fontWeight: 600 }}>{f.severity}</span>
                  </td>
                  <td style={{ padding: '12px 16px', color: '#94a3b8' }}>{f.cwe_id || 'N/A'}</td>
                  <td style={{ padding: '12px 16px', color: '#e2e8f0' }}>{f.title}</td>
                  <td style={{ padding: '12px 16px' }}>
                    <span style={{ background: f.is_remediated ? '#16a34a22' : '#64748b22', color: f.is_remediated ? '#4ade80' : '#94a3b8', borderRadius: '6px', padding: '2px 8px', fontSize: '12px' }}>
                      {f.is_remediated ? 'Remediated' : 'Open'}
                    </span>
                  </td>
                  <td style={{ padding: '12px 16px', color: '#64748b', fontSize: '12px' }}>{new Date(f.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
