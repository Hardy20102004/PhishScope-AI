import React from 'react';
import './KnowledgeGraphStyles.css';

export const TimelineViewer: React.FC = () => {
  return (
    <div className="kg-container">
      <header className="kg-header">
        <h2>Unified Graph Timeline</h2>
        <p className="kg-subtitle">Chronological evolution of Campaigns and IOCs</p>
      </header>

      <div className="kg-timeline glassmorphism">
        <div className="timeline-event">
          <div className="timeline-date">July 26, 2026 (08:30 AM)</div>
          <div className="timeline-content">
            <h4>Inference Engine Detection</h4>
            <p>Graph identified overlapping infrastructure between Campaign Alpha and APT29.</p>
            <span className="kg-badge kg-badge-accent mt-2 block w-max">Inferred Relationship Created</span>
          </div>
        </div>

        <div className="timeline-event">
          <div className="timeline-date">July 25, 2026 (14:15 PM)</div>
          <div className="timeline-content">
            <h4>IOC Correlation</h4>
            <p>Domain malicious-site.com resolved to 192.168.1.5. Graph updated with TARGETS edge.</p>
          </div>
        </div>

        <div className="timeline-event">
          <div className="timeline-date">July 20, 2026 (09:00 AM)</div>
          <div className="timeline-content">
            <h4>Campaign Creation</h4>
            <p>Campaign Alpha was created by SOC Team based on phishing reports.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
