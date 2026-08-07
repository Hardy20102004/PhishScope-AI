import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Briefcase, Landmark, ShieldCheck, ActivitySquare, BrainCircuit } from 'lucide-react';

export default function ExecutiveDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-indigo-400">
            <Briefcase size={32} />
            Executive Decision Intelligence
          </h1>
          <p className="text-slate-400 mt-2">Consolidated governance, business impact, and investment analytics for the C-Suite.</p>
        </div>
        <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/20 gap-2">
            <BrainCircuit size={18} /> Ask AI Advisor
        </Button>
      </div>

      {/* Top KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard title="NIST CSF Compliance" value="84%" icon={<Landmark size={20} className="text-indigo-400"/>} color="text-indigo-400" />
          <MetricCard title="Critical Services At Risk" value="1" icon={<ActivitySquare size={20} className="text-rose-500 animate-pulse"/>} color="text-rose-400" />
          <MetricCard title="Automation ROI (Hours)" value="420" icon={<ShieldCheck size={20} className="text-emerald-500"/>} color="text-emerald-400" />
          <MetricCard title="Strategic Roadmap" value="On Track" icon={<Briefcase size={20} className="text-sky-500"/>} color="text-sky-400" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Business Impact Table */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Critical Business Impact</h3>
                  <div className="space-y-4">
                      <ImpactRow service="Production Payments API" status="AT RISK" riskScore={88} />
                      <ImpactRow service="Global Active Directory" status="SECURE" riskScore={21} />
                      <ImpactRow service="Customer Web Portal" status="DEGRADED" riskScore={65} />
                  </div>
              </CardContent>
          </Card>

          {/* Governance Progress */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Strategic Initiative Progress</h3>
                  <div className="space-y-4">
                      <ProgressRow name="Zero Trust Identity Rollout" progress={85} />
                      <ProgressRow name="Cloud Workload Protection (CWPP)" progress={60} />
                      <ProgressRow name="Automated SOAR Deployment" progress={95} />
                      <ProgressRow name="Data Loss Prevention (DLP) Revamp" progress={20} />
                  </div>
              </CardContent>
          </Card>

      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, color = "text-slate-200" }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">{title}</h3>
                    {icon}
                </div>
                <div className={`text-4xl font-black ${color}`}>{value}</div>
            </CardContent>
        </Card>
    );
}

function ImpactRow({ service, status, riskScore }: any) {
    let statusColor = "text-emerald-400 border-emerald-900/50 bg-emerald-950/20";
    if (status === 'DEGRADED') statusColor = "text-amber-400 border-amber-900/50 bg-amber-950/20";
    if (status === 'AT RISK') statusColor = "text-rose-400 border-rose-900/50 bg-rose-950/20 animate-pulse";

    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <span className="text-sm font-bold text-slate-200">{service}</span>
            <div className="flex items-center gap-4">
                <div className="text-xs text-slate-500 font-mono">Risk: <span className="text-slate-300">{riskScore}/100</span></div>
                <div className={`text-[10px] font-bold px-2 py-1 rounded border ${statusColor}`}>
                    {status}
                </div>
            </div>
        </div>
    );
}

function ProgressRow({ name, progress }: any) {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between text-xs font-bold text-slate-300">
                <span>{name}</span>
                <span>{progress}%</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="h-2 rounded-full bg-indigo-500" style={{ width: `${progress}%` }}></div>
            </div>
        </div>
    );
}
