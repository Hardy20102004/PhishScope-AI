import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { LineChart, DollarSign, Clock } from 'lucide-react';

export default function InvestmentAnalytics() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <LineChart className="text-emerald-400" />
                Security Investment ROI Analytics
            </h2>
            <p className="text-slate-400 mt-1">Measuring the operational efficiency and risk reduction yielded by strategic initiatives.</p>
        </div>

        <div className="space-y-6">
            
            <InvestmentCard 
                initiative="AI SOC Copilot & SOAR Automation"
                status="ACTIVE"
                hoursSaved={420}
                riskReduction={15}
                description="Deployment of Tier-1 alert triage automation and AI-assisted investigation workflows."
            />

            <InvestmentCard 
                initiative="Zero Trust Network Access (ZTNA)"
                status="ACTIVE"
                hoursSaved={80}
                riskReduction={32}
                description="Migration from legacy VPNs to identity-aware proxies, drastically reducing lateral movement potential."
            />

            <InvestmentCard 
                initiative="Continuous Security Validation (BAS)"
                status="COMPLETED"
                hoursSaved={120}
                riskReduction={22}
                description="Automated red teaming replaced quarterly manual pen-tests, providing continuous coverage."
            />

        </div>
    </div>
  );
}

function InvestmentCard({ initiative, status, hoursSaved, riskReduction, description }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded border border-indigo-900/50 bg-indigo-950/30 text-indigo-400">
                            {status}
                        </span>
                        <h3 className="text-lg font-bold text-slate-200">{initiative}</h3>
                    </div>
                    <p className="text-sm text-slate-400">{description}</p>
                </div>

                <div className="flex gap-8">
                    <div className="flex flex-col items-center">
                        <div className="flex items-center gap-1 text-slate-500 mb-1">
                            <Clock size={14} /> <span className="text-xs font-bold uppercase">Efficiency</span>
                        </div>
                        <div className="text-2xl font-black text-emerald-400">+{hoursSaved}h <span className="text-xs text-slate-500 font-normal">/mo</span></div>
                    </div>
                    
                    <div className="flex flex-col items-center">
                        <div className="flex items-center gap-1 text-slate-500 mb-1">
                            <DollarSign size={14} /> <span className="text-xs font-bold uppercase">Risk Reduction</span>
                        </div>
                        <div className="text-2xl font-black text-sky-400">{riskReduction}%</div>
                    </div>
                </div>

            </CardContent>
        </Card>
    );
}
