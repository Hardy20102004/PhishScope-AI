import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Clock, PlayCircle, Layers, Link } from 'lucide-react';

export default function UnifiedTimelineDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-fuchsia-400">
            <Clock size={32} />
            Unified Forensic Timeline
          </h1>
          <p className="text-slate-400 mt-2">Correlates events across Disk, Memory, Cloud, and Email into a single chronological view.</p>
        </div>
        <Button className="bg-fuchsia-600 hover:bg-fuchsia-700 text-white shadow-lg shadow-fuchsia-500/20 gap-2">
            <PlayCircle size={18} /> Generate Attack Replay
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <StatCard title="Total Correlated Events" value={42} icon={<Layers className="text-fuchsia-400" />} />
          <StatCard title="Modules Involved" value={4} subtitle="EMAIL, DISK, MEMORY, CLOUD" icon={<Layers className="text-slate-400" />} />
          <StatCard title="Explicit Correlations" value={12} subtitle="Shared IP, Hashes" icon={<Link className="text-sky-400" />} />
          <StatCard title="Causal Chains" value={3} subtitle="Spawned, Executed" icon={<Link className="text-amber-400" />} />
      </div>
    </div>
  );
}

function StatCard({ title, value, subtitle, icon }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-2">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">{title}</h3>
                    {icon}
                </div>
                <div className="text-3xl font-black text-slate-200 mb-1">{value}</div>
                {subtitle && <div className="text-xs text-slate-500 font-mono">{subtitle}</div>}
            </CardContent>
        </Card>
    );
}
