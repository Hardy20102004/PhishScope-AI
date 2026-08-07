import React, { useState, useEffect } from 'react';
import './KnowledgeGraphStyles.css';

export const ThreatGraphDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState({
    totalNodes: 0,
    totalEdges: 0,
    inferredEdges: 0,
    activeClusters: 0
  });

  useEffect(() => {
    // Mock fetch
    setTimeout(() => {
      setMetrics({
        totalNodes: 15420,
        totalEdges: 89304,
        inferredEdges: 1250,
        activeClusters: 8
      });
    }, 1000);
  }, []);

  return (
    <div className="kg-container">
      <header className="kg-header">
        <h1>Enterprise IOC Knowledge Graph</h1>
        <p className="kg-subtitle">Central Reasoning Layer & AI Graph Analysis</p>
      </header>

      <div className="kg-metrics-grid">
        <div className="kg-metric-card glassmorphism hover-lift">
          <div className="kg-metric-icon">🟢</div>
          <div className="kg-metric-content">
            <h3>Entities</h3>
            <div className="kg-metric-value">{metrics.totalNodes.toLocaleString()}</div>
          </div>
        </div>

        <div className="kg-metric-card glassmorphism hover-lift">
          <div className="kg-metric-icon">🔗</div>
          <div className="kg-metric-content">
            <h3>Relationships</h3>
            <div className="kg-metric-value">{metrics.totalEdges.toLocaleString()}</div>
          </div>
        </div>

        <div className="kg-metric-card glassmorphism hover-lift">
          <div className="kg-metric-icon">🧠</div>
          <div className="kg-metric-content">
            <h3>AI Inferred Links</h3>
            <div className="kg-metric-value text-accent">{metrics.inferredEdges.toLocaleString()}</div>
          </div>
        </div>

        <div className="kg-metric-card glassmorphism hover-lift">
          <div className="kg-metric-icon">🕸️</div>
          <div className="kg-metric-content">
            <h3>Threat Clusters</h3>
            <div className="kg-metric-value">{metrics.activeClusters}</div>
          </div>
        </div>
      </div>

      <div className="kg-content-grid">
        <div className="kg-panel glassmorphism">
          <div className="flex-between">
            <h2>Recent Inference Engine Deductions</h2>
            <button className="kg-btn-secondary">Run Inference</button>
          </div>
          <ul className="kg-activity-list mt-4">
            <li>
              <span className="kg-activity-time">Just now</span>
              <span className="kg-activity-desc">Linked <strong>APT29</strong> and <strong>CozyBear</strong> (Shared Malware: SUNBURST)</span>
              <span className="kg-badge kg-badge-accent">Inferred</span>
            </li>
            <li>
              <span className="kg-activity-time">5m ago</span>
              <span className="kg-activity-desc">Clustered 15 domains under <strong>Shared Infrastructure C2</strong></span>
              <span className="kg-badge kg-badge-accent">Inferred</span>
            </li>
          </ul>
        </div>

        <div className="kg-panel glassmorphism">
          <h2>Top Graph Queries</h2>
          <div className="kg-query-preview">
            <div className="kg-query-item">
              <h4>Shortest Path: [IP X] to [Threat Actor Y]</h4>
              <p>Found path length: 3 hops</p>
            </div>
            <div className="kg-query-item">
              <h4>Neighborhood: [Campaign Alpha]</h4>
              <p>Expanded to depth 2 (45 nodes)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
