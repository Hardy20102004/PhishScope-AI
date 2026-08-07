import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Wrench, ArrowDown, Network } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function RemediationWorkspace() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Wrench className="text-emerald-400" />
                Remediation & Choke Point Prioritization
            </h2>
            <p className="text-slate-400 mt-1">Identified graph edges that, if removed or secured, sever the highest number of viable attack paths.</p>
        </div>

        <div className="space-y-4">
            
            <ChokePointCard 
                rank={1}
                action="Remove local admin rights for 'HelpDesk_Tier1' group on Engineering Workstations."
                edge="HelpDesk_Tier1 → CAN_ADMINISTER → Eng_Workstations"
                pathsSevered={412}
                impact="HIGH"
            />
            
            <ChokePointCard 
                rank={2}
                action="Enforce MFA for RDP access to the DMZ Jump Host."
                edge="Any_User → CAN_RDP → JUMP_HOST_01"
                pathsSevered={288}
                impact="HIGH"
            />

            <ChokePointCard 
                rank={3}
                action="Revoke overly permissive S3 read access from legacy Jenkins IAM role."
                edge="Jenkins_Role → CAN_READ → S3_Prod_Configs"
                pathsSevered={94}
                impact="MEDIUM"
            />

        </div>
    </div>
  );
}

function ChokePointCard({ rank, action, edge, pathsSevered, impact }: any) {
    let impactColor = "text-sky-400 border-sky-900/50 bg-sky-950/10";
    if (impact === 'HIGH') impactColor = "text-rose-400 border-rose-900/50 bg-rose-950/10";
    if (impact === 'MEDIUM') impactColor = "text-amber-400 border-amber-900/50 bg-amber-950/10";

    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-emerald-900/50 transition-colors group">
            <CardContent className="p-6 flex items-start gap-6">
                
                <div className="flex-shrink-0 w-12 h-12 rounded bg-slate-800 flex items-center justify-center font-black text-xl text-slate-500 group-hover:text-emerald-400 transition-colors">
                    #{rank}
                </div>
                
                <div className="flex-grow">
                    <h3 className="text-lg font-bold text-slate-200 mb-2">{action}</h3>
                    <div className="flex items-center gap-2 text-xs font-mono text-slate-500 mb-4 bg-slate-950 px-3 py-2 rounded w-fit border border-slate-800">
                        <Network size={14} className="text-fuchsia-400" />
                        Target Edge: <span className="text-slate-300">{edge}</span>
                    </div>
                </div>

                <div className="flex-shrink-0 flex flex-col items-end gap-3 min-w-[150px]">
                    <div className={`text-[10px] font-bold px-2 py-1 rounded border ${impactColor}`}>
                        {impact} RISK REDUCTION
                    </div>
                    <div className="flex items-center gap-1 text-emerald-400 font-bold">
                        <ArrowDown size={16} /> {pathsSevered} Paths Severed
                    </div>
                    <Button variant="outline" className="w-full text-xs h-8 bg-slate-950 border-slate-700 text-slate-300 mt-2">
                        Create Ticket
                    </Button>
                </div>

            </CardContent>
        </Card>
    );
}
