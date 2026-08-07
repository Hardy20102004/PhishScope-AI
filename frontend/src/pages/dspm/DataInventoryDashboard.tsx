import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Database, Cloud, ShieldCheck, Activity } from 'lucide-react';

export default function DataInventoryDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-cyan-400">
            <Database size={32} />
            Data Security Posture Management (DSPM)
          </h1>
          <p className="text-slate-400 mt-2">Continuous discovery, classification, and exposure analysis for cloud data assets.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-cyan-600 hover:bg-cyan-700 text-white shadow-lg shadow-cyan-500/20 gap-2">
                <Activity size={18} /> Trigger Discovery Scan
            </Button>
        </div>
      </div>

      {/* Top Posture Area */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <PostureCard title="Total Data Assets" value="1,842" icon={<Database size={24} className="text-slate-400"/>} />
          <PostureCard title="Sensitive Assets (PII/PHI)" value="341" icon={<ShieldCheck size={24} className="text-amber-400"/>} highlight="amber" />
          <PostureCard title="Publicly Exposed" value="12" icon={<Cloud size={24} className="text-rose-400 animate-pulse"/>} highlight="rose" />
          <PostureCard title="Encrypted at Rest" value="98%" icon={<ShieldCheck size={24} className="text-emerald-400"/>} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Assets by Provider */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Assets by Cloud Provider</h3>
                  <div className="space-y-4">
                      <AssetRow provider="AWS (S3, RDS, DynamoDB)" count={1145} percent={62} color="bg-amber-500" />
                      <AssetRow provider="Azure (Blob, SQL, CosmosDB)" count={420} percent={23} color="bg-blue-500" />
                      <AssetRow provider="GCP (GCS, CloudSQL, BigQuery)" count={277} percent={15} color="bg-rose-500" />
                  </div>
              </CardContent>
          </Card>

          {/* Highest Risk Assets */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                      <h3 className="text-lg font-bold text-slate-200">Highest Risk Data Assets</h3>
                      <span className="text-xs font-bold text-slate-400">Requires Remediation</span>
                  </div>
                  <div className="space-y-4">
                      <RiskRow name="prod-customer-backups-2026" type="AWS S3" risk="CRITICAL" issues={["Public Read", "Contains PII"]} />
                      <RiskRow name="analytics-staging-db" type="Azure SQL" risk="HIGH" issues={["Unencrypted", "Dormant 90 Days"]} />
                      <RiskRow name="marketing-campaign-data" type="GCP BigQuery" risk="MEDIUM" issues={["Excessive Cross-Account Access"]} />
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

function AssetRow({ provider, count, percent, color }: any) {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm font-bold text-slate-300">
                <span>{provider}</span>
                <span className="text-slate-500">{count} Assets</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
                <div className={`h-2 rounded-full ${color}`} style={{ width: `${percent}%` }}></div>
            </div>
        </div>
    );
}

function RiskRow({ name, type, risk, issues }: any) {
    let riskColor = "text-amber-400 bg-amber-950/30 border-amber-900/50";
    if (risk === 'CRITICAL') riskColor = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (risk === 'HIGH') riskColor = "text-orange-400 bg-orange-950/30 border-orange-900/50";

    return (
        <div className="flex flex-col gap-2 p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <div className="flex justify-between items-start">
                <span className="text-sm font-bold text-slate-300">{name} <span className="text-xs text-slate-500 ml-2 font-normal">({type})</span></span>
                <span className={`text-[10px] font-bold tracking-widest px-2 py-1 rounded border ${riskColor}`}>
                    {risk}
                </span>
            </div>
            <div className="flex gap-2 mt-1">
                {issues.map((i: str, idx: number) => (
                    <span key={idx} className="text-xs text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-800">{i}</span>
                ))}
            </div>
        </div>
    );
}
