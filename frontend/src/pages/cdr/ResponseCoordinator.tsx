import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Shield, PlayCircle, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ResponseCoordinator() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <PlayCircle className="text-emerald-400" />
                    Response Coordination Playbooks
                </h2>
                <p className="text-slate-400 mt-1">AI-generated containment actions for active investigations. Requires human approval.</p>
            </div>
        </div>

        <div className="grid grid-cols-1 gap-6">
            
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <div className="flex justify-between items-start mb-6 border-b border-slate-800 pb-4">
                        <div>
                            <h3 className="text-lg font-bold text-slate-200 flex items-center gap-2">
                                <Shield className="text-emerald-400" /> Containment Playbook: Compromised Identity
                            </h3>
                            <p className="text-sm text-slate-400 mt-1">Target: <span className="font-mono text-indigo-400">svc_legacy_deploy</span> (Investigation: Suspicious Activity)</p>
                        </div>
                        <span className="text-xs font-bold text-amber-400 bg-amber-950/30 px-3 py-1 rounded border border-amber-900/50">PENDING APPROVAL</span>
                    </div>
                    
                    <div className="space-y-4 mb-6">
                        <ActionRow action="REVOKE_IAM_SESSIONS" description="Revoke all active STS sessions for the compromised role." />
                        <ActionRow action="ATTACH_DENY_ALL_POLICY" description="Attach a managed DenyAll policy to prevent further API calls." />
                        <ActionRow action="ISOLATE_K8S_POD" description="Apply a NetworkPolicy to isolate the spawned pod in prod-eks-us-east." />
                    </div>

                    <div className="flex gap-4 justify-end border-t border-slate-800 pt-4">
                        <Button variant="outline" className="border-rose-900 text-rose-400 hover:bg-rose-950">
                            <X size={16} className="mr-2" /> Reject Playbook
                        </Button>
                        <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
                            <Check size={16} className="mr-2" /> Approve & Execute
                        </Button>
                    </div>
                </CardContent>
            </Card>

        </div>
    </div>
  );
}

function ActionRow({ action, description }: any) {
    return (
        <div className="flex items-start gap-4 p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <div className="text-xs font-bold text-sky-400 bg-sky-950/30 border border-sky-900/50 px-2 py-1 rounded w-48 shrink-0 text-center">
                {action}
            </div>
            <div className="text-sm text-slate-300 pt-0.5">
                {description}
            </div>
        </div>
    );
}
