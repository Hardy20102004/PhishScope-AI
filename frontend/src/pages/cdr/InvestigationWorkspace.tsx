import React from 'react';
import { Target, Link as LinkIcon, AlertTriangle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function InvestigationWorkspace() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <div className="flex items-center gap-2 mb-2">
                    <span className="text-[10px] font-black tracking-widest px-2 py-0.5 rounded border border-rose-900/50 bg-rose-950/30 text-rose-400">CRITICAL INVESTIGATION</span>
                </div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Target className="text-rose-400" />
                    Suspicious Activity: svc_legacy_deploy
                </h2>
                <p className="text-slate-400 mt-1">AI Correlation Engine linked 5 detections to principal: <span className="font-mono text-indigo-400">svc_legacy_deploy</span></p>
            </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div className="lg:col-span-2 space-y-6">
                
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <h3 className="text-lg font-bold text-slate-200 mb-4 border-b border-slate-800 pb-2">Correlated Attack Narrative</h3>
                        <p className="text-slate-400 text-sm leading-relaxed mb-6">
                            The `CloudCorrelationEngine` has identified a highly suspicious sequence of events tied to the `svc_legacy_deploy` IAM role. This role, which was previously dormant for 120 days (identified by CIEM), suddenly authenticated without MFA. Within 5 minutes, it initiated an unauthorized Kubernetes API call (detected by K8s Security) to spawn a privileged container, and subsequently attempted to delete multiple S3 bucket policies. This pattern strongly indicates a credential compromise followed by privilege escalation and defense evasion.
                        </p>
                        
                        <div className="space-y-4">
                            <h4 className="text-sm font-bold text-slate-300 uppercase tracking-wider">Detection Timeline</h4>
                            <TimelineEvent time="10:42:01" source="AWS CloudTrail" alert="Console Login Without MFA" severity="HIGH" />
                            <TimelineEvent time="10:45:12" source="EKS Audit Log" alert="Unauthorized K8s API Call (create pod)" severity="HIGH" />
                            <TimelineEvent time="10:45:15" source="Container Runtime" alert="Privileged Container Spawned" severity="CRITICAL" />
                            <TimelineEvent time="10:47:00" source="AWS CloudTrail" alert="Mass S3 Policy Deletion" severity="CRITICAL" />
                        </div>
                    </CardContent>
                </Card>

            </div>

            <div className="space-y-6">
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Entity Graph</h3>
                        <div className="space-y-3">
                            <EntityNode type="Identity" value="svc_legacy_deploy" icon={<LinkIcon size={14} className="text-slate-500" />} />
                            <EntityNode type="IP Address" value="185.12.3.4" icon={<LinkIcon size={14} className="text-rose-500" />} />
                            <EntityNode type="Cluster" value="prod-eks-us-east" icon={<LinkIcon size={14} className="text-slate-500" />} />
                        </div>
                    </CardContent>
                </Card>
            </div>

        </div>
    </div>
  );
}

function TimelineEvent({ time, source, alert, severity }: any) {
    let sevColor = "text-amber-400";
    if (severity === 'CRITICAL') sevColor = "text-rose-400";
    if (severity === 'HIGH') sevColor = "text-orange-400";

    return (
        <div className="flex gap-4 p-3 bg-slate-950/50 rounded border border-slate-800/50 hover:bg-slate-800/50 transition-colors">
            <div className="text-slate-500 font-mono text-xs pt-0.5">{time}</div>
            <div>
                <div className="text-sm font-bold text-slate-200 flex items-center gap-2">
                    <AlertTriangle size={14} className={sevColor} /> {alert}
                </div>
                <div className="text-xs text-slate-500 mt-1">Source: {source}</div>
            </div>
        </div>
    );
}

function EntityNode({ type, value, icon }: any) {
    return (
        <div className="flex items-center gap-2 bg-slate-950 p-2 rounded border border-slate-800">
            {icon}
            <div>
                <div className="text-[10px] uppercase font-bold text-slate-500">{type}</div>
                <div className="text-xs font-mono text-slate-200">{value}</div>
            </div>
        </div>
    );
}
