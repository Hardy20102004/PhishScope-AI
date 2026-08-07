import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './AlertStyles.css';

export default function AlertDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Mock data for the specific alert
  const alert = {
    id,
    title: 'Suspicious PowerShell Execution',
    source: 'CrowdStrike EDR',
    severity: 'HIGH',
    status: 'NEW',
    priority_score: 85,
    risk_score: 75,
    confidence: 90,
    created_at: '2026-07-27T10:15:00Z',
    ai_summary: 'AI Analysis: This alert from CrowdStrike EDR requires immediate investigation. The execution of a highly obfuscated PowerShell script with Base64 encoding is indicative of a dropper malware. The parent process is winword.exe, suggesting a malicious macro payload. Recommended action: Isolate host and extract memory dump.',
    mitre_techniques: {
      'T1059.001': 'PowerShell',
      'T1132.001': 'Standard Encoding',
    },
    evidence: [
      { type: 'HOST', value: 'DESKTOP-FINANCE-01' },
      { type: 'USER', value: 'jdoe@enterprise.com' },
      { type: 'HASH', value: 'a4b5c6d7e8f9a4b5c6d7e8f9a4b5c6d7' },
    ]
  };

  return (
    <div className="alert-dashboard-container">
      <div className="mb-4 flex items-center gap-4">
        <button 
          onClick={() => navigate('/alerts')}
          className="text-gray-400 hover:text-white transition"
        >
          &larr; Back to Queue
        </button>
      </div>

      <div className="alert-header">
        <div>
          <h1>{alert.title}</h1>
          <div className="mt-2 text-sm text-gray-400 flex items-center gap-4">
            <span>ID: {alert.id}</span>
            <span>|</span>
            <span>Source: {alert.source}</span>
            <span>|</span>
            <span>{new Date(alert.created_at).toLocaleString()}</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 bg-gray-800 border border-gray-700 text-white rounded hover:bg-gray-700 transition">
            Acknowledge
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            Assign to me
          </button>
        </div>
      </div>

      <div className="alert-detail-grid">
        <div className="flex flex-col gap-6">
          <div className="detail-section">
            <h2>AI Security Brain Summary</h2>
            <div className="ai-summary-box">
              {alert.ai_summary}
            </div>
          </div>

          <div className="detail-section">
            <h2>Evidence Artifacts</h2>
            <div className="evidence-list">
              {alert.evidence.map((ev, i) => (
                <div key={i} className="evidence-item">
                  <span className="text-gray-400 text-sm font-mono">{ev.type}</span>
                  <span className="text-white font-medium">{ev.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="detail-section">
            <h2>Risk Assessment</h2>
            <div className="flex flex-col gap-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Severity</span>
                <span className="severity-badge severity-high">{alert.severity}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Priority Score</span>
                <span className="text-xl font-bold text-white">{alert.priority_score}/100</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">AI Confidence</span>
                <span className="text-xl font-bold text-white">{alert.confidence}%</span>
              </div>
            </div>
          </div>

          <div className="detail-section">
            <h2>MITRE ATT&CK</h2>
            <div className="flex flex-col gap-2">
              {Object.entries(alert.mitre_techniques).map(([id, name]) => (
                <div key={id} className="p-2 bg-gray-800 rounded border border-gray-700 flex flex-col">
                  <span className="text-blue-400 text-sm font-mono">{id}</span>
                  <span className="text-gray-300 text-sm">{name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
