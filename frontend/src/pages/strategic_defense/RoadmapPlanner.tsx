import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Map, Calendar } from 'lucide-react';

export default function RoadmapPlanner() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Map className="text-blue-400" />
                    Strategic Optimization Roadmap
                </h2>
                <p className="text-slate-400 mt-1">Multi-year security transformation plan aligned with NIST CSF core functions.</p>
            </div>
            <div className="flex items-center gap-2 text-slate-400 bg-slate-900 px-4 py-2 rounded border border-slate-800">
                <Calendar size={16} /> <span className="text-sm font-bold">FY26 - FY27</span>
            </div>
        </div>

        <div className="space-y-4">
            <NistSection func="IDENTIFY" color="border-blue-500">
                <RoadmapItem title="Enterprise Asset Knowledge Graph Expansion" timeframe="Q1 FY26 - Q2 FY26" status="IN PROGRESS" />
                <RoadmapItem title="Third-Party Vendor Risk Integration" timeframe="Q3 FY26" status="PLANNED" />
            </NistSection>

            <NistSection func="PROTECT" color="border-purple-500">
                <RoadmapItem title="Zero Trust Identity Migration" timeframe="Q1 FY26 - Q4 FY26" status="IN PROGRESS" />
                <RoadmapItem title="Deprecate Legacy VPNs" timeframe="Q4 FY26" status="PLANNED" />
                <RoadmapItem title="Cloud Native Application Protection (CNAPP)" timeframe="Q1 FY27" status="PLANNED" />
            </NistSection>

            <NistSection func="DETECT" color="border-amber-500">
                <RoadmapItem title="Continuous BAS Validation Deployment" timeframe="Q4 FY25" status="COMPLETED" />
                <RoadmapItem title="Consolidate EDR and NDR Telemetry" timeframe="Q2 FY26" status="IN PROGRESS" />
            </NistSection>
            
            <NistSection func="RESPOND & RECOVER" color="border-rose-500">
                <RoadmapItem title="Autonomous AI SOC Triage" timeframe="Q1 FY26" status="COMPLETED" />
                <RoadmapItem title="Automated Ransomware Containment Playbooks" timeframe="Q3 FY26" status="PLANNED" />
            </NistSection>
        </div>

    </div>
  );
}

function NistSection({ func, color, children }: any) {
    return (
        <Card className={`bg-slate-900 border-slate-800 border-l-4 ${color}`}>
            <CardContent className="p-6">
                <h3 className="text-lg font-black text-slate-200 mb-4 tracking-widest">{func}</h3>
                <div className="space-y-2">
                    {children}
                </div>
            </CardContent>
        </Card>
    );
}

function RoadmapItem({ title, timeframe, status }: any) {
    let statusStyle = "text-slate-400 border-slate-700 bg-slate-800";
    if (status === 'IN PROGRESS') statusStyle = "text-cyan-400 border-cyan-900 bg-cyan-950/50";
    if (status === 'COMPLETED') statusStyle = "text-emerald-400 border-emerald-900 bg-emerald-950/50";

    return (
        <div className="flex justify-between items-center bg-slate-950/50 p-3 rounded border border-slate-800/50">
            <div>
                <div className="text-sm font-bold text-slate-200">{title}</div>
                <div className="text-xs text-slate-500 mt-1">{timeframe}</div>
            </div>
            <div className={`text-[10px] font-black tracking-widest px-2 py-1 rounded border ${statusStyle}`}>
                {status}
            </div>
        </div>
    );
}
