import React, { useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

export const ClusterGraph: React.FC<{ campaignId: string }> = ({ campaignId: _campaignId }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Mock Graph Data demonstrating a discovered cluster
  const graphData = {
    nodes: [
      { id: 'c1', label: 'Operation Ghost Hunt', type: 'Campaign', color: '#10B981', val: 20 },
      { id: 'd1', label: 'login-secure-portal.com', type: 'Domain', color: '#3B82F6', val: 10 },
      { id: 'd2', label: 'auth-gateway-update.net', type: 'Domain', color: '#3B82F6', val: 10 },
      { id: 'd3', label: 'verify-account-info.org', type: 'Domain', color: '#3B82F6', val: 10 },
      { id: 'ip1', label: '198.51.100.45', type: 'IP', color: '#F59E0B', val: 15 },
      { id: 'cert1', label: 'Let\'s Encrypt (SNI)', type: 'Certificate', color: '#A855F7', val: 12 },
    ],
    links: [
      { source: 'c1', target: 'd1', label: 'Infrastructure', strength: 0.9 },
      { source: 'c1', target: 'd2', label: 'Infrastructure', strength: 0.9 },
      { source: 'c1', target: 'd3', label: 'Infrastructure', strength: 0.9 },
      { source: 'd1', target: 'ip1', label: 'Resolves To', strength: 1.0 },
      { source: 'd2', target: 'ip1', label: 'Resolves To', strength: 1.0 },
      { source: 'd3', target: 'ip1', label: 'Resolves To', strength: 1.0 },
      { source: 'ip1', target: 'cert1', label: 'Hosts', strength: 0.8 },
    ]
  };

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-6 h-[450px] flex flex-col relative" ref={containerRef}>
      <div className="absolute top-6 left-6 z-10 pointer-events-none">
        <h3 className="text-lg font-semibold text-white flex items-center bg-gray-900/80 px-2 py-1 rounded">
          <svg className="w-5 h-5 mr-2 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Discovery Cluster Subgraph
        </h3>
        
        <div className="mt-4 bg-gray-800/80 p-3 rounded border border-gray-700 pointer-events-auto">
           <h4 className="text-sm font-medium text-gray-300 mb-2">Legend</h4>
           <div className="space-y-1 text-xs">
             <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-emerald-500 mr-2"></span> Campaign Cluster</div>
             <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-blue-500 mr-2"></span> Domain</div>
             <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-yellow-500 mr-2"></span> IP Address</div>
             <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-purple-500 mr-2"></span> Certificate</div>
           </div>
        </div>
      </div>
      
      <div className="flex-grow w-full rounded overflow-hidden">
        <ForceGraph2D
          graphData={graphData}
          width={containerRef.current?.clientWidth || 600}
          height={380}
          backgroundColor="#111827"
          nodeColor="color"
          nodeLabel="label"
          nodeVal="val"
          nodeRelSize={4}
          linkColor={() => '#6B7280'}
          linkWidth={1.5}
          linkDirectionalArrowLength={3}
          linkDirectionalArrowRelPos={1}
        />
      </div>
    </div>
  );
};
