import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { CheckCircle, ShieldAlert, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ComplianceDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <FileText className="text-emerald-400" />
                    Cloud Compliance Posture
                </h2>
                <p className="text-slate-400 mt-1">Continuous assessment of cloud configurations against major industry benchmarks.</p>
            </div>
            <Button variant="outline" className="bg-slate-900 border-slate-700 text-slate-300">
                Export Audit Report
            </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <ComplianceFrameworkCard 
                framework="CIS AWS Foundations Benchmark v1.4.0"
                score={88}
                passed={42}
                failed={6}
            />

            <ComplianceFrameworkCard 
                framework="NIST Cybersecurity Framework (CSF)"
                score={94}
                passed={85}
                failed={5}
            />

            <ComplianceFrameworkCard 
                framework="SOC 2 (Security & Availability)"
                score={76}
                passed={35}
                failed={11}
                warning={true}
            />

            <ComplianceFrameworkCard 
                framework="ISO/IEC 27001"
                score={100}
                passed={50}
                failed={0}
            />

        </div>
    </div>
  );
}

function ComplianceFrameworkCard({ framework, score, passed, failed, warning = false }: any) {
    let ringColor = "text-emerald-400";
    if (score < 80) ringColor = "text-amber-400";
    if (score < 60) ringColor = "text-rose-400";

    return (
        <Card className={`bg-slate-900 border-slate-800 ${warning ? 'border-amber-900/30' : ''}`}>
            <CardContent className="p-6 flex items-center gap-6">
                
                {/* Radial Score */}
                <div className="relative flex items-center justify-center shrink-0">
                    <svg className="w-24 h-24 transform -rotate-90">
                        <circle cx="48" cy="48" r="40" stroke="currentColor" strokeWidth="6" fill="transparent" className="text-slate-800" />
                        <circle cx="48" cy="48" r="40" stroke="currentColor" strokeWidth="6" fill="transparent" strokeDasharray="251" strokeDashoffset={251 - (251 * score) / 100} className={ringColor} />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                        <span className="text-xl font-black text-slate-100">{score}%</span>
                    </div>
                </div>

                <div className="flex-1">
                    <h3 className="text-lg font-bold text-slate-200 mb-4">{framework}</h3>
                    <div className="flex gap-4">
                        <div className="flex items-center gap-2 bg-emerald-950/20 px-3 py-1.5 rounded border border-emerald-900/30">
                            <CheckCircle size={14} className="text-emerald-400" />
                            <span className="text-sm font-bold text-emerald-400">{passed} Passed</span>
                        </div>
                        <div className={`flex items-center gap-2 ${failed > 0 ? 'bg-rose-950/20 border-rose-900/30' : 'bg-slate-950/50 border-slate-800'} px-3 py-1.5 rounded border`}>
                            <ShieldAlert size={14} className={failed > 0 ? 'text-rose-400' : 'text-slate-600'} />
                            <span className={`text-sm font-bold ${failed > 0 ? 'text-rose-400' : 'text-slate-600'}`}>{failed} Failed</span>
                        </div>
                    </div>
                </div>

            </CardContent>
        </Card>
    );
}
