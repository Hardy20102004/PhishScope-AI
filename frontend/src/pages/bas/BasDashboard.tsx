import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Shield, PlayCircle, Target, Activity } from 'lucide-react';

export default function BasDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-emerald-400">
            <Shield size={32} />
            Breach & Attack Simulation
          </h1>
          <p className="text-slate-400 mt-2">Safely validate enterprise detection engineering and incident response readiness.</p>
        </div>
        <Button className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-500/20 gap-2">
            <PlayCircle size={18} /> Schedule Simulation
        </Button>
      </div>

      {/* Readiness Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="bg-slate-900 border-slate-800 col-span-2">
              <CardContent className="p-8 flex items-center justify-between">
                  <div className="space-y-2">
                      <h2 className="text-xl font-bold text-slate-300">Organizational Readiness Score</h2>
                      <p className="text-sm text-slate-500 max-w-md">Calculated across 42 scenarios executed in the last 30 days. Identifies your ability to detect and block TTPs.</p>
                  </div>
                  <div className="flex items-center gap-4">
                      <div className="text-6xl font-black text-emerald-400">82<span className="text-3xl text-emerald-600">%</span></div>
                      <div className="flex flex-col gap-1 text-xs font-mono">
                          <span className="text-emerald-400">↑ 14% vs Last Quarter</span>
                          <span className="text-rose-400">3 Critical Gaps Identified</span>
                      </div>
                  </div>
              </CardContent>
          </Card>
          
          <StatCard title="Active Simulations" value={2} icon={<Activity className="text-sky-400" />} />
      </div>
    </div>
  );
}

function StatCard({ title, value, icon }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-2">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">{title}</h3>
                    {icon}
                </div>
                <div className="text-3xl font-black text-slate-200 mb-1">{value}</div>
            </CardContent>
        </Card>
    );
}
