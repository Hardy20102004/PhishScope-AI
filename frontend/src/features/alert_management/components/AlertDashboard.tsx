import React, { useState, useEffect } from 'react';
import './AlertStyles.css';
import AlertQueue from './AlertQueue';

export default function AlertDashboard() {
  const [metrics, setMetrics] = useState({
    activeAlerts: 0,
    criticalAlerts: 0,
    mtta: '15m',
    mttr: '2h 30m',
  });

  // In a real implementation, this would fetch from the analytics API endpoint
  useEffect(() => {
    setMetrics({
      activeAlerts: 124,
      criticalAlerts: 12,
      mtta: '8m',
      mttr: '1h 45m',
    });
  }, []);

  return (
    <div className="alert-dashboard-container">
      <div className="alert-header">
        <h1>SOC Alert Management</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
          Generate Report
        </button>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <span className="metric-title">Active Alerts</span>
          <span className="metric-value">{metrics.activeAlerts}</span>
        </div>
        <div className="metric-card">
          <span className="metric-title" style={{ color: '#ef4444' }}>Critical Alerts</span>
          <span className="metric-value" style={{ color: '#ef4444' }}>{metrics.criticalAlerts}</span>
        </div>
        <div className="metric-card">
          <span className="metric-title">MTTA</span>
          <span className="metric-value">{metrics.mtta}</span>
        </div>
        <div className="metric-card">
          <span className="metric-title">MTTR</span>
          <span className="metric-value">{metrics.mttr}</span>
        </div>
      </div>

      <div className="alert-queue-section mt-8">
        <AlertQueue />
      </div>
    </div>
  );
}
