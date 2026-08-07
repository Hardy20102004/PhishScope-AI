import React, { useRef, useState, useEffect } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

export const AttributionGraph: React.FC<{ actorId: string }> = ({ actorId: _actorId }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(800);

  useEffect(() => {
    if (!containerRef.current) return;
    const ro = new ResizeObserver(entries => {
      setWidth(entries[0].contentRect.width);
    });
    ro.observe(containerRef.current);
    return () => ro.disconnect();
  }, []);
  
  // Mock Graph Data demonstrating observed facts vs inferences
  const graphData = {
    nodes: [
      { id: 'actor', label: 'APT29', type: 'Threat Actor', color: '#EF4444' }, // Red
      { id: 'c2_ip', label: '192.168.1.100', type: 'IPv4', color: '#3B82F6' }, // Blue
      { id: 'malware', label: 'CozyCar', type: 'Malware', color: '#A855F7' }, // Purple
      { id: 'campaign', label: 'Op Ghost', type: 'Campaign', color: '#10B981' }, // Green
      { id: 'victim', label: 'Gov Agency A', type: 'Victim', color: '#F59E0B' } // Yellow
    ],
    links: [
      { source: 'actor', target: 'c2_ip', label: 'Infrastructure (Observed)', confidence: 1.0, isFact: true },
      { source: 'c2_ip', target: 'malware', label: 'Hosted (Observed)', confidence: 1.0, isFact: true },
      { source: 'actor', target: 'malware', label: 'Uses (Inferred)', confidence: 0.85, isFact: false },
      { source: 'actor', target: 'campaign', label: 'Attributed (Inferred)', confidence: 0.9, isFact: false },
      { source: 'campaign', target: 'victim', label: 'Targeted (Observed)', confidence: 1.0, isFact: true },
    ]
  };

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-6 h-[500px] flex flex-col relative" ref={containerRef}>
      <div className="absolute top-6 left-6 z-10 pointer-events-none">
        <h3 className="text-xl font-semibold text-white flex items-center bg-gray-900/80 px-2 py-1 rounded">
          <svg className="w-5 h-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Attribution Evidence Graph
        </h3>
        
        <div className="mt-4 bg-gray-800/80 p-3 rounded border border-gray-700 pointer-events-auto">
           <h4 className="text-sm font-medium text-gray-300 mb-2">Legend</h4>
           <div className="space-y-1 text-xs">
             <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-red-500 mr-2"></span> Threat Actor</div>
             <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-blue-500 mr-2"></span> Infrastructure (IOC)</div>
             <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-purple-500 mr-2"></span> Malware</div>
             <div className="flex items-center mt-2 pt-2 border-t border-gray-700">
               <span className="w-6 h-0.5 bg-gray-400 mr-2"></span> Observed Fact (Solid)
             </div>
             <div className="flex items-center">
               <span className="w-6 h-0.5 border-t border-dashed border-gray-400 mr-2"></span> Inference (Dashed)
             </div>
           </div>
        </div>
      </div>
      
      <div className="flex-grow w-full rounded overflow-hidden">
        <ForceGraph2D
          graphData={graphData}
          width={width}
          height={400}
          backgroundColor="#111827"
          nodeColor="color"
          nodeLabel="label"
          nodeRelSize={6}
          linkColor={(link: any) => link.isFact ? '#9CA3AF' : '#6B7280'}
          linkLineDash={(link: any) => link.isFact ? null : [4, 4]}
          linkWidth={(link: any) => link.confidence * 2}
          linkDirectionalArrowLength={3.5}
          linkDirectionalArrowRelPos={1}
        />
      </div>
    </div>
  );
};
