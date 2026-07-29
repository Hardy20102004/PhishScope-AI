import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ShieldAlert, Trash2, ShieldMinus } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function LeastPrivilegeDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <ShieldMinus className="text-amber-400" />
                    Least Privilege Optimization
                </h2>
                <p className="text-slate-400 mt-1">AI-driven identification of dormant accounts, unused entitlements, and over-privileged identities.</p>
            </div>
            <div className="flex gap-2">
                <Button className="bg-amber-600 hover:bg-amber-700 text-white">Generate Remediation Script</Button>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Dormant Accounts */}
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-6 flex items-center gap-2">
                        <ShieldAlert className="text-rose-400" /> High-Risk Dormant Identities
                    </h3>
                    <div className="space-y-4">
                        <OptimizationRow name="svc_legacy_deploy" reason="120 Days Dormant + AdministratorAccess" action="Revoke Access" />
                        <OptimizationRow name="temp-contractor-01" reason="85 Days Dormant + Database Write Access" action="Suspend Account" />
                        <OptimizationRow name="db_migration_role" reason="Never Used (Created 60 days ago)" action="Delete Role" />
                    </div>
                </CardContent>
            </Card>

            {/* Over-Privileged Accounts */}
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-6 flex items-center gap-2">
                        <ShieldAlert className="text-amber-400" /> Unused Entitlements (Over-Privileged)
                    </h3>
                    <div className="space-y-4">
                        <OptimizationRow name="dev-team-lead-role" reason="Granted S3FullAccess, only uses s3:GetObject" action="Right-Size Policy" type="warning" />
                        <OptimizationRow name="analytics-engine-sa" reason="Granted IAM:PassRole, never invoked in 90 days" action="Right-Size Policy" type="warning" />
                        <OptimizationRow name="marketing-group" reason="Granted EC2:TerminateInstances, out of business scope" action="Remove Permission" type="warning" />
                    </div>
                </CardContent>
            </Card>

        </div>
    </div>
  );
}

function OptimizationRow({ name, reason, action, type = "critical" }: any) {
    let bgStyle = "bg-rose-950/20 border-rose-900/30";
    let nameStyle = "text-rose-400";
    if (type === 'warning') {
        bgStyle = "bg-amber-950/20 border-amber-900/30";
        nameStyle = "text-amber-400";
    }

    return (
        <div className={`flex justify-between items-center p-4 rounded border ${bgStyle}`}>
            <div className="flex flex-col gap-1">
                <span className={`text-sm font-bold font-mono ${nameStyle}`}>{name}</span>
                <span className="text-xs text-slate-400">{reason}</span>
            </div>
            <Button variant="outline" size="sm" className="border-slate-700 text-slate-300 hover:bg-slate-800">
                <Trash2 size={14} className="mr-2" /> {action}
            </Button>
        </div>
    );
}
