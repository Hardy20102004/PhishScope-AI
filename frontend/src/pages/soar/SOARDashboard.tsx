import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Zap, Play, CheckSquare, Clock, Cpu } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function SOARDashboard() {
  const navigate = useNavigate();

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
            <Zap className="text-cyan-500" size={36} />
            SOAR & Automation
          </h1>
          <p className="text-slate-400 mt-2">Human-guided playbooks and automated response orchestration.</p>
        </div>
        <div className="flex gap-4">
            <Button onClick={() => navigate('/soar/designer')} className="bg-cyan-600 hover:bg-cyan-700 text-white shadow-lg shadow-cyan-500/20">
              <Cpu className="mr-2" size={16} />
              Design Playbook
            </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Executions (30d)" value="4,291" trend="+12% from last month" icon={<Play className="text-cyan-400" />} />
        <MetricCard title="Time Saved" value="1,402 hrs" trend="Automation efficiency" icon={<Clock className="text-emerald-400" />} highlight />
        <MetricCard title="Pending Approvals" value="12" trend="Requires manual review" icon={<CheckSquare className="text-amber-400" />} alert />
        <MetricCard title="Active Connectors" value="24" trend="EDR, SIEM, Firewalls" icon={<Zap className="text-blue-400" />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
         <Card className="bg-slate-900 border-slate-800 lg:col-span-2 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Playbook Library</CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
              <PlaybookRow name="Ransomware Containment (Standard)" executions={142} successRate={98} />
              <PlaybookRow name="Phishing Email Extraction & Delete" executions={890} successRate={99} />
              <PlaybookRow name="Compromised Credential Revoke" executions={34} successRate={100} />
              <PlaybookRow name="Suspicious IP Enrichment (VirusTotal)" executions={2104} successRate={95} />
           </CardContent>
         </Card>

         <Card className="bg-slate-900 border-slate-800 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Connector Health</CardTitle>
           </CardHeader>
           <CardContent className="space-y-6">
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>CrowdStrike Falcon (EDR)</span>
                  <span className="text-emerald-400">99.9% Uptime</span>
                </div>
                <Progress value={99.9} className="h-2 bg-slate-800" indicatorClassName="bg-emerald-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Palo Alto (Firewall)</span>
                  <span className="text-emerald-400">99.9% Uptime</span>
                </div>
                <Progress value={99.9} className="h-2 bg-slate-800" indicatorClassName="bg-emerald-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>ServiceNow (Ticketing)</span>
                  <span className="text-amber-400">85.0% Uptime</span>
                </div>
                <Progress value={85} className="h-2 bg-slate-800" indicatorClassName="bg-amber-500" />
              </div>
           </CardContent>
         </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend, highlight = false, alert = false }: any) {
  return (
    <Card className={`bg-slate-900 border-slate-800 backdrop-blur-xl transition-all duration-300 ${highlight ? 'border-emerald-500/30' : ''} ${alert ? 'border-amber-500/30 shadow-[0_0_15px_rgba(245,158,11,0.15)]' : ''}`}>
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

function PlaybookRow({ name, executions, successRate }: { name: string, executions: number, successRate: number }) {
  const navigate = useNavigate();
  return (
    <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800/50 hover:bg-slate-800 transition-colors cursor-pointer" onClick={() => navigate('/soar/designer')}>
      <div>
        <p className="text-sm font-medium text-slate-200">{name}</p>
        <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
            <span>{executions} executions (30d)</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs text-slate-400">Success:</span>
        <span className="text-sm font-bold text-emerald-400">{successRate}%</span>
      </div>
    </div>
  );
}
