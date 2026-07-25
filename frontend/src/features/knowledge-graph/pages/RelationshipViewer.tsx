import React, { useRef, useEffect, useState, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Card } from '@/components/ui/Card';
import { Network, Search, Zap } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const RelationshipViewer: React.FC = () => {
  const fgRef = useRef<any>(null);
  const [graphData, setGraphData] = useState<{nodes: any[], links: any[]}>({ nodes: [], links: [] });
  const [loading, setLoading] = useState(false);
  const [searchId, setSearchId] = useState('');

  // We mock a highly connected subgraph if the DB is empty just to show off the visualizer
  const loadMockGraph = () => {
    const nodes = [
      { id: 'actor_1', name: 'APT-29', group: 'THREAT_ACTOR', val: 5 },
      { id: 'camp_1', name: 'Operation Ghost', group: 'CAMPAIGN', val: 3 },
      { id: 'dom_1', name: 'secure-login.xyz', group: 'DOMAIN', val: 2 },
      { id: 'dom_2', name: 'auth-update.net', group: 'DOMAIN', val: 2 },
      { id: 'ip_1', name: '192.168.1.100', group: 'IP_ADDRESS', val: 1 },
    ];
    const links = [
      { source: 'actor_1', target: 'camp_1', name: 'ATTRIBUTED_TO' },
      { source: 'camp_1', target: 'dom_1', name: 'USES' },
      { source: 'camp_1', target: 'dom_2', name: 'USES' },
      { source: 'dom_1', target: 'ip_1', name: 'RESOLVES_TO' },
      { source: 'dom_2', target: 'ip_1', name: 'RESOLVES_TO' }, // Shared infra inference!
    ];
    setGraphData({ nodes: nodes as any, links: links as any });
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchId) return;
    
    setLoading(true);
    try {
      const res = await api.get(`/knowledge-graph/traverse/${searchId}?depth=2`);
      const nodes = res.data.entities.map((e: any) => ({
        id: e.id,
        name: e.name,
        group: e.entity_type,
        val: 2
      }));
      const links = res.data.relationships.map((r: any) => ({
        source: r.source_id,
        target: r.target_id,
        name: r.relationship_type
      }));
      
      if (nodes.length > 0) {
        setGraphData({ nodes, links });
      } else {
        // Fallback to mock if DB is empty
        loadMockGraph();
      }
    } catch (err) {
      console.error(err);
      loadMockGraph();
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    loadMockGraph(); // Initial load
  }, []);

  const handleNodeClick = useCallback((node: any) => {
    // Re-center on node
    if (fgRef.current) {
      fgRef.current.centerAt(node.x, node.y, 1000);
      fgRef.current.zoom(8, 2000);
    }
  }, [fgRef]);

  // Color mapping
  const getColor = (group: string) => {
    const colors: Record<string, string> = {
      'THREAT_ACTOR': '#ef4444', // Red
      'CAMPAIGN': '#f97316', // Orange
      'DOMAIN': '#3b82f6', // Blue
      'IP_ADDRESS': '#8b5cf6', // Purple
      'DEFAULT': '#6b7280'
    };
    return colors[group] || colors['DEFAULT'];
  };

  return (
    <div className="flex-1 flex flex-col bg-[#0a0a0b] text-gray-100 min-h-screen relative">
      <div className="absolute top-8 left-8 z-10 w-96">
        <Card className="bg-gray-900/90 border-gray-800 backdrop-blur-md shadow-2xl">
          <div className="p-4 border-b border-gray-800">
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              <Network className="w-5 h-5 text-purple-500" />
              Relationship Viewer
            </h1>
          </div>
          <div className="p-4">
            <form onSubmit={handleSearch} className="relative mb-4">
              <input
                type="text"
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                placeholder="Enter Entity ID..."
                className="w-full bg-black border border-gray-700 rounded text-sm pl-8 pr-2 py-2 focus:outline-none focus:border-purple-500"
              />
              <Search className="w-4 h-4 absolute left-2.5 top-2.5 text-gray-500" />
            </form>
            
            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2 text-xs text-gray-400"><div className="w-3 h-3 rounded-full bg-red-500"></div> Threat Actor</div>
              <div className="flex items-center gap-2 text-xs text-gray-400"><div className="w-3 h-3 rounded-full bg-orange-500"></div> Campaign</div>
              <div className="flex items-center gap-2 text-xs text-gray-400"><div className="w-3 h-3 rounded-full bg-blue-500"></div> Domain</div>
              <div className="flex items-center gap-2 text-xs text-gray-400"><div className="w-3 h-3 rounded-full bg-purple-500"></div> IP Address</div>
            </div>
            
            <button 
              className="w-full bg-purple-900/40 hover:bg-purple-900/60 border border-purple-900/50 text-purple-400 py-1.5 rounded flex justify-center items-center gap-2 text-sm transition-colors"
              onClick={() => {}}
              disabled={loading}
            >
              <Zap className="w-4 h-4" /> {loading ? 'Loading...' : 'Run Inference'}
            </button>
          </div>
        </Card>
      </div>
      
      <div className="flex-1 w-full h-full cursor-grab active:cursor-grabbing">
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          nodeLabel="name"
          nodeColor={(node: any) => getColor(node.group)}
          linkColor={() => 'rgba(255,255,255,0.2)'}
          linkDirectionalArrowLength={3.5}
          linkDirectionalArrowRelPos={1}
          linkCurvature={0.25}
          linkLabel="name"
          onNodeClick={handleNodeClick}
          backgroundColor="#0a0a0b"
          // @ts-ignore
          nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.name;
            const fontSize = 12/globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

            ctx.fillStyle = 'rgba(10, 10, 11, 0.8)';
            ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = getColor(node.group);
            ctx.fillText(label, node.x, node.y);
            node.__bckgDimensions = bckgDimensions;
          }}
          nodePointerAreaPaint={(node, color, ctx) => {
            ctx.fillStyle = color;
            const bckgDimensions = node.__bckgDimensions;
            bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);
          }}
        />
      </div>
    </div>
  );
};
