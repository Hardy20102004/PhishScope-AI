import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function AlertQueue() {
  const navigate = useNavigate();
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    // Mock data for the UI
    setAlerts([
      {
        id: '123e4567-e89b-12d3-a456-426614174001',
        title: 'Suspicious PowerShell Execution',
        source: 'CrowdStrike EDR',
        severity: 'HIGH',
        status: 'NEW',
        priority_score: 85,
        created_at: '2026-07-27T10:15:00Z',
      },
      {
        id: '123e4567-e89b-12d3-a456-426614174002',
        title: 'Multiple Failed Logins',
        source: 'Okta',
        severity: 'MEDIUM',
        status: 'IN_INVESTIGATION',
        priority_score: 65,
        created_at: '2026-07-27T09:30:00Z',
      },
      {
        id: '123e4567-e89b-12d3-a456-426614174003',
        title: 'Malware Detected: Emotet Payload',
        source: 'Palo Alto Firewall',
        severity: 'CRITICAL',
        status: 'NEW',
        priority_score: 98,
        created_at: '2026-07-27T11:05:00Z',
      },
    ]);
  }, []);

  const getSeverityBadge = (severity: str) => {
    const s = severity.toLowerCase();
    return <span className={`severity-badge severity-${s}`}>{severity}</span>;
  };

  return (
    <div className="alert-queue">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-200">Active Alert Queue</h2>
        <input 
          type="text" 
          placeholder="Search alerts..." 
          className="bg-gray-800 border border-gray-700 text-white rounded px-3 py-1.5 focus:outline-none focus:border-blue-500"
        />
      </div>
      
      <table className="alert-queue-table">
        <thead>
          <tr>
            <th>Severity</th>
            <th>Title</th>
            <th>Source</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.id} onClick={() => navigate(`/alerts/${alert.id}`)}>
              <td>{getSeverityBadge(alert.severity)}</td>
              <td className="font-medium text-blue-400">{alert.title}</td>
              <td>{alert.source}</td>
              <td>
                <div className="flex items-center gap-2">
                  <div className="w-16 h-2 bg-gray-700 rounded overflow-hidden">
                    <div 
                      className="h-full bg-blue-500" 
                      style={{ width: `${alert.priority_score}%` }} 
                    />
                  </div>
                  <span>{alert.priority_score}</span>
                </div>
              </td>
              <td>{alert.status}</td>
              <td className="text-gray-400">{new Date(alert.created_at).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
