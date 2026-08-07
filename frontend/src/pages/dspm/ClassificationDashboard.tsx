import React from 'react';
import { Fingerprint, AlertCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function ClassificationDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Fingerprint className="text-fuchsia-400" />
                    Data Sensitivity & Classification
                </h2>
                <p className="text-slate-400 mt-1">AI-driven identification of PII, PHI, Financial, and proprietary Intellectual Property.</p>
            </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div className="lg:col-span-2 space-y-6">
                
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Classification Distribution</h3>
                        
                        <div className="space-y-4">
                            <ClassificationRow label="PII (Personal Identifiable Information)" count={142} confidence="98%" severity="HIGH" />
                            <ClassificationRow label="PHI (Personal Health Information)" count={24} confidence="99%" severity="CRITICAL" />
                            <ClassificationRow label="PCI / Financial Data" count={58} confidence="95%" severity="CRITICAL" />
                            <ClassificationRow label="Internal / Proprietary" count={642} confidence="88%" severity="MEDIUM" />
                            <ClassificationRow label="Public / Unclassified" count={976} confidence="100%" severity="LOW" />
                        </div>
                    </CardContent>
                </Card>

            </div>

            <div className="space-y-6">
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <AlertCircle className="text-amber-400" />
                            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-widest">Pending Human Review</h3>
                        </div>
                        <p className="text-xs text-slate-400 mb-6">The AI Context Engine flagged the following unstructured assets with low classification confidence (&lt; 80%).</p>
                        
                        <div className="space-y-3">
                            <ReviewNode asset="s3://research-notes-2026/drafts" suspected="Intellectual Property" confidence="72%" />
                            <ReviewNode asset="azure-blob/hr-temp-uploads" suspected="PII" confidence="68%" />
                            <ReviewNode asset="gcs://ml-training-dataset-raw" suspected="PHI" confidence="75%" />
                        </div>
                    </CardContent>
                </Card>
            </div>

        </div>
    </div>
  );
}

function ClassificationRow({ label, count, confidence, severity }: any) {
    let sevColor = "text-emerald-400";
    if (severity === 'CRITICAL') sevColor = "text-rose-400";
    if (severity === 'HIGH') sevColor = "text-amber-400";
    if (severity === 'MEDIUM') sevColor = "text-blue-400";

    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <span className="text-sm font-bold text-slate-300">{label}</span>
            <div className="flex items-center gap-6">
                <span className="text-xs text-slate-500">Confidence: <span className="font-mono text-slate-300">{confidence}</span></span>
                <span className="text-xs font-bold text-slate-400 w-24 text-right">{count} Assets</span>
                <span className={`text-[10px] font-bold tracking-widest px-2 py-1 rounded border border-slate-700 w-24 text-center ${sevColor}`}>
                    {severity}
                </span>
            </div>
        </div>
    );
}

function ReviewNode({ asset, suspected, confidence }: any) {
    return (
        <div className="flex flex-col gap-1 bg-slate-950 p-3 rounded border border-slate-800 hover:border-slate-600 transition-colors cursor-pointer">
            <div className="text-xs font-mono text-indigo-400 truncate" title={asset}>{asset}</div>
            <div className="flex justify-between items-center mt-1">
                <div className="text-xs text-slate-400">Suspected: <span className="text-slate-200 font-bold">{suspected}</span></div>
                <div className="text-xs text-amber-500 font-mono">{confidence}</div>
            </div>
        </div>
    );
}
