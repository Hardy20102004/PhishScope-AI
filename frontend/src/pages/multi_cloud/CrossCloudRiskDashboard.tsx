import React from 'react';
import { Target, Activity, Zap } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function CrossCloudRiskDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Zap className="text-amber-400" />
                    Cross-Cloud Toxic Combinations
                </h2>
                <p className="text-slate-400 mt-1">AI-driven critical path analysis highlighting compounded risk across multiple domains (CSPM + CIEM + DSPM).</p>
            </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div className="lg:col-span-2 space-y-6">
                
                <Card className="bg-slate-900 border-rose-900/50">
                    <CardContent className="p-6">
                        <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                            <h3 className="text-lg font-bold text-slate-200 flex items-center gap-2">
                                <Target className="text-rose-400" /> High-Impact Toxic Combination Detected
                            </h3>
                            <span className="text-[10px] font-black tracking-widest px-2 py-1 rounded border border-rose-900/50 bg-rose-950/30 text-rose-400">CRITICAL RISK PATH</span>
                        </div>
                        
                        <p className="text-slate-400 text-sm leading-relaxed mb-6">
                            The Unified Risk Engine has identified an exponential risk path crossing three domains. An internet-facing AWS EC2 instance containing a critical unpatched vulnerability (CWPP) is attached to an overly permissive IAM role (CIEM) that has read access to an unencrypted S3 bucket containing PII (DSPM).
                        </p>
                        
                        <div className="space-y-4">
                            <h4 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-2">The Attack Path</h4>
                            <PathNode domain="CSPM" title="Publicly Accessible EC2 Instance" asset="i-0abcd1234efgh5678" />
                            <div className="w-1 h-4 bg-rose-900/50 ml-6"></div>
                            <PathNode domain="CWPP" title="Critical CVE-2024-XXXX Present" asset="nginx:1.18.0" />
                            <div className="w-1 h-4 bg-rose-900/50 ml-6"></div>
                            <PathNode domain="CIEM" title="Over-Privileged IAM Role" asset="svc_app_frontend" />
                            <div className="w-1 h-4 bg-rose-900/50 ml-6"></div>
                            <PathNode domain="DSPM" title="Unencrypted PII Data Access" asset="s3://customer-records-prod" />
                        </div>
                    </CardContent>
                </Card>

            </div>

            <div className="space-y-6">
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <Activity className="text-sky-400" />
                            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-widest">Risk Calculation</h3>
                        </div>
                        <p className="text-xs text-slate-400 mb-6">Critical Path Strategy applied. Risk is exponential, not averaged.</p>
                        
                        <div className="space-y-3">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-500">Base Posture Risk:</span>
                                <span className="font-mono text-slate-300">100</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-500">Toxic Combos (14 x 50):</span>
                                <span className="font-mono text-amber-400">+700</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-500">Critical Path Multiplier:</span>
                                <span className="font-mono text-rose-400">x1.5</span>
                            </div>
                            <div className="border-t border-slate-800 pt-2 flex justify-between font-bold">
                                <span className="text-slate-200">Calculated Risk Score:</span>
                                <span className="text-rose-500 text-lg">1000 (MAX)</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

        </div>
    </div>
  );
}

function PathNode({ domain, title, asset }: any) {
    return (
        <div className="flex gap-4 p-3 bg-slate-950/50 rounded border border-rose-900/30 items-center">
            <div className="text-[10px] font-bold text-slate-500 bg-slate-900 border border-slate-800 px-2 py-1 rounded w-16 text-center shrink-0">
                {domain}
            </div>
            <div>
                <div className="text-sm font-bold text-slate-200">{title}</div>
                <div className="text-xs font-mono text-indigo-400 mt-1">{asset}</div>
            </div>
        </div>
    );
}
