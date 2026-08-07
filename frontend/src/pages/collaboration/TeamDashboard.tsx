import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Users, UserCheck, UserX, Activity, Hash, MessageSquare } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function TeamDashboard() {
  const navigate = useNavigate();

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-500">
            <Users className="text-purple-500" size={36} />
            SOC Collaboration & Presence
          </h1>
          <p className="text-slate-400 mt-2">Manage team workload, active workspaces, and cross-team communication.</p>
        </div>
        <div className="flex gap-4">
            <Button onClick={() => navigate('/collaboration/workspace/new')} className="bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-500/20">
              <Hash className="mr-2" size={16} />
              Create Shared Room
            </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Active Analysts" value="12" trend="Shift 1 Online" icon={<UserCheck className="text-emerald-400" />} highlight />
        <MetricCard title="Average Bandwidth" value="78%" trend="Operating near capacity" icon={<Activity className="text-amber-400" />} alert />
        <MetricCard title="Active Workspaces" value="5" trend="3 Incident, 2 Threat Hunt" icon={<Hash className="text-blue-400" />} />
        <MetricCard title="Messages Today" value="842" trend="Across all secure rooms" icon={<MessageSquare className="text-purple-400" />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
         <Card className="bg-slate-900 border-slate-800 lg:col-span-2 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Active Workspaces</CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
              <WorkspaceRow name="inc-2026-084-ransomware" type="INCIDENT" members={5} unread={12} />
              <WorkspaceRow name="hunt-apt29-lateral" type="HUNT" members={3} unread={0} />
              <WorkspaceRow name="intel-sharing-global" type="INTEL" members={42} unread={5} />
              <WorkspaceRow name="soc-general" type="GENERAL" members={18} unread={2} />
           </CardContent>
         </Card>

         <Card className="bg-slate-900 border-slate-800 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Team Presence & Workload</CardTitle>
           </CardHeader>
           <CardContent className="space-y-6">
              <AnalystRow name="Jane Doe" role="L3 DFIR" status="ONLINE" load={90} />
              <AnalystRow name="Bob Smith" role="L2 SOC" status="ONLINE" load={45} />
              <AnalystRow name="Alice Wang" role="Threat Intel" status="BUSY" load={100} />
              <AnalystRow name="Charlie Ray" role="L1 Triage" status="OFFLINE" load={0} />
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

function WorkspaceRow({ name, type, members, unread }: { name: string, type: string, members: number, unread: number }) {
  const navigate = useNavigate();
  return (
    <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800/50 hover:bg-slate-800 transition-colors cursor-pointer" onClick={() => navigate('/collaboration/workspace/demo')}>
      <div className="flex items-center gap-4">
          <Hash className="text-slate-500" size={18} />
          <div>
            <p className="text-sm font-medium text-slate-200">#{name}</p>
            <p className="text-xs text-slate-500 mt-1">{members} members</p>
          </div>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-[10px] font-mono px-2 py-1 rounded border bg-slate-800 text-slate-400 border-slate-700">
            {type}
        </span>
        {unread > 0 && (
            <span className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center text-xs font-bold border border-purple-500/50">
                {unread}
            </span>
        )}
      </div>
    </div>
  );
}

function AnalystRow({ name, role, status, load }: any) {
    const getStatusColor = (s: string) => {
        switch(s) {
            case 'ONLINE': return 'bg-emerald-500';
            case 'BUSY': return 'bg-amber-500';
            default: return 'bg-slate-600';
        }
    };
    
    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-2">
                    <div className="relative">
                        <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-xs font-bold text-slate-300">
                            {name.charAt(0)}
                        </div>
                        <div className={`absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full border-2 border-slate-900 ${getStatusColor(status)}`}></div>
                    </div>
                    <div>
                        <p className="text-sm text-slate-200">{name}</p>
                        <p className="text-[10px] text-slate-500">{role}</p>
                    </div>
                </div>
                <span className="text-xs font-mono text-slate-400">{load}% Load</span>
            </div>
            <Progress value={load} className="h-1.5 bg-slate-800" indicatorClassName={load > 80 ? 'bg-amber-500' : 'bg-emerald-500'} />
        </div>
    );
}
