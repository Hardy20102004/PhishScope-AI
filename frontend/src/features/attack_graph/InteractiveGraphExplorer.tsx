import React, { useState, useEffect, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

export const InteractiveGraphExplorer: React.FC<{ seedId?: string }> = ({ seedId = 'apt29' }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [graphData, setGraphData] = useState<any>({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const response = await fetch(`/api/v1/attack-graph/build?seed_id=${seedId}&depth=3`);
        if (response.ok) {
          const data = await response.json();
          // Map backend types to colors for the UI
          const coloredNodes = data.nodes.map((n: any) => {
            let color = '#9CA3AF'; // Gray default
            if (n.type === 'Threat Actor') color = '#EF4444'; // Red
            if (n.type === 'Campaign') color = '#10B981'; // Green
            if (n.type === 'Infrastructure') color = '#3B82F6'; // Blue
            if (n.type === 'Victim') color = '#F59E0B'; // Yellow
            return { ...n, color };
          });
          setGraphData({ nodes: coloredNodes, links: data.links });
        }
      } catch (error) {
        console.error('Failed to load attack graph', error);
      } finally {
        setLoading(false);
      }
    };
    fetchGraph();
  }, [seedId]);

  if (loading) return <div className="h-[600px] flex items-center justify-center bg-gray-900 border border-gray-700 rounded-xl text-gray-400">Rendering Subgraph...</div>;

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg h-[600px] flex flex-col relative" ref={containerRef}>
      {/* Top Overlay Controls */}
      <div className="absolute top-4 left-4 z-10 pointer-events-none w-full pr-8">
        <div className="flex justify-between items-start pointer-events-auto">
          <div>
            <h3 className="text-xl font-semibold text-white flex items-center bg-gray-900/80 px-3 py-1.5 rounded border border-gray-700 shadow">
              <svg className="w-5 h-5 mr-2 text-fuchsia-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
              </svg>
              Enterprise Attack Graph
            </h3>
            <div className="mt-2 flex space-x-2">
              <span className="bg-gray-800 border border-gray-700 text-gray-300 text-xs px-2 py-1 rounded shadow">Seed: {seedId}</span>
              <span className="bg-gray-800 border border-gray-700 text-gray-300 text-xs px-2 py-1 rounded shadow">Nodes: {graphData.nodes.length}</span>
            </div>
          </div>

          <div className="bg-gray-800 p-3 rounded-lg border border-gray-700 shadow-lg text-sm">
            <h4 className="font-semibold text-gray-200 mb-2 border-b border-gray-700 pb-1">Legend</h4>
            <div className="space-y-1.5">
              <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-red-500 mr-2 shadow"></span> Threat Actor</div>
              <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-green-500 mr-2 shadow"></span> Campaign</div>
              <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-blue-500 mr-2 shadow"></span> Infrastructure</div>
              <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-yellow-500 mr-2 shadow"></span> Victim</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* 2D Force Graph */}
      <div className="flex-grow w-full rounded-xl overflow-hidden cursor-crosshair">
        <ForceGraph2D
          graphData={graphData}
          width={containerRef.current?.clientWidth || 1000}
          height={600}
          backgroundColor="#111827"
          nodeColor="color"
          nodeLabel="label"
          nodeRelSize={6}
          linkColor={() => '#4B5563'} // gray-600
          linkWidth={1.5}
          linkDirectionalArrowLength={3.5}
          linkDirectionalArrowRelPos={1}
          linkDirectionalParticles={2}
          linkDirectionalParticleSpeed={0.005}
          onNodeClick={(node) => {
            // In a full implementation, this would trigger the NodeInspector.tsx overlay
            console.log("Clicked Node:", node);
          }}
        />
      </div>
    </div>
  );
};
