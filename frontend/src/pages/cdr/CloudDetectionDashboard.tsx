import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Shield, Activity, Target, AlertTriangle } from 'lucide-react';

export default function CloudDetectionDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-red-400">
            <Shield size={32} />
            Cloud Detection & Response (CDR)
          </h1>
          <p className="text-slate-400 mt-2">Continuous multi-cloud telemetry ingestion, threat detection, and incident response.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-red-600 hover:bg-red-700 text-white shadow-lg shadow-red-500/20 gap-2">
                <Target size={18} /> Open Investigation Workspace
            </Button>
        </div>
      </div>

      {/* Top Posture Area */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <PostureCard title="Telemetry Processed (24h)" value="14.2M" icon={<Activity size={24} className="text-slate-400"/>} />
          <PostureCard title="Active Detections" value="84" icon={<AlertTriangle size={24} className="text-amber-400"/>} highlight="amber" />
          <PostureCard title="Critical Investigations" value="2" icon={<Target size={24} className="text-rose-400 animate-pulse"/>} highlight="rose" />
          <PostureCard title="Automated Responses" value="12" icon={<Shield size={24} className="text-emerald-400"/>} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Active Investigations */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                      <h3 className="text-lg font-bold text-slate-200">Active High-Priority Investigations</h3>
                      <span className="text-xs font-bold text-slate-400">AI Correlated Cases</span>
                  </div>
                  <div className="space-y-4">
                      <InvestigationRow title="Suspicious Activity: svc_legacy_deploy" entity="svc_legacy_deploy" priority="CRITICAL" time="14m ago" detections={5} />
                      <InvestigationRow title="Data Exfiltration Behavior: S3 Bucket" entity="arn:aws:s3:::customer-pii-data" priority="HIGH" time="1h ago" detections={3} />
                      <InvestigationRow title="Unauthorized K8s Execution" entity="prod-eks-cluster" priority="HIGH" time="4h ago" detections={2} />
                  </div>
              </CardContent>
          </Card>

          {/* Top Detections */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                      <h3 className="text-lg font-bold text-slate-200">Recent Detections</h3>
                      <span className="text-xs font-bold text-slate-400">Live Stream</span>
                  </div>
                  <div className="space-y-4">
                      <DetectionRow rule="AWS Console Login Without MFA" severity="HIGH" time="2m ago" />
                      <DetectionRow rule="Azure AD: Multiple Failed Logins" severity="MEDIUM" time="14m ago" />
                      <DetectionRow rule="GCP: IAM Policy Granted to Unknown Email" severity="CRITICAL" time="1h ago" />
                      <DetectionRow rule="AWS: EC2 Instance Terminated via API" severity="LOW" time="1h ago" />
                  </div>
              </CardContent>
          </Card>

      </div>
    </div>
  );
}

function PostureCard({ title, value, icon, highlight }: any) {
    let borderClass = 'border-slate-800';
    if (highlight === 'rose') borderClass = 'border-rose-900/50';
    if (highlight === 'amber') borderClass = 'border-amber-900/50';

    return (
        <Card className={`bg-slate-900 ${borderClass}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider leading-tight">{title}</h3>
                    {icon}
                </div>
                <div className="text-4xl font-black text-slate-200">{value}</div>
            </CardContent>
        </Card>
    );
}

function InvestigationRow({ title, entity, priority, time, detections }: any) {
    let priColor = "text-amber-400 bg-amber-950/30 border-amber-900/50";
    if (priority === 'CRITICAL') priColor = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (priority === 'HIGH') priColor = "text-orange-400 bg-orange-950/30 border-orange-900/50";

    return (
        <div className="flex flex-col gap-2 p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <div className="flex justify-between items-start">
                <span className="text-sm font-bold text-slate-300">{title}</span>
                <span className={`text-[10px] font-bold tracking-widest px-2 py-1 rounded border ${priColor}`}>
                    {priority}
                </span>
            </div>
            <div className="flex justify-between text-xs text-slate-500">
                <span className="font-mono text-indigo-400">{entity}</span>
                <span>{detections} Detections • {time}</span>
            </div>
        </div>
    );
}

function DetectionRow({ rule, severity, time }: any) {
    let sevColor = "text-amber-400";
    if (severity === 'CRITICAL') sevColor = "text-rose-400";
    if (severity === 'HIGH') sevColor = "text-orange-400";
    if (severity === 'LOW') sevColor = "text-emerald-400";

    return (
        <div className="flex justify-between items-center p-2 hover:bg-slate-800/50 rounded transition-colors">
            <span className="text-sm text-slate-300 font-bold">{rule}</span>
            <div className="flex gap-4 items-center">
                <span className={`text-xs font-bold ${sevColor}`}>{severity}</span>
                <span className="text-xs text-slate-500">{time}</span>
            </div>
        </div>
    );
}
