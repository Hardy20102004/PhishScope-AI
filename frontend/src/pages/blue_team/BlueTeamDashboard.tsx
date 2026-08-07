import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ShieldCheck, Activity, Target, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function BlueTeamDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-sky-400">
            <ShieldCheck size={32} />
            Blue Team Readiness Platform
          </h1>
          <p className="text-slate-400 mt-2">Continuous measurement of detection health and SOC operational maturity.</p>
        </div>
        <Button className="bg-sky-600 hover:bg-sky-700 text-white shadow-lg shadow-sky-500/20 gap-2">
            <Activity size={18} /> Generate Scorecard
        </Button>
      </div>

      {/* Main Readiness Score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="bg-slate-900 border-slate-800 col-span-2">
              <CardContent className="p-8 flex items-center justify-between">
                  <div className="space-y-2">
                      <h2 className="text-xl font-bold text-slate-300">Operational Maturity Score</h2>
                      <p className="text-sm text-slate-500 max-w-md">Synthesized from SIEM detection fidelity, Analyst MTTx metrics, and recent Purple Team validations.</p>
                  </div>
                  <div className="flex items-center gap-6">
                      <div className="text-6xl font-black text-sky-400">76<span className="text-3xl text-sky-600">/100</span></div>
                      <div className="flex flex-col gap-1 text-xs font-mono">
                          <span className="text-sky-400 font-bold">MATURITY: MANAGED</span>
                          <span className="text-emerald-400">↑ 4 pts vs Last Month</span>
                      </div>
                  </div>
              </CardContent>
          </Card>
          
          <StatCard title="Noisy Rules (Tuning Req.)" value={14} icon={<Zap className="text-amber-400" />} />
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4 text-slate-200">Sub-Component Scores</h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <ComponentScoreCard title="Detection Health" score={82} desc="Rule fidelity and false positive ratios." />
            <ComponentScoreCard title="Analyst Readiness" score={71} desc="MTTR, Triage speed, and Playbook usage." />
            <ComponentScoreCard title="Purple Team Coverage" score={75} desc="BAS and Red Team validation success rate." />
        </div>
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

function ComponentScoreCard({ title, score, desc }: any) {
    let color = "text-emerald-400";
    if (score < 80) color = "text-sky-400";
    if (score < 60) color = "text-amber-400";

    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
            <CardContent className="p-6">
                <h3 className="text-lg font-bold text-slate-200 mb-1">{title}</h3>
                <p className="text-xs text-slate-500 mb-4 h-8">{desc}</p>
                <div className={`text-4xl font-black ${color}`}>{score}%</div>
            </CardContent>
        </Card>
    );
}
