import React from 'react';
import './PredictiveStyles.css';

export const TrendDashboard: React.FC = () => {
  return (
    <div className="pred-container">
      <header className="pred-header">
        <h2>Macro Trend Analysis</h2>
        <p className="pred-subtitle">Aggregated shifts in adversary behavior across the enterprise</p>
      </header>

      <div className="pred-content-grid">
        <div className="pred-panel glassmorphism">
          <h3>Industry Targeting Shifts</h3>
          <table className="pred-table mt-4 w-full">
            <thead>
              <tr>
                <th>Industry</th>
                <th>Trend</th>
                <th>Change</th>
                <th>Primary Actor</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Healthcare</td>
                <td><span className="text-red-500">↑ Rising</span></td>
                <td>+45%</td>
                <td>FIN7</td>
              </tr>
              <tr>
                <td>Finance</td>
                <td><span className="text-yellow-500">→ Stable</span></td>
                <td>+2%</td>
                <td>Lazarus Group</td>
              </tr>
              <tr>
                <td>Energy</td>
                <td><span className="text-green-500">↓ Falling</span></td>
                <td>-15%</td>
                <td>APT33</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="pred-panel glassmorphism">
          <h3>Malware Volume Projection</h3>
          {/* Mock representation of a chart area */}
          <div className="h-48 mt-4 bg-gradient-to-t from-red-500/20 to-transparent border-b border-red-500/50 flex items-end px-4 gap-2">
             <div className="w-1/6 bg-red-500/30 h-1/4"></div>
             <div className="w-1/6 bg-red-500/40 h-2/4"></div>
             <div className="w-1/6 bg-red-500/50 h-[55%]"></div>
             <div className="w-1/6 bg-red-500/60 h-3/4"></div>
             <div className="w-1/6 bg-red-500/80 h-[90%]"></div>
             <div className="w-1/6 bg-red-500 h-full relative">
                <span className="absolute -top-6 left-0 right-0 text-center text-xs text-red-400 font-bold">Ransomware Spike Projected</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};
