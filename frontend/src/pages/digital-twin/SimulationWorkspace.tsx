import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Clock, ShieldAlert } from 'lucide-react';

export default function SimulationWorkspace() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <h1 className="text-2xl font-bold text-slate-200 mb-6">Simulation Results: Q4 M&A Forecast</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <ResultCard 
                title="Forecasted MTTR" 
                value="45.2 mins" 
                delta="+15.2 mins (Degraded)" 
                status="danger"
                icon={<Clock size={20} />} 
            />
            <ResultCard 
                title="SLA Breach Rate" 
                value="14.5%" 
                delta="Critical Queueing Detected" 
                status="danger"
                icon={<ShieldAlert size={20} />} 
            />
            <ResultCard 
                title="Analyst Utilization" 
                value="115%" 
                delta="Burnout Risk High" 
                status="danger"
                icon={<Activity size={20} />} 
            />
        </div>

        <Card className="bg-slate-900 border-slate-800 mt-8">
            <CardHeader>
                <CardTitle className="text-slate-200 text-sm font-semibold uppercase tracking-wider">Queueing Theory Projection</CardTitle>
            </CardHeader>
            <CardContent className="h-64 flex items-center justify-center border-t border-slate-800/50 bg-slate-950/50 relative">
                {/* Simulated Chart Placeholder */}
                <div className="absolute inset-x-8 inset-y-8 flex items-end justify-between px-4">
                    <div className="w-12 bg-slate-800 rounded-t h-1/6"></div>
                    <div className="w-12 bg-slate-800 rounded-t h-2/6"></div>
                    <div className="w-12 bg-indigo-900/50 rounded-t h-3/6 border-t-2 border-indigo-500"></div>
                    <div className="w-12 bg-rose-900/50 rounded-t h-5/6 border-t-2 border-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.5)]"></div>
                    <div className="w-12 bg-rose-900/50 rounded-t h-full border-t-2 border-rose-500 shadow-[0_0_20px_rgba(244,63,94,0.8)]"></div>
                </div>
                <div className="absolute inset-0 flex items-center justify-center opacity-30 pointer-events-none">
                     <span className="text-6xl font-black text-rose-500 transform -rotate-12">CAPACITY EXCEEDED</span>
                </div>
            </CardContent>
        </Card>
    </div>
  );
}

function ResultCard({ title, value, delta, status, icon }: any) {
    const isDanger = status === 'danger';
    return (
        <Card className={`bg-slate-900 border-slate-800 ${isDanger ? 'border-b-4 border-b-rose-500' : 'border-b-4 border-b-emerald-500'}`}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">{title}</CardTitle>
                <div className={isDanger ? 'text-rose-500' : 'text-emerald-500'}>{icon}</div>
            </CardHeader>
            <CardContent>
                <div className={`text-3xl font-bold ${isDanger ? 'text-rose-400' : 'text-emerald-400'}`}>{value}</div>
                <p className="text-xs text-slate-500 mt-2 font-medium">{delta}</p>
            </CardContent>
        </Card>
    );
}
