import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Sparkles, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function RecommendationWorkspace() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Sparkles className="text-fuchsia-400" />
                Strategic AI Recommendations (Approval Gate)
            </h2>
            <p className="text-slate-400 mt-1">Review, adjust, and approve AI-generated strategic optimizations before they are added to the roadmap.</p>
        </div>

        <div className="space-y-6">
            
            <ApprovalCard 
                title="Consolidate EDR Tooling to Unified XDR"
                description="Detection gap analysis indicates significant overlap between legacy EDR agents. The AI advisor recommends consolidating to a single XDR platform to reduce endpoint overhead and licensing costs."
                impact="Estimated $450k/yr savings. 15% increase in cross-telemetry detection fidelity."
            />

            <ApprovalCard 
                title="Deprecate Legacy VPN Infrastructure"
                description="Attack path simulations continually highlight the legacy VPN concentrators as a primary ingress point for ransomware actors. The AI advisor recommends accelerating the ZTNA rollout to deprecate the VPNs."
                impact="Eliminates 3 critical attack paths. Reduces external attack surface by 40%."
            />

        </div>
    </div>
  );
}

function ApprovalCard({ title, description, impact }: any) {
    return (
        <Card className="bg-slate-900 border-fuchsia-900/30 hover:border-fuchsia-500/50 transition-colors">
            <CardContent className="p-6">
                <div className="flex items-start justify-between gap-6">
                    
                    <div className="flex-1">
                        <div className="flex items-center gap-2 mb-3">
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded border border-amber-900/50 bg-amber-950/30 text-amber-400">
                                PENDING REVIEW
                            </span>
                            <h3 className="text-xl font-bold text-slate-200">{title}</h3>
                        </div>
                        <p className="text-sm text-slate-400 mb-4 leading-relaxed">{description}</p>
                        
                        <div className="bg-slate-950 p-3 rounded border border-slate-800">
                            <span className="text-xs font-bold text-slate-500 uppercase mr-2">Expected Impact:</span>
                            <span className="text-sm text-emerald-400 font-medium">{impact}</span>
                        </div>
                    </div>

                    <div className="flex flex-col gap-3 min-w-[140px] pt-8">
                        <Button className="bg-emerald-600 hover:bg-emerald-700 text-white gap-2 justify-start">
                            <Check size={16} /> Approve
                        </Button>
                        <Button variant="outline" className="border-rose-900/50 text-rose-400 hover:bg-rose-950/30 gap-2 justify-start">
                            <X size={16} /> Reject
                        </Button>
                    </div>

                </div>
            </CardContent>
        </Card>
    );
}
