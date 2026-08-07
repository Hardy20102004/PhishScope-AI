import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Radar, Target, Crosshair, BookOpen, Search } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function ThreatHuntingDashboard() {
  const navigate = useNavigate();

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-amber-500">
            <Radar className="text-red-500" size={36} />
            AI Threat Hunting
          </h1>
          <p className="text-slate-400 mt-2">Proactive, hypothesis-driven intelligence gathering and correlation.</p>
        </div>
        <div className="flex gap-4">
            <Button onClick={() => navigate('/threat-hunting/workspace')} className="bg-red-600 hover:bg-red-700 text-white shadow-lg shadow-red-500/20">
              <Crosshair className="mr-2" size={16} />
              Start New Hunt
            </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Active Hunt Sessions" value="14" trend="3 pending review" icon={<Radar className="text-red-400" />} />
        <MetricCard title="AI Hypotheses Generated" value="128" trend="+12 this week" icon={<Target className="text-amber-400" />} />
        <MetricCard title="Pattern Discoveries" value="45" trend="Infrastructure Reuse Identified" icon={<Search className="text-blue-400" />} />
        <MetricCard title="MITRE ATT&CK Coverage" value="82%" trend="+5% from previous quarter" icon={<BookOpen className="text-emerald-400" />} highlight />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
         <Card className="bg-slate-900 border-slate-800 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Recent Hunt Sessions</CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
              <HuntRow name="Operation Night Owl" status="ACTIVE" queries={24} hypotheses={3} />
              <HuntRow name="Q2 Credential Stuffing Sweep" status="COMPLETED" queries={150} hypotheses={12} />
              <HuntRow name="APT32 Infrastructure Overlap" status="ACTIVE" queries={8} hypotheses={1} />
              <HuntRow name="Zero-Day Indicator Sweep" status="ARCHIVED" queries={42} hypotheses={0} />
           </CardContent>
         </Card>

         <Card className="bg-slate-900 border-slate-800 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Top MITRE Tactics Hunted</CardTitle>
           </CardHeader>
           <CardContent className="space-y-6">
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Execution (TA0002)</span>
                  <span>45 Hunts</span>
                </div>
                <Progress value={80} className="h-2 bg-slate-800" indicatorClassName="bg-red-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Credential Access (TA0006)</span>
                  <span>38 Hunts</span>
                </div>
                <Progress value={65} className="h-2 bg-slate-800" indicatorClassName="bg-amber-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Lateral Movement (TA0008)</span>
                  <span>22 Hunts</span>
                </div>
                <Progress value={40} className="h-2 bg-slate-800" indicatorClassName="bg-blue-500" />
              </div>
           </CardContent>
         </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend, highlight = false }: any) {
  return (
    <Card className={`bg-slate-900 border-slate-800 backdrop-blur-xl transition-all duration-300 ${highlight ? 'border-emerald-500/30' : ''}`}>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-slate-400">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className={`text-3xl font-bold ${highlight ? 'text-emerald-400' : 'text-slate-100'}`}>{value}</div>
        <p className="text-xs mt-2 text-slate-500">{trend}</p>
      </CardContent>
    </Card>
  );
}

function HuntRow({ name, status, queries, hypotheses }: { name: string, status: string, queries: number, hypotheses: number }) {
  const navigate = useNavigate();
  return (
    <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800/50 hover:bg-slate-800 transition-colors cursor-pointer" onClick={() => navigate('/threat-hunting/workspace')}>
      <div>
        <p className="text-sm font-medium text-slate-200">{name}</p>
        <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
            <span>{queries} queries</span>
            <span>{hypotheses} hypotheses</span>
        </div>
      </div>
      <div>
        <span className={`text-xs px-2 py-1 rounded-full border ${status === 'ACTIVE' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-slate-800 text-slate-400 border-slate-700'}`}>
            {status}
        </span>
      </div>
    </div>
  );
}
