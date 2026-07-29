import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ShieldAlert, Target, Clock, Activity, AlertOctagon } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function SOCDashboard() {
  const navigate = useNavigate();

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-rose-500 to-orange-500">
            <ShieldAlert className="text-rose-500" size={36} />
            Incident Response Command Center
          </h1>
          <p className="text-slate-400 mt-2">Manage the complete DFIR lifecycle from detection to closure.</p>
        </div>
        <div className="flex gap-4">
            <Button onClick={() => navigate('/incident-response/new')} className="bg-rose-600 hover:bg-rose-700 text-white shadow-lg shadow-rose-500/20">
              <AlertOctagon className="mr-2" size={16} />
              Declare Incident
            </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Active Incidents" value="8" trend="2 Critical" icon={<Activity className="text-rose-400" />} alert />
        <MetricCard title="Mean Time To Respond (MTTR)" value="14m" trend="-2m from last month" icon={<Clock className="text-emerald-400" />} />
        <MetricCard title="Pending Tasks" value="45" trend="Across all active cases" icon={<Target className="text-amber-400" />} />
        <MetricCard title="Evidence Items Logged" value="1,204" trend="With full Chain of Custody" icon={<ShieldAlert className="text-blue-400" />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
         <Card className="bg-slate-900 border-slate-800 lg:col-span-2 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Incident Queue</CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
              <IncidentRow id="INC-2026-084" name="Ransomware attempt on HR Subnet" status="CONTAINMENT" severity="CRITICAL" time="2h ago" />
              <IncidentRow id="INC-2026-083" name="Suspected Data Exfiltration via DNS" status="INVESTIGATING" severity="HIGH" time="5h ago" />
              <IncidentRow id="INC-2026-082" name="Anomalous Login to Production DB" status="RESOLVED" severity="MEDIUM" time="1d ago" />
              <IncidentRow id="INC-2026-081" name="Phishing Campaign targeting Finance" status="CLOSED" severity="LOW" time="3d ago" />
           </CardContent>
         </Card>

         <Card className="bg-slate-900 border-slate-800 shadow-2xl">
           <CardHeader>
             <CardTitle className="text-slate-200">Incident Lifecycle Load</CardTitle>
           </CardHeader>
           <CardContent className="space-y-6">
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Under Investigation</span>
                  <span>5 Incidents</span>
                </div>
                <Progress value={60} className="h-2 bg-slate-800" indicatorClassName="bg-amber-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Containment & Eradication</span>
                  <span>2 Incidents</span>
                </div>
                <Progress value={25} className="h-2 bg-slate-800" indicatorClassName="bg-rose-500" />
              </div>
              <div>
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Pending Post-Incident Review</span>
                  <span>1 Incident</span>
                </div>
                <Progress value={10} className="h-2 bg-slate-800" indicatorClassName="bg-blue-500" />
              </div>
           </CardContent>
         </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend, alert = false }: any) {
  return (
    <Card className={`bg-slate-900 border-slate-800 backdrop-blur-xl transition-all duration-300 ${alert ? 'border-rose-500/30 shadow-[0_0_15px_rgba(244,63,94,0.15)]' : ''}`}>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-slate-400">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold text-slate-100">{value}</div>
        <p className={`text-xs mt-2 ${alert ? 'text-rose-400' : 'text-slate-500'}`}>{trend}</p>
      </CardContent>
    </Card>
  );
}

function IncidentRow({ id, name, status, severity, time }: { id: string, name: string, status: string, severity: string, time: string }) {
  const navigate = useNavigate();
  
  const getSeverityColor = (sev: string) => {
      switch(sev) {
          case 'CRITICAL': return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
          case 'HIGH': return 'bg-orange-500/10 text-orange-400 border-orange-500/20';
          case 'MEDIUM': return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
          default: return 'bg-slate-800 text-slate-400 border-slate-700';
      }
  };

  return (
    <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800/50 hover:bg-slate-800 transition-colors cursor-pointer" onClick={() => navigate(`/incident-response/${id}`)}>
      <div className="flex items-center gap-4">
          <span className={`text-xs font-mono px-2 py-1 rounded border ${getSeverityColor(severity)}`}>
              {severity}
          </span>
          <div>
            <p className="text-sm font-medium text-slate-200">{name}</p>
            <p className="text-xs text-slate-500 font-mono mt-1">{id} • Updated {time}</p>
          </div>
      </div>
      <div>
        <span className="text-xs px-2 py-1 rounded-full border bg-slate-800 text-slate-400 border-slate-700">
            {status}
        </span>
      </div>
    </div>
  );
}
