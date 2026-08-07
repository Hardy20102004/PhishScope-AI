import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Bomb, Database, Server, Users } from 'lucide-react';

export default function BlastRadiusViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Bomb className="text-orange-500" />
                Blast Radius Estimation
            </h2>
            <p className="text-slate-400 mt-1">Calculates the downstream compromise potential if a specific node is breached.</p>
        </div>

        {/* Selected Node Profile */}
        <Card className="bg-slate-900 border-orange-900/30 mb-8">
            <CardContent className="p-6 flex items-center gap-6">
                <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-slate-700 flex items-center justify-center text-slate-400">
                    <Users size={32} />
                </div>
                <div>
                    <h3 className="text-[10px] font-bold text-orange-500 uppercase tracking-wider">Simulated Compromised Node</h3>
                    <div className="text-2xl font-black text-slate-200">ServiceAccount_Backup</div>
                    <div className="text-xs text-slate-500 mt-1 font-mono">ID: SA-9912-AWS | Type: CLOUD_IAM_ROLE</div>
                </div>
            </CardContent>
        </Card>

        <h3 className="text-lg font-bold text-slate-200 mb-4">Estimated Downstream Impact</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <div className="flex items-center gap-2 mb-4 text-emerald-400">
                        <Database size={20} />
                        <h4 className="font-bold">Databases</h4>
                    </div>
                    <div className="text-4xl font-black text-slate-200 mb-2">14</div>
                    <p className="text-xs text-slate-500">Accessible via backup snapshot privileges across 3 VPCs.</p>
                </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <div className="flex items-center gap-2 mb-4 text-sky-400">
                        <Server size={20} />
                        <h4 className="font-bold">EC2 Instances</h4>
                    </div>
                    <div className="text-4xl font-black text-slate-200 mb-2">142</div>
                    <p className="text-xs text-slate-500">Instances running with instance profiles trusting this role.</p>
                </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-800 border-rose-900/50">
                <CardContent className="p-6">
                    <div className="flex items-center gap-2 mb-4 text-rose-500">
                        <Bomb size={20} />
                        <h4 className="font-bold">Critical Assets</h4>
                    </div>
                    <div className="text-4xl font-black text-rose-400 mb-2">2</div>
                    <p className="text-xs text-slate-500 font-mono text-rose-500/70">
                        - Customer_PII_Cluster<br/>
                        - Core_Financial_Ledger
                    </p>
                </CardContent>
            </Card>

        </div>
    </div>
  );
}
