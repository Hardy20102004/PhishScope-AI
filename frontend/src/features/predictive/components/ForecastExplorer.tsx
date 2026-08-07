import React from 'react';
import './PredictiveStyles.css';

export const ForecastExplorer: React.FC = () => {
  return (
    <div className="pred-container">
      <header className="pred-header flex-between">
        <div>
          <h2>Forecast Explorer</h2>
          <p className="pred-subtitle">Likely Campaign Resurgence on domain-xyz-123</p>
        </div>
        <div className="flex gap-4">
          <div className="text-right">
            <div className="text-sm text-gray-400">Confidence Score</div>
            <div className="text-xl text-accent font-bold">85%</div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400">Uncertainty Gap</div>
            <div className="text-xl text-yellow-500 font-bold">30%</div>
          </div>
        </div>
      </header>

      <div className="pred-content-grid">
        {/* Scenarios Panel */}
        <div className="pred-panel glassmorphism">
          <h3>Alternative Scenarios</h3>
          <div className="mt-4 flex flex-col gap-4">
            <div className="scenario-card bg-primary-dark border-l-4 border-accent">
              <div className="flex-between">
                <h4>Active Campaign Launch</h4>
                <span className="font-bold text-accent">75% Prob</span>
              </div>
              <p className="text-sm text-gray-300 mt-2">
                The threat actor will launch a new phishing wave using this domain within 14 days.
              </p>
            </div>

            <div className="scenario-card bg-black-20 border-l-4 border-gray-500">
              <div className="flex-between">
                <h4>Infrastructure Staging</h4>
                <span className="font-bold text-gray-400">25% Prob</span>
              </div>
              <p className="text-sm text-gray-300 mt-2">
                The domain is being staged for future use but won't be active immediately.
              </p>
            </div>
          </div>
        </div>

        {/* Evidence Panel */}
        <div className="pred-panel glassmorphism">
          <h3>Supporting Evidence</h3>
          <div className="mt-4 flex flex-col gap-4">
            <div className="evidence-card bg-black-20 p-4 rounded">
              <span className="pred-badge mb-2 inline-block">KNOWLEDGE_GRAPH_NODE</span>
              <h4>Node: domain-xyz-123</h4>
              <p className="text-sm text-gray-400 mt-1">Historically linked to APT29 campaigns in Q1 2025.</p>
              <button className="text-xs text-accent mt-2 hover:underline">View in Graph</button>
            </div>
            
            <div className="evidence-card bg-black-20 p-4 rounded">
              <span className="pred-badge mb-2 inline-block">TIMELINE_EVENT</span>
              <h4>Event: New TLS Cert Issued</h4>
              <p className="text-sm text-gray-400 mt-1">Let's Encrypt certificate generated 24 hours ago.</p>
              <button className="text-xs text-accent mt-2 hover:underline">View in Timeline</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
