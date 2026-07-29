import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Sparkles, Map, LineChart, ShieldCheck } from 'lucide-react';

export default function StrategicDefenseDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-cyan-400">
            <Sparkles size={32} />
            AI Strategic Cyber Defense
          </h1>
          <p className="text-slate-400 mt-2">Autonomous enterprise security optimization, forecasting, and roadmapping.</p>
        </div>
        <Button className="bg-cyan-600 hover:bg-cyan-700 text-white shadow-lg shadow-cyan-500/20 gap-2">
            Generate 5-Year Outlook
        </Button>
      </div>

      {/* Top Outlook */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <OutlookCard title="Active Optimization Initiatives" value="12" icon={<Map size={24} className="text-cyan-400"/>} />
          <OutlookCard title="Pending AI Recommendations" value="4" icon={<Sparkles size={24} className="text-fuchsia-400 animate-pulse"/>} highlight={true} />
          <OutlookCard title="Projected Resilience (FY27)" value="92/100" icon={<LineChart size={24} className="text-emerald-400"/>} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Recent AI Recommendations */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                      <h3 className="text-lg font-bold text-slate-200">Urgent Strategic Recommendations</h3>
                      <span className="text-xs font-bold text-fuchsia-400 bg-fuchsia-950/30 px-2 py-1 rounded border border-fuchsia-900/50">Human Review Required</span>
                  </div>
                  <div className="space-y-4">
                      <RecRow title="Deprecate Legacy VPN Infrastructure" impact="High Risk Reduction" />
                      <RecRow title="Migrate Tier-1 SOC to Autonomous Triage" impact="Major Cost Savings" />
                      <RecRow title="Consolidate 3 Identity Providers to Azure AD" impact="Operational Efficiency" />
                  </div>
              </CardContent>
          </Card>

          {/* Roadmap Snapshot */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">NIST CSF Optimization Roadmap</h3>
                  <div className="space-y-4">
                      <NistRow func="IDENTIFY" title="Asset Graph Expansion" status="IN PROGRESS" />
                      <NistRow func="PROTECT" title="Zero Trust Rollout Phase 2" status="PLANNED" />
                      <NistRow func="DETECT" title="Cloud Threat Detection Engineering" status="IN PROGRESS" />
                      <NistRow func="RESPOND" title="Automated Ransomware Playbooks" status="COMPLETED" />
                  </div>
              </CardContent>
          </Card>

      </div>
    </div>
  );
}

function OutlookCard({ title, value, icon, highlight = false }: any) {
    return (
        <Card className={`bg-slate-900 border-slate-800 ${highlight ? 'border-fuchsia-900/50' : ''}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <h3 className="text-sm font-bold text-slate-400">{title}</h3>
                    {icon}
                </div>
                <div className={`text-5xl font-black ${highlight ? 'text-fuchsia-400' : 'text-slate-200'}`}>{value}</div>
            </CardContent>
        </Card>
    );
}

function RecRow({ title, impact }: any) {
    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-slate-800/50 hover:border-cyan-900/50 transition-colors cursor-pointer">
            <span className="text-sm font-bold text-slate-300">{title}</span>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{impact}</span>
        </div>
    );
}

function NistRow({ func, title, status }: any) {
    let color = "text-slate-400";
    if (func === 'IDENTIFY') color = "text-blue-400";
    if (func === 'PROTECT') color = "text-purple-400";
    if (func === 'DETECT') color = "text-amber-400";
    if (func === 'RESPOND') color = "text-rose-400";
    
    return (
        <div className="flex justify-between items-center p-2 border-b border-slate-800/50 last:border-0">
            <div className="flex items-center gap-3">
                <span className={`text-[10px] font-black tracking-widest w-20 ${color}`}>{func}</span>
                <span className="text-sm text-slate-300">{title}</span>
            </div>
            <span className="text-xs text-slate-500 font-bold">{status}</span>
        </div>
    );
}
