import React, { useState, useEffect, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

// Note: To run this in a real project, you would need to run:
// npm install react-force-graph-2d

interface Node {
  id: string;
  name: string;
  group: number;
  val: number;
  type: string;
}

interface Link {
  source: string;
  target: string;
  label: string;
  confidence: number;
}

interface GraphData {
  nodes: Node[];
  links: Link[];
}

interface CorrelationViewerProps {
  iocId?: string; // Optional: Center graph on a specific IOC
}

export const CorrelationViewer: React.FC<CorrelationViewerProps> = ({ iocId }) => {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const fgRef = useRef<any>(null);

  useEffect(() => {
    // Simulate fetching relationship data from the API
    // In reality: GET /api/v1/ioc/${iocId}/relationships or a full graph query
    const loadMockData = () => {
      const mockData: GraphData = {
        nodes: [
          { id: '1', name: 'evil-phishing.com', group: 1, val: 5, type: 'Domain' },
          { id: '2', name: '192.168.1.100', group: 2, val: 3, type: 'IPv4' },
          { id: '3', name: 'malicious_payload.exe', group: 3, val: 4, type: 'File Name' },
          { id: '4', name: 'attacker@protonmail.com', group: 4, val: 2, type: 'Email Address' },
          { id: '5', name: 'login-update.evil-phishing.com', group: 1, val: 2, type: 'Subdomain' }
        ],
        links: [
          { source: '1', target: '2', label: 'RESOLVES_TO', confidence: 1.0 },
          { source: '3', target: '2', label: 'DOWNLOADED_FROM', confidence: 0.8 },
          { source: '4', target: '1', label: 'REGISTERED_DOMAIN', confidence: 0.9 },
          { source: '5', target: '1', label: 'PART_OF', confidence: 1.0 }
        ]
      };
      
      setGraphData(mockData);
      setLoading(false);
    };

    // Small delay to simulate network
    setTimeout(loadMockData, 500);
  }, [iocId]);

  const getNodeColor = (type: string) => {
    switch(type) {
      case 'Domain': return '#3b82f6'; // Blue
      case 'Subdomain': return '#60a5fa'; // Lighter blue
      case 'IPv4': return '#10b981'; // Green
      case 'File Name': return '#ef4444'; // Red
      case 'Email Address': return '#a855f7'; // Purple
      default: return '#9ca3af'; // Gray
    }
  };

  if (loading) {
    return <div className="h-96 w-full flex items-center justify-center bg-gray-900 border border-gray-700 rounded-xl text-gray-400">Loading Knowledge Graph...</div>;
  }

  return (
    <div className="flex flex-col bg-gray-900 rounded-xl border border-gray-700 overflow-hidden shadow-lg h-[600px]">
      <div className="p-4 bg-gray-800 border-b border-gray-700 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white">Relationship Graph Explorer</h3>
        <div className="flex space-x-2 text-xs">
           <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-blue-500 mr-1"></span> Domains</span>
           <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-green-500 mr-1"></span> IP Addresses</span>
           <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-red-500 mr-1"></span> Files</span>
           <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-purple-500 mr-1"></span> Emails</span>
        </div>
      </div>
      
      <div className="flex-grow relative w-full h-full bg-gray-950">
        {/* We use a conditional render here because react-force-graph can be tricky in some SSR/test environments */}
        {typeof window !== 'undefined' && (
          <ForceGraph2D
            ref={fgRef}
            graphData={graphData}
            nodeLabel="name"
            nodeColor={(node: any) => getNodeColor(node.type)}
            nodeRelSize={6}
            linkColor={() => 'rgba(156, 163, 175, 0.4)'}
            linkWidth={(link: any) => Math.max(1, (link.confidence || 0.5) * 3)}
            linkDirectionalArrowLength={3.5}
            linkDirectionalArrowRelPos={1}
            onNodeClick={(node: any) => {
              // Center/zoom on node
              if (fgRef.current) {
                fgRef.current.centerAt(node.x, node.y, 1000);
                fgRef.current.zoom(8, 2000);
              }
            }}
            // Link label on hover
            linkLabel={(link: any) => `<div class="bg-gray-800 text-xs text-white p-1 rounded border border-gray-600">${link.label} (${(link.confidence * 100).toFixed(0)}%)</div>`}
          />
        )}
      </div>
      
      <div className="p-3 bg-gray-800 border-t border-gray-700 text-xs text-gray-400 flex justify-between">
        <span>Zoom: Scroll | Pan: Drag | Node Info: Hover/Click</span>
        <span>Nodes: {graphData.nodes.length} | Edges: {graphData.links.length}</span>
      </div>
    </div>
  );
};
