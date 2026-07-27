import React from 'react';
import './TimelineStyles.css';

export const TimelineExplorer: React.FC = () => {
  return (
    <div className="tl-container flex h-screen overflow-hidden">
      
      {/* Main Timeline Canvas */}
      <div className="flex-1 flex flex-col pr-4">
        <header className="tl-header">
          <h2>Timeline Explorer: APT29 Infrastructure Shift</h2>
          <div className="flex gap-2 mt-2">
            <button className="tl-btn-secondary">Zoom In</button>
            <button className="tl-btn-secondary">Zoom Out</button>
            <button className="tl-btn-secondary">Filter by Confidence</button>
          </div>
        </header>

        <div className="tl-canvas-area glassmorphism flex-1 overflow-y-auto p-8 relative">
          {/* Vertical Line */}
          <div className="absolute left-1/2 top-0 bottom-0 w-1 bg-indigo-500/30 -translate-x-1/2"></div>
          
          <div className="tl-event-node left-side">
            <div className="tl-event-card">
              <span className="tl-date-badge">2026-07-20 14:00 UTC</span>
              <h4>Domain Registered</h4>
              <p>malicious-c2.com was registered via Namecheap.</p>
              <div className="mt-2 text-xs text-gray-400">Category: OBSERVATION • Confidence: 1.0</div>
            </div>
          </div>

          <div className="tl-event-node right-side">
            <div className="tl-event-card border-accent border-dashed">
              <span className="tl-date-badge">2026-07-21 09:00 UTC</span>
              <h4>[Hypothetical] DNS Propagation</h4>
              <p>AI Engine infers propagation occurred before active C2 communication.</p>
              <div className="mt-2 text-xs text-indigo-300">Category: INFERENCE • Confidence: 0.65</div>
            </div>
          </div>

          <div className="tl-event-node left-side">
            <div className="tl-event-card">
              <span className="tl-date-badge">2026-07-22 18:30 UTC</span>
              <h4>Malware Communicates with C2</h4>
              <p>TEARDROP malware beaconed to malicious-c2.com.</p>
              <div className="mt-2 text-xs text-gray-400">Category: COMMUNICATION • Confidence: 1.0</div>
            </div>
          </div>
        </div>
      </div>

      {/* Drill Down Panel */}
      <div className="w-96 glassmorphism p-6 flex flex-col overflow-y-auto border-l border-white/10">
        <h3>Event Details</h3>
        
        <div className="mt-6">
          <h4 className="text-xl text-white">Malware Communicates with C2</h4>
          <span className="text-sm text-gray-400 mt-1 block">July 22, 2026 18:30:00 UTC</span>
        </div>

        <div className="mt-6">
          <h5 className="text-gray-300 mb-2 uppercase tracking-wider text-xs">Evidence (2)</h5>
          <div className="bg-black/30 p-3 rounded mb-2">
            <strong>Network PCAP</strong>
            <p className="text-sm text-gray-400 mt-1 truncate">s3://evidence/pcap_8892.pcap</p>
          </div>
          <div className="bg-black/30 p-3 rounded">
            <strong>Suricata Alert</strong>
            <p className="text-sm text-gray-400 mt-1">ET MALWARE TEARDROP Beacon</p>
          </div>
        </div>

        <div className="mt-6 border-t border-white/10 pt-4">
          <button className="tl-btn-primary w-full">View in Knowledge Graph</button>
        </div>
      </div>
      
    </div>
  );
};
