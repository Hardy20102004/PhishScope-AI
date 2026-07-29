import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Network, Play, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function InteractiveAttackGraph() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800 flex flex-col">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-2">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Network className="text-fuchsia-400" />
                    Interactive Graph Viewer
                </h2>
                <p className="text-slate-400 mt-1">Visually trace simulated attack paths through the enterprise asset graph.</p>
            </div>
            <div className="flex gap-2">
                <Button variant="outline" className="bg-slate-900 border-slate-700 text-slate-300 gap-2">
                    <Filter size={16} /> Filters
                </Button>
                <Button className="bg-fuchsia-600 hover:bg-fuchsia-700 text-white gap-2">
                    <Play size={16} /> Run Pathfinding
                </Button>
            </div>
        </div>

        {/* Mock Graph Visualization Canvas */}
        <div className="flex-1 min-h-[600px] bg-slate-900 border border-slate-800 rounded-lg relative overflow-hidden flex items-center justify-center">
            
            {/* Background Grid */}
            <div className="absolute inset-0 opacity-5" 
                 style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)', backgroundSize: '40px 40px' }}>
            </div>

            {/* Mock Nodes and Edges */}
            <div className="relative w-full max-w-4xl aspect-video">
                
                {/* Source Node */}
                <div className="absolute left-[10%] top-[40%] flex flex-col items-center z-10">
                    <div className="w-16 h-16 rounded-full border-2 border-rose-500 bg-rose-950/80 flex items-center justify-center shadow-[0_0_15px_rgba(244,63,94,0.5)]">
                        <span className="text-xs font-bold text-rose-400">USER</span>
                    </div>
                    <span className="mt-2 text-xs font-mono text-slate-300">Phished_Dev</span>
                </div>

                {/* Edge 1 */}
                <div className="absolute left-[15%] top-[48%] w-[25%] h-0.5 bg-rose-500/50 -rotate-12 z-0">
                    <span className="absolute -top-4 left-1/2 -translate-x-1/2 text-[10px] text-rose-400 font-bold bg-slate-900 px-1">HAS_SESSION</span>
                </div>

                {/* Intermediate Node */}
                <div className="absolute left-[40%] top-[30%] flex flex-col items-center z-10">
                    <div className="w-16 h-16 rounded border-2 border-amber-500 bg-amber-950/80 flex items-center justify-center">
                        <span className="text-xs font-bold text-amber-400">SERVER</span>
                    </div>
                    <span className="mt-2 text-xs font-mono text-slate-300">JUMP_HOST_01</span>
                </div>

                {/* Edge 2 */}
                <div className="absolute left-[45%] top-[38%] w-[35%] h-0.5 bg-rose-500/50 rotate-12 z-0">
                    <span className="absolute -top-4 left-1/2 -translate-x-1/2 text-[10px] text-rose-400 font-bold bg-slate-900 px-1">CAN_ASSUME_ROLE</span>
                </div>

                {/* Target Node */}
                <div className="absolute right-[10%] top-[50%] flex flex-col items-center z-10">
                    <div className="w-20 h-20 rounded border-2 border-emerald-500 bg-emerald-950/80 flex items-center justify-center shadow-[0_0_20px_rgba(16,185,129,0.3)]">
                        <span className="text-sm font-black text-emerald-400 text-center leading-tight">PROD<br/>DB</span>
                    </div>
                    <span className="mt-2 text-xs font-mono text-emerald-400 border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 rounded">CRITICAL ASSET</span>
                </div>

            </div>

            {/* Path Details Overlay */}
            <div className="absolute bottom-4 right-4 w-80 bg-slate-950/90 border border-slate-800 p-4 rounded backdrop-blur">
                <h4 className="text-sm font-bold text-slate-200 mb-2">Selected Path Analysis</h4>
                <div className="space-y-2 text-xs font-mono">
                    <div className="flex justify-between"><span className="text-slate-500">Complexity:</span><span className="text-amber-400">2 Hops</span></div>
                    <div className="flex justify-between"><span className="text-slate-500">Required Privs:</span><span className="text-rose-400">Low</span></div>
                    <div className="flex justify-between"><span className="text-slate-500">Defensive Coverage:</span><span className="text-emerald-400">Partial</span></div>
                </div>
            </div>
        </div>
    </div>
  );
}
