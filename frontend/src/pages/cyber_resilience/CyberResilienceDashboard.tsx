import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Shield, Target, Activity, Zap, TrendingUp, AlertTriangle } from 'lucide-react';

export default function CyberResilienceDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-emerald-400">
            <Shield size={32} />
            Enterprise Cyber Resilience
          </h1>
          <p className="text-slate-400 mt-2">Executive abstraction of technical security validation, SOC operations, and control effectiveness.</p>
        </div>
        <Button className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-500/20 gap-2">
            <Target size={18} /> Generate Board Report
        </Button>
      </div>

      {/* Main Score Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <Card className="bg-slate-900 border-emerald-900/50 lg:col-span-1 flex flex-col items-center justify-center py-12 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4">
                  <div className="flex items-center gap-1 text-emerald-400 font-bold text-sm bg-emerald-950/50 px-2 py-1 rounded">
                      <TrendingUp size={14} /> +2.4% (Q3)
                  </div>
              </div>
              <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Apex Resilience Score</h3>
              
              <div className="relative flex items-center justify-center mb-4">
                  {/* Outer glowing ring */}
                  <div className="absolute inset-0 rounded-full border-4 border-emerald-500/20 animate-pulse w-48 h-48 -m-4"></div>
                  {/* Inner track */}
                  <svg className="w-40 h-40 transform -rotate-90">
                      <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-slate-800" />
                      <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="8" fill="transparent" strokeDasharray="440" strokeDashoffset="44" className="text-emerald-400" />
                  </svg>
                  <div className="absolute flex flex-col items-center">
                      <span className="text-5xl font-black text-slate-100">82<span className="text-2xl text-emerald-500">/100</span></span>
                  </div>
              </div>
              
              <div className="text-emerald-400 font-bold tracking-widest uppercase text-sm">Resilient Status: Strong</div>
          </Card>

          {/* Sub-Pillars */}
          <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-4">
              <PillarCard title="Preventive Controls" score={88} icon={<Shield className="text-cyan-400"/>} trend="+1.2%" />
              <PillarCard title="Detective Controls" score={75} icon={<Activity className="text-amber-400"/>} trend="-0.5%" warning={true} />
              <PillarCard title="Response Readiness" score={82} icon={<Zap className="text-rose-400"/>} trend="+3.1%" />
          </div>

      </div>

    </div>
  );
}

function PillarCard({ title, score, icon, trend, warning = false }: any) {
    let scoreColor = "text-emerald-400";
    if (score < 80) scoreColor = "text-amber-400";
    if (score < 60) scoreColor = "text-rose-400";

    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6 h-full flex flex-col justify-between">
                <div className="flex justify-between items-start mb-4">
                    <div className="p-2 bg-slate-950 rounded border border-slate-800">
                        {icon}
                    </div>
                    {warning && (
                        <div className="flex items-center gap-1 text-amber-500 text-[10px] font-bold bg-amber-500/10 px-2 py-1 rounded">
                            <AlertTriangle size={12} /> NEEDS ATTN
                        </div>
                    )}
                </div>
                
                <div>
                    <h3 className="text-sm font-bold text-slate-400 mb-1">{title}</h3>
                    <div className="flex items-end justify-between">
                        <div className={`text-4xl font-black ${scoreColor}`}>{score}</div>
                        <div className={`text-xs font-bold ${trend.startsWith('+') ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {trend}
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
