import React from 'react';
import { Lock, AlertTriangle, KeySquare } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function EncryptionDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Lock className="text-emerald-400" />
                    Encryption & Key Management Posture
                </h2>
                <p className="text-slate-400 mt-1">Validating at-rest encryption, in-transit protocols, and KMS configuration compliance.</p>
            </div>
            <div className="flex gap-2">
                <Button className="bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700">Export Compliance Report</Button>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-6 flex items-center gap-2">
                        <AlertTriangle className="text-rose-400" /> Unencrypted Data Assets (At Rest)
                    </h3>
                    <div className="space-y-4">
                        <FindingRow name="analytics-staging-db" type="Azure SQL" classification="FINANCIAL" />
                        <FindingRow name="legacy-app-storage-vol" type="AWS EBS" classification="INTERNAL" />
                        <FindingRow name="ml-training-dataset-raw" type="GCP Cloud Storage" classification="PHI" />
                    </div>
                </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-6 flex items-center gap-2">
                        <KeySquare className="text-amber-400" /> Key Management Risks (KMS/CMK)
                    </h3>
                    <div className="space-y-4">
                        <FindingRow name="arn:aws:kms:::key/prod-db-key" type="Customer Managed Key" finding="Key rotation disabled (Last rotated: 2 years ago)" />
                        <FindingRow name="azure-keyvault/marketing-keys" type="Key Vault" finding="Excessive administrative access (12 users)" />
                    </div>
                </CardContent>
            </Card>

        </div>
    </div>
  );
}

function FindingRow({ name, type, classification, finding }: any) {
    return (
        <div className="flex flex-col gap-2 p-4 rounded border bg-slate-950/50 border-slate-800/50">
            <div className="flex justify-between items-start">
                <span className="text-sm font-bold font-mono text-sky-400 truncate max-w-[300px]" title={name}>{name}</span>
                {classification && (
                    <span className={`text-[10px] font-bold tracking-widest px-2 py-0.5 rounded border border-rose-900/50 bg-rose-950/30 text-rose-400`}>
                        {classification}
                    </span>
                )}
            </div>
            <div className="flex flex-col gap-1 mt-1">
                <span className="text-xs text-slate-500 font-bold uppercase tracking-wider">{type}</span>
                {finding && <span className="text-sm text-slate-300">{finding}</span>}
            </div>
        </div>
    );
}
