import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Presentation, Download, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function BoardReportingView() {
  return (
    <div className="p-8 space-y-6 bg-slate-50 min-h-screen text-slate-900 font-sans border-t border-slate-200">
        
        {/* Light theme for presentation/printing readiness */}
        <div className="flex justify-between items-center border-b border-slate-300 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-black flex items-center gap-2 text-slate-800">
                    <Presentation className="text-indigo-600" />
                    Quarterly Board of Directors Report
                </h2>
                <p className="text-slate-500 mt-1">Generated: Q3 FY2026 | Confidential</p>
            </div>
            <Button variant="outline" onClick={() => window.print()} className="bg-white border-slate-300 text-slate-700 gap-2 hover:bg-slate-100">
                <Download size={16} /> Export PDF
            </Button>
        </div>

        <div className="max-w-4xl mx-auto space-y-8 bg-white p-10 rounded-lg shadow-sm border border-slate-200">
            
            <section>
                <h3 className="text-xl font-bold text-slate-800 border-b-2 border-indigo-100 pb-2 mb-4">Executive Summary</h3>
                <p className="text-slate-600 leading-relaxed text-sm">
                    The enterprise security posture remains strong with an overall Resilience Score of <strong className="text-emerald-600">82/100</strong>. 
                    During Q3, the deployment of the Automated SOAR platform successfully reduced Mean Time to Contain (MTTC) by 12%. 
                    However, we are currently tracking an elevated risk profile concerning the <strong>Production Payments API</strong> due to legacy identity controls, which is the primary focus for Q4 remediation.
                </p>
            </section>

            <section className="grid grid-cols-2 gap-8">
                <div>
                    <h3 className="text-lg font-bold text-slate-800 border-b-2 border-indigo-100 pb-2 mb-4">Key Achievements</h3>
                    <ul className="space-y-3">
                        <Achievement text="Zero Trust Phase 1 Completed" />
                        <Achievement text="420 analyst hours saved via AI triage" />
                        <Achievement text="100% compliance with ISO 27001 audit" />
                    </ul>
                </div>
                <div>
                    <h3 className="text-lg font-bold text-slate-800 border-b-2 border-rose-100 pb-2 mb-4">Strategic Risks</h3>
                    <ul className="space-y-3">
                        <Risk text="Legacy API authentication on core payment systems." />
                        <Risk text="Third-party vendor compromise trends increasing globally." />
                    </ul>
                </div>
            </section>

            <section>
                <h3 className="text-xl font-bold text-slate-800 border-b-2 border-indigo-100 pb-2 mb-6">Investment ROI Summary</h3>
                <div className="grid grid-cols-3 gap-4">
                    <ROICard title="Security Automation" stat="420" sub="Hours Saved / Month" color="text-indigo-600" />
                    <ROICard title="EDR Consolidation" stat="15%" sub="Licensing Cost Reduction" color="text-emerald-600" />
                    <ROICard title="Continuous Validation" stat="4x" sub="Faster Gap Detection" color="text-sky-600" />
                </div>
            </section>

        </div>
    </div>
  );
}

function Achievement({ text }: any) {
    return (
        <li className="flex items-start gap-2 text-sm text-slate-600">
            <CheckCircle2 size={18} className="text-emerald-500 mt-0.5 flex-shrink-0" />
            {text}
        </li>
    );
}

function Risk({ text }: any) {
    return (
        <li className="flex items-start gap-2 text-sm text-slate-600">
            <span className="w-2 h-2 rounded-full bg-rose-500 mt-1.5 flex-shrink-0"></span>
            {text}
        </li>
    );
}

function ROICard({ title, stat, sub, color }: any) {
    return (
        <div className="bg-slate-50 border border-slate-200 p-4 rounded text-center">
            <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">{title}</div>
            <div className={`text-3xl font-black ${color} mb-1`}>{stat}</div>
            <div className="text-[10px] font-bold text-slate-400 uppercase">{sub}</div>
        </div>
    );
}
