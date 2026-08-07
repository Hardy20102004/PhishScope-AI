import React from 'react';
import { ShieldCheck } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ComplianceDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <ShieldCheck className="text-emerald-400" />
                    Unified Compliance Analytics
                </h2>
                <p className="text-slate-400 mt-1">Aggregated framework alignment mapping across AWS, Azure, GCP, and Kubernetes.</p>
            </div>
            <div className="flex gap-2">
                <Button className="bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700">Export Auditor Report</Button>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FrameworkCard name="NIST Cybersecurity Framework" score={82} passed={210} failed={42} />
            <FrameworkCard name="CIS Multi-Cloud Benchmarks" score={75} passed={450} failed={150} />
            <FrameworkCard name="ISO/IEC 27001" score={91} passed={105} failed={10} />
        </div>
    </div>
  );
}

function FrameworkCard({ name, score, passed, failed }: any) {
    let colorClass = "text-emerald-400";
    let bgClass = "bg-emerald-500";
    if (score < 80) { colorClass = "text-amber-400"; bgClass = "bg-amber-500"; }
    if (score < 60) { colorClass = "text-rose-400"; bgClass = "bg-rose-500"; }

    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6">
                <h3 className="text-lg font-bold text-slate-200 mb-6 flex items-center gap-2 h-14">
                    {name}
                </h3>
                
                <div className="flex items-end gap-2 mb-6 border-b border-slate-800 pb-4">
                    <div className={`text-5xl font-black ${colorClass}`}>{score}%</div>
                    <div className="text-sm font-bold text-slate-500 mb-1">Alignment</div>
                </div>

                <div className="space-y-4 mb-4">
                    <div className="flex flex-col gap-1">
                        <div className="flex justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
                            <span>Passed Controls</span>
                            <span>{passed}</span>
                        </div>
                        <div className="w-full bg-slate-800 rounded-full h-1.5">
                            <div className={`h-1.5 rounded-full ${bgClass}`} style={{ width: `${(passed/(passed+failed))*100}%` }}></div>
                        </div>
                    </div>

                    <div className="flex flex-col gap-1">
                        <div className="flex justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
                            <span>Failed Controls</span>
                            <span className="text-rose-400">{failed}</span>
                        </div>
                        <div className="w-full bg-slate-800 rounded-full h-1.5">
                            <div className={`h-1.5 rounded-full bg-rose-500`} style={{ width: `${(failed/(passed+failed))*100}%` }}></div>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
