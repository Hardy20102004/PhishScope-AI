import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Users, Clock, FileText } from 'lucide-react';

export default function AnalystReadinessDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Users className="text-sky-400" />
                SOC Analyst Readiness
            </h2>
            <p className="text-slate-400 mt-1">Aggregated operational efficiency and playbook adherence metrics by tier.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <TeamCard 
                name="SOC Tier 1 (Triage)" 
                mtt="8 mins" 
                mttr="45 mins" 
                adherence={92}
            />
            <TeamCard 
                name="SOC Tier 2 (Investigation)" 
                mtt="N/A" 
                mttr="4 hrs" 
                adherence={85}
            />
            <TeamCard 
                name="DFIR Team" 
                mtt="N/A" 
                mttr="72 hrs" 
                adherence={98}
            />
        </div>
    </div>
  );
}

function TeamCard({ name, mtt, mttr, adherence }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6">
                <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">{name}</h3>
                
                <div className="space-y-4 font-mono text-xs">
                    <div className="flex justify-between items-center">
                        <span className="text-slate-500 flex items-center gap-2"><Clock size={14}/> Mean Time to Triage</span>
                        <span className="text-sky-400 font-bold text-sm">{mtt}</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-slate-500 flex items-center gap-2"><Clock size={14}/> Mean Time to Resolve</span>
                        <span className="text-sky-400 font-bold text-sm">{mttr}</span>
                    </div>
                    <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                        <span className="text-slate-500 flex items-center gap-2"><FileText size={14}/> Playbook Adherence</span>
                        <span className="text-emerald-400 font-bold text-sm">{adherence}%</span>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
