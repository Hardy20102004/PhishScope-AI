import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Shield, Target, GitMerge, TrendingUp, AlertTriangle } from 'lucide-react';

export default function SecurityPostureDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-indigo-400">
            <Shield size={32} />
            Enterprise Security Posture
          </h1>
          <p className="text-slate-400 mt-2">Continuous aggregation of BAS, Red Team, and Blue Team operational metrics.</p>
        </div>
        <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/20 gap-2">
            <TrendingUp size={18} /> Generate Executive Report
        </Button>
      </div>

      {/* Apex Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="bg-slate-900 border-indigo-900/50 col-span-2 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-8 opacity-10">
                  <Shield size={160} />
              </div>
              <CardContent className="p-8 flex items-center justify-between relative z-10">
                  <div className="space-y-2">
                      <h2 className="text-xl font-bold text-slate-200">Apex Posture Score</h2>
                      <p className="text-sm text-slate-500 max-w-md">Calculated dynamically based on real-time control validation, detection fidelity, and adversarial resilience.</p>
                  </div>
                  <div className="flex items-center gap-6">
                      <div className="text-7xl font-black text-indigo-400">76<span className="text-3xl text-indigo-700">/100</span></div>
                      <div className="flex flex-col gap-1 text-xs font-mono">
                          <span className="text-emerald-400 flex items-center gap-1"><TrendingUp size={14}/> Stable (+2.1 30d)</span>
                          <span className="text-rose-400 flex items-center gap-1"><AlertTriangle size={14}/> 1 Drift Detected</span>
                      </div>
                  </div>
              </CardContent>
          </Card>
          
          <Card className="bg-slate-900 border-slate-800 flex flex-col justify-center items-center text-center p-6">
             <div className="text-indigo-400 mb-2"><GitMerge size={32} /></div>
             <h3 className="text-sm font-bold text-slate-400 uppercase">Data Sources Synchronized</h3>
             <div className="text-3xl font-black text-slate-200 mt-2">12,402</div>
             <p className="text-[10px] text-slate-500 mt-1">Events correlated in the last 24h</p>
          </Card>
      </div>

      {/* Sub-Components */}
      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4 text-slate-200">Validation Vectors</h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <VectorCard 
                title="BAS Control Effectiveness" 
                score={82} 
                source="Automated Simulations"
                color="text-emerald-400"
            />
            <VectorCard 
                title="Blue Team Readiness" 
                score={71} 
                source="Detection Health & MTTx"
                color="text-sky-400"
            />
            <VectorCard 
                title="Red Team Resilience" 
                score={68} 
                source="Manual Execution Campaigns"
                color="text-rose-400"
            />
        </div>
      </div>
    </div>
  );
}

function VectorCard({ title, score, source, color }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
            <CardContent className="p-6">
                <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-1">{title}</h3>
                <p className="text-xs text-slate-500 mb-4">{source}</p>
                <div className={`text-5xl font-black ${color}`}>{score}%</div>
            </CardContent>
        </Card>
    );
}
