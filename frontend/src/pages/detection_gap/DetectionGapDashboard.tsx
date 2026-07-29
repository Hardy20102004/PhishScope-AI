import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Activity, Target, ShieldAlert, Zap } from 'lucide-react';

export default function DetectionGapDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-cyan-400">
            <Activity size={32} />
            Detection Gap Analysis
          </h1>
          <p className="text-slate-400 mt-2">Continuous evaluation of enterprise SIEM/EDR rule base against the MITRE ATT&CK framework.</p>
        </div>
        <Button className="bg-cyan-600 hover:bg-cyan-700 text-white shadow-lg shadow-cyan-500/20 gap-2">
            <Target size={18} /> Generate Gap Report
        </Button>
      </div>

      {/* Top Level Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <MetricCard title="Overall MITRE Coverage" value="64%" icon={<Target size={20} className="text-cyan-400"/>} color="text-cyan-400" />
          <MetricCard title="Critical Blind Spots" value="8" icon={<ShieldAlert size={20} className="text-rose-500 animate-pulse"/>} color="text-rose-400" />
          <MetricCard title="Techniques Monitored" value="142" icon={<Activity size={20} className="text-slate-500"/>} />
          <MetricCard title="Active Optimizations" value="12" icon={<Zap size={20} className="text-amber-500"/>} color="text-amber-400" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Top Blind Spots */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Top Critical Blind Spots</h3>
                  <div className="space-y-4">
                      <BlindSpotRow technique="T1562.001" name="Disable Windows Event Logging" coverage={0} trend="DOWN" />
                      <BlindSpotRow technique="T1048.003" name="Exfiltration Over Alternative Protocol" coverage={12} trend="FLAT" />
                      <BlindSpotRow technique="T1484.001" name="Group Policy Modification" coverage={25} trend="UP" />
                  </div>
              </CardContent>
          </Card>

          {/* Coverage by Tactic */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Coverage by Tactic Phase</h3>
                  <div className="space-y-4">
                      <TacticRow name="Initial Access" score={85} />
                      <TacticRow name="Execution" score={72} />
                      <TacticRow name="Defense Evasion" score={41} />
                      <TacticRow name="Exfiltration" score={33} />
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

function BlindSpotRow({ technique, name, coverage, trend }: any) {
    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-rose-900/30">
            <div className="flex flex-col">
                <span className="text-sm font-bold text-slate-200">{name}</span>
                <span className="text-[10px] text-rose-400 font-mono uppercase">{technique}</span>
            </div>
            <div className="flex gap-4 text-right">
                <div className="flex flex-col">
                    <span className="text-[10px] text-slate-500 uppercase">Coverage</span>
                    <span className="text-sm font-bold text-rose-400">{coverage}%</span>
                </div>
            </div>
        </div>
    );
}

function TacticRow({ name, score }: any) {
    let color = "bg-emerald-500";
    if (score < 70) color = "bg-amber-500";
    if (score < 40) color = "bg-rose-500";

    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between text-xs font-bold text-slate-300">
                <span>{name}</span>
                <span>{score}%</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-1.5">
                <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${score}%` }}></div>
            </div>
        </div>
    );
}
