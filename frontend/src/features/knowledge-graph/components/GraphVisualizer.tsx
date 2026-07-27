import React, { useRef, useEffect } from 'react';
import './KnowledgeGraphStyles.css';

export const GraphVisualizer: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    // A simplified visual mock of a node-link diagram on a canvas to represent Graph Visualization
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set dimensions
    canvas.width = canvas.parentElement?.clientWidth || 800;
    canvas.height = 500;

    // Draw background
    ctx.fillStyle = 'rgba(15, 23, 42, 0.5)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Nodes
    const nodes = [
      { id: 1, x: 200, y: 250, label: 'APT29', type: 'THREAT_ACTOR' },
      { id: 2, x: 400, y: 150, label: 'SUNBURST', type: 'MALWARE_FAMILY' },
      { id: 3, x: 400, y: 350, label: 'TEARDROP', type: 'MALWARE_FAMILY' },
      { id: 4, x: 600, y: 250, label: '192.168.1.5', type: 'IPV4' },
      { id: 5, x: 200, y: 100, label: 'Campaign Solar', type: 'CAMPAIGN' }
    ];

    // Edges
    const edges = [
      { source: 0, target: 1, label: 'USES', inferred: false },
      { source: 0, target: 2, label: 'USES', inferred: false },
      { source: 1, target: 3, label: 'COMMUNICATES_WITH', inferred: true },
      { source: 2, target: 3, label: 'COMMUNICATES_WITH', inferred: false },
      { source: 4, target: 0, label: 'ASSOCIATED_WITH', inferred: true }
    ];

    // Draw Edges
    edges.forEach(edge => {
      const source = nodes[edge.source];
      const target = nodes[edge.target];
      
      ctx.beginPath();
      ctx.moveTo(source.x, source.y);
      ctx.lineTo(target.x, target.y);
      ctx.strokeStyle = edge.inferred ? 'rgba(167, 139, 250, 0.8)' : 'rgba(148, 163, 184, 0.5)'; // Accent color for inferred
      if (edge.inferred) ctx.setLineDash([5, 5]);
      else ctx.setLineDash([]);
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    // Draw Nodes
    nodes.forEach(node => {
      ctx.beginPath();
      ctx.arc(node.x, node.y, 25, 0, 2 * Math.PI);
      ctx.fillStyle = node.type === 'THREAT_ACTOR' ? '#ef4444' : 
                      node.type === 'MALWARE_FAMILY' ? '#f59e0b' : '#3b82f6';
      ctx.fill();
      ctx.strokeStyle = 'white';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.fillStyle = 'white';
      ctx.font = '12px Inter';
      ctx.textAlign = 'center';
      ctx.fillText(node.label, node.x, node.y + 40);
    });
  }, []);

  return (
    <div className="kg-container">
      <header className="kg-header flex-between">
        <div>
          <h2>Graph Explorer</h2>
          <p className="kg-subtitle">Interactive visualization of threat relationships</p>
        </div>
        <div className="kg-filters flex gap-2">
          <button className="kg-btn-secondary">Filter: Inferred Only</button>
          <button className="kg-btn-primary">Expand Neighbors</button>
        </div>
      </header>
      
      <div className="kg-canvas-container glassmorphism">
        <canvas ref={canvasRef} className="kg-canvas"></canvas>
        <div className="kg-legend mt-4 flex gap-4 text-sm text-gray-300">
          <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-red-500 inline-block"></span> Threat Actor</div>
          <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-yellow-500 inline-block"></span> Malware</div>
          <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-blue-500 inline-block"></span> Infrastructure</div>
          <div className="flex items-center gap-2 ml-4">-- Inferred Edge</div>
        </div>
      </div>
    </div>
  );
};
