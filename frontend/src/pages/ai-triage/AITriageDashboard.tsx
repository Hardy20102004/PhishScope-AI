import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BrainCircuit, Filter, Layers, TrendingDown, Crosshair, ArrowRight } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function AITriageDashboard() {
  const navigate = useNavigate();

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-violet-400 to-fuchsia-500">
            <BrainCircuit className="text-violet-500" size={36} />
            AI Alert Triage
          </h1>
          <p className="text-slate-400 mt-2">Intelligent alert clustering, business impact analysis, and prioritization.</p>
        </div>
        <Button onClick={() => navigate('/ai-triage/queue')} className="bg-violet-600 hover:bg-violet-700 text-white">
          <Layers className="mr-2" size={16} />
          View Triage Queue
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Raw Alerts Processed" value="14,289" trend="Past 24h" icon={<Filter className="text-slate-400" />} />
        <MetricCard title="AI Triage Groups" value="842" trend="94% Reduction" icon={<TrendingDown className="text-emerald-400" />} highlight />
        <MetricCard title="Critical Incidents" value="12" trend="Requires Immediate Action" icon={<Crosshair className="text-red-400" />} alert />
        <MetricCard title="Analyst Feedback Rate" value="14.2%" trend="Continuous Learning" icon={<BrainCircuit className="text-violet-400" />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
         <Card className="bg-slate-900 border-slate-800 lg:col-span-2 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Alert Reduction Pipeline</CardTitle>
           </CardHeader>
           <CardContent className="space-y-6">
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Raw Alerts Ingested</span>
                  <span>14,289</span>
                </div>
                <Progress value={100} className="h-2 bg-slate-800" indicatorClassName="bg-slate-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>After Exact-Match Deduplication</span>
                  <span>6,104</span>
                </div>
                <Progress value={42} className="h-2 bg-slate-800" indicatorClassName="bg-blue-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span className="font-semibold text-violet-400">After AI Fuzzy Clustering</span>
                  <span className="text-violet-400 font-bold">842 Actionable Groups</span>
                </div>
                <Progress value={6} className="h-2 bg-slate-800" indicatorClassName="bg-violet-500" />
              </div>
           </CardContent>
         </Card>

         <Card className="bg-slate-900 border-slate-800 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Top Impact Assets</CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
              <AssetRow name="SWIFT Core DB" ip="10.4.2.100" impact={98} />
              <AssetRow name="Active Directory DC-1" ip="10.1.1.5" impact={95} />
              <AssetRow name="Executive Mail Server" ip="10.2.0.50" impact={88} />
              <AssetRow name="Customer Web Portal" ip="172.16.0.12" impact={82} />
           </CardContent>
         </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend, alert = false, highlight = false }: any) {
  return (
    <Card className={`bg-slate-900 border-slate-800 backdrop-blur-xl transition-all duration-300 ${alert ? 'border-red-500/30 shadow-[0_0_15px_rgba(248,113,113,0.15)]' : ''} ${highlight ? 'border-emerald-500/30' : ''}`}>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-slate-400">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className={`text-3xl font-bold ${highlight ? 'text-emerald-400' : 'text-slate-100'}`}>{value}</div>
        <p className={`text-xs mt-2 ${alert ? 'text-red-400' : 'text-slate-500'}`}>{trend}</p>
      </CardContent>
    </Card>
  );
}

function AssetRow({ name, ip, impact }: { name: string, ip: string, impact: number }) {
  return (
    <div className="flex items-center justify-between group cursor-pointer">
      <div>
        <p className="text-sm font-medium text-slate-200 group-hover:text-violet-400 transition-colors">{name}</p>
        <p className="text-xs text-slate-500 font-mono">{ip}</p>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs font-bold text-orange-400">Impact: {impact}</span>
        <ArrowRight size={14} className="text-slate-600 group-hover:text-violet-400" />
      </div>
    </div>
  );
}
