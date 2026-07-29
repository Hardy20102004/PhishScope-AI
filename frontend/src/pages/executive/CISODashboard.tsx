import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ShieldCheck, Activity, TrendingDown, Target, BrainCircuit, FileText } from 'lucide-react';

export default function CISODashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-500">
            <ShieldCheck className="text-emerald-500" size={36} />
            Executive Security Posture
          </h1>
          <p className="text-slate-400 mt-2">Strategic view of enterprise risk, SOC KPIs, and AI-generated board reporting.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-500/20">
              <FileText className="mr-2" size={16} />
              Export Board Report
            </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Enterprise Risk Score" value="A-" trend="Improved from B+" icon={<Activity className="text-emerald-400" />} highlight />
        <MetricCard title="Mean Time To Resolve" value="14.5 hrs" trend="12% reduction (30d)" icon={<TrendingDown className="text-emerald-400" />} />
        <MetricCard title="Open Critical Incidents" value="2" trend="Requires attention" icon={<Target className="text-amber-400" />} alert />
        <MetricCard title="Automation ROI" value="84.5%" trend="Playbook execution rate" icon={<BrainCircuit className="text-teal-400" />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
         <Card className="bg-slate-900 border-slate-800 lg:col-span-2 shadow-2xl relative overflow-hidden">
           <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
             <BrainCircuit size={120} className="text-emerald-500" />
           </div>
           <CardHeader>
             <CardTitle className="text-slate-200 flex items-center gap-2">
                 <BrainCircuit size={18} className="text-emerald-400" />
                 AI Executive Summary - July 2026
             </CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
              <div className="prose prose-invert prose-emerald max-w-none">
                  <p className="text-slate-300 leading-relaxed text-lg">
                      The Security Operations Center successfully mitigated <strong>142</strong> major incidents this month. 
                      Strategic investments in the new SOAR platform have driven our Mean Time To Resolve (MTTR) down by 12%.
                  </p>
                  <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 mt-4">
                      <h4 className="text-emerald-400 font-semibold mb-2 uppercase tracking-wider text-xs">Primary Risk Exposure</h4>
                      <p className="text-slate-400 text-sm">
                          The <strong>Finance</strong> business unit currently represents the highest risk vector due to an ongoing targeted phishing campaign attributed to APT29. 
                          Endpoint isolation controls are actively holding, but user awareness training is highly recommended.
                      </p>
                  </div>
              </div>
           </CardContent>
         </Card>

         <Card className="bg-slate-900 border-slate-800 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Business Unit Risk Map</CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
              <RiskRow unit="Finance" score={85} status="HIGH" />
              <RiskRow unit="Human Resources" score={65} status="MEDIUM" />
              <RiskRow unit="Engineering" score={40} status="LOW" />
              <RiskRow unit="Marketing" score={25} status="LOW" />
           </CardContent>
         </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend, highlight = false, alert = false }: any) {
  return (
    <Card className={`bg-slate-900 border-slate-800 backdrop-blur-xl transition-all duration-300 ${highlight ? 'border-emerald-500/30 shadow-[0_0_20px_rgba(16,185,129,0.15)]' : ''} ${alert ? 'border-amber-500/30' : ''}`}>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-slate-400">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className={`text-3xl font-bold ${highlight ? 'text-emerald-400' : 'text-slate-100'}`}>{value}</div>
        <p className={`text-xs mt-2 ${alert ? 'text-amber-400' : 'text-slate-500'}`}>{trend}</p>
      </CardContent>
    </Card>
  );
}

function RiskRow({ unit, score, status }: any) {
    const getStatusColor = (s: string) => {
        switch(s) {
            case 'HIGH': return 'bg-rose-500 text-rose-100 border-rose-600';
            case 'MEDIUM': return 'bg-amber-500 text-amber-100 border-amber-600';
            default: return 'bg-emerald-500 text-emerald-100 border-emerald-600';
        }
    };
    
    return (
        <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800/50">
            <span className="text-sm font-medium text-slate-200">{unit}</span>
            <div className="flex items-center gap-3">
                <span className="text-xs font-mono text-slate-400">Score: {score}</span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getStatusColor(status)}`}>
                    {status}
                </span>
            </div>
        </div>
    );
}
