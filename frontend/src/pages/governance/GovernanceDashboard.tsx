import React from 'react';
import { Activity, ShieldCheck, GitCommit } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function GovernanceDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Activity className="text-emerald-400" />
                    Executive Governance Overview
                </h2>
                <p className="text-slate-400 mt-1">High-level metrics on policy compliance, workflow throughput, and automation health.</p>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-2 flex items-center gap-2">
                        <ShieldCheck className="text-emerald-400" /> Active Security Policies
                    </h3>
                    <div className="text-4xl font-black text-slate-100 mb-2">45</div>
                    <p className="text-xs text-slate-500">1205 compliant assets, 12 non-compliant.</p>
                </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-2 flex items-center gap-2">
                        <GitCommit className="text-sky-400" /> Automation Throughput (30d)
                    </h3>
                    <div className="text-4xl font-black text-slate-100 mb-2">1,204</div>
                    <p className="text-xs text-slate-500">Workflows executed successfully.</p>
                </CardContent>
            </Card>
            
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-2 flex items-center gap-2">
                        <Activity className="text-fuchsia-400" /> Avg. Approval Latency
                    </h3>
                    <div className="text-4xl font-black text-slate-100 mb-2">18m</div>
                    <p className="text-xs text-slate-500">Average time to reach L3 approval.</p>
                </CardContent>
            </Card>

        </div>
    </div>
  );
}
