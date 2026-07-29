import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ShieldAlert, BookOpen, Clock, Activity, FileText, CheckCircle } from 'lucide-react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';

export default function IncidentWorkspace() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  // Mock Incident Data
  const incident = {
      id: id || "INC-2026-084",
      title: "Ransomware attempt on HR Subnet",
      status: "CONTAINMENT",
      severity: "CRITICAL",
      description: "Initial access gained via Phishing. Lateral movement detected towards HR database servers. Ransomware payload blocked by EDR on 2 hosts.",
      lead: "Jane Doe (Principal DFIR)"
  };

  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
       <div className="flex justify-between items-start">
           <div>
               <div className="flex items-center gap-3 mb-2">
                   <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/50">
                       {incident.severity}
                   </Badge>
                   <span className="text-slate-500 text-sm font-mono">{incident.id}</span>
                   <Badge variant="outline" className="bg-slate-800 text-slate-300 border-slate-700">
                       {incident.status}
                   </Badge>
               </div>
               <h1 className="text-3xl font-bold">{incident.title}</h1>
               <p className="text-slate-400 mt-2 max-w-3xl leading-relaxed">{incident.description}</p>
           </div>
           <div className="flex gap-2 flex-col items-end">
               <span className="text-sm text-slate-400">Lead Investigator: <span className="text-slate-200">{incident.lead}</span></span>
               <div className="flex gap-2 mt-2">
                   <Button variant="outline" className="bg-slate-900 border-slate-700 hover:bg-slate-800">Change Status</Button>
                   <Button className="bg-rose-600 hover:bg-rose-700">Generate Executive Report</Button>
               </div>
           </div>
       </div>

       <Tabs defaultValue="overview" className="w-full mt-6">
           <TabsList className="bg-slate-900 border border-slate-800 p-1">
               <TabsTrigger value="overview" className="data-[state=active]:bg-slate-800">Overview</TabsTrigger>
               <TabsTrigger value="evidence" className="data-[state=active]:bg-slate-800" onClick={() => navigate(`/incident-response/${incident.id}/evidence`)}>Evidence Locker</TabsTrigger>
               <TabsTrigger value="tasks" className="data-[state=active]:bg-slate-800" onClick={() => navigate(`/incident-response/${incident.id}/tasks`)}>Task Board</TabsTrigger>
               <TabsTrigger value="timeline" className="data-[state=active]:bg-slate-800">Timeline</TabsTrigger>
           </TabsList>

           <TabsContent value="overview" className="mt-6 space-y-6">
               <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                   <div className="lg:col-span-2 space-y-6">
                       <Card className="bg-indigo-950/20 border-indigo-500/20 shadow-2xl relative overflow-hidden">
                           <CardHeader>
                               <CardTitle className="text-indigo-400 flex items-center gap-2">
                                   <Activity size={20} /> AI Investigation Summary
                               </CardTitle>
                           </CardHeader>
                           <CardContent className="space-y-4">
                               <p className="text-sm text-slate-300 leading-relaxed">
                                   The attacker likely compromised the HR user 'j.smith' at 08:14 UTC. 
                                   Subsequent PowerShell commands mapped network drives to `10.2.0.50`. 
                                   EDR blocked `encrypt.exe` execution. Recommend immediately isolating the `/24` HR subnet.
                               </p>
                               <div className="bg-slate-950 p-4 rounded-lg border border-indigo-500/10">
                                   <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Suggested Next Steps</h4>
                                   <ul className="space-y-2 text-sm text-slate-300">
                                       <li className="flex items-center gap-2"><CheckCircle size={14} className="text-emerald-500"/> Force password reset for all HR users.</li>
                                       <li className="flex items-center gap-2"><CheckCircle size={14} className="text-emerald-500"/> Block outbound C2 communication to `malicious-domain.com`.</li>
                                   </ul>
                               </div>
                           </CardContent>
                       </Card>

                       <Card className="bg-slate-900 border-slate-800">
                           <CardHeader>
                               <CardTitle className="text-slate-200">Recent Tasks</CardTitle>
                           </CardHeader>
                           <CardContent>
                               <div className="space-y-2">
                                   <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                                       <span className="text-sm text-slate-300 line-through">Isolate affected HR endpoints</span>
                                       <Badge className="bg-emerald-500/10 text-emerald-400">DONE</Badge>
                                   </div>
                                   <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                                       <span className="text-sm text-slate-300">Analyze memory dump from HR-05</span>
                                       <Badge className="bg-amber-500/10 text-amber-400">IN PROGRESS</Badge>
                                   </div>
                               </div>
                           </CardContent>
                       </Card>
                   </div>
                   
                   <div className="space-y-6">
                        <Card className="bg-slate-900 border-slate-800">
                           <CardHeader>
                               <CardTitle className="text-slate-200 text-sm flex items-center gap-2">
                                   <FileText size={16} /> Key Evidence
                               </CardTitle>
                           </CardHeader>
                           <CardContent>
                               <ul className="space-y-3">
                                   <li className="text-xs font-mono bg-slate-950 p-2 rounded border border-slate-800">
                                       <span className="text-blue-400 block mb-1">FILE HASH (SHA256)</span>
                                       e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
                                   </li>
                                   <li className="text-xs font-mono bg-slate-950 p-2 rounded border border-slate-800">
                                       <span className="text-orange-400 block mb-1">C2 IP ADDRESS</span>
                                       198.51.100.42
                                   </li>
                               </ul>
                               <Button variant="ghost" className="w-full mt-4 text-xs text-slate-400" onClick={() => navigate(`/incident-response/${incident.id}/evidence`)}>
                                   View Full Evidence Locker →
                               </Button>
                           </CardContent>
                       </Card>
                   </div>
               </div>
           </TabsContent>
       </Tabs>
    </div>
  );
}
