import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Cloud, UploadCloud, Box, ShieldAlert, Key } from 'lucide-react';

export default function CloudDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-cyan-400">
            <Cloud size={32} />
            Cloud & Container Forensics
          </h1>
          <p className="text-slate-400 mt-2">Analyze IAM audit logs (CloudTrail) and Docker/Kubernetes container configurations for misconfigurations and compromise.</p>
        </div>
        <Button className="bg-cyan-600 hover:bg-cyan-700 text-white shadow-lg shadow-cyan-500/20 gap-2">
            <UploadCloud size={18} /> Import Cloud Evidence
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <EnvCard 
              name="AWS Prod Account" 
              provider="AWS" 
              account="123456789012" 
              status="IAM ANOMALY"
              auditCount={14500}
              containerCount={12}
              isCompromised={true}
          />
          <EnvCard 
              name="K8s Staging Cluster" 
              provider="Kubernetes" 
              account="arn:aws:eks:cluster/staging" 
              status="ANALYZED"
              auditCount={890}
              containerCount={45}
              isCompromised={false}
          />
      </div>
    </div>
  );
}

function EnvCard({ name, provider, account, status, auditCount, containerCount, isCompromised }: any) {
    
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${isCompromised ? 'border-t-4 border-t-rose-500' : 'border-t-4 border-t-cyan-500'}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                        <Cloud size={20} className="text-slate-400" />
                        <h3 className="text-lg font-bold text-slate-200 truncate" title={name}>{name}</h3>
                    </div>
                </div>
                
                <div className="space-y-3 mb-6 font-mono text-sm">
                    <div className="flex justify-between">
                        <span className="text-slate-500">Provider</span>
                        <span className="text-slate-300">{provider}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">Account/Cluster</span>
                        <span className="text-slate-300">{account}</span>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2 mb-6">
                    <div className="bg-slate-950 p-2 rounded border border-slate-800 flex items-center gap-2">
                        <Key size={14} className="text-cyan-400" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-slate-500 uppercase font-bold">Audit Events</span>
                            <span className="text-xs font-mono text-slate-300">{auditCount.toLocaleString()}</span>
                        </div>
                    </div>
                    <div className="bg-slate-950 p-2 rounded border border-slate-800 flex items-center gap-2">
                        <Box size={14} className="text-emerald-400" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-slate-500 uppercase font-bold">Containers</span>
                            <span className="text-xs font-mono text-slate-300">{containerCount}</span>
                        </div>
                    </div>
                </div>

                <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                    <span className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded ${isCompromised ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}`}>
                        {isCompromised && <ShieldAlert size={12} />}
                        {status}
                    </span>
                    <Button variant="outline" className="text-xs h-8 border-slate-700 bg-slate-800 hover:bg-slate-700">Explore Artifacts</Button>
                </div>
            </CardContent>
        </Card>
    );
}
