import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ClipboardCheck, Fingerprint, Clock, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function GovernanceDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <ClipboardCheck className="text-emerald-400" />
                    Identity Governance & Access Reviews
                </h2>
                <p className="text-slate-400 mt-1">Periodic certification campaigns to enforce Zero Trust continuous validation.</p>
            </div>
            <div className="flex gap-2">
                <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">Create New Campaign</Button>
            </div>
        </div>

        {/* Active Campaigns */}
        <div className="space-y-6">
            <h3 className="text-lg font-bold text-slate-200 flex items-center gap-2">
                <Clock className="text-amber-400" /> Pending Reviews (Q3 Cloud Admin Certification)
            </h3>
            
            <ReviewCard 
                identity="bob.williams@corp.com" 
                role="AWS Organization Admin" 
                lastLogin="2 hours ago"
                usage="High (142 API calls/day)" 
                status="pending"
            />
            
            <ReviewCard 
                identity="svc_automation_bot" 
                role="GCP Project Owner" 
                lastLogin="Never (Key Last Used: 124 days ago)"
                usage="Zero" 
                status="critical"
            />

        </div>
    </div>
  );
}

function ReviewCard({ identity, role, lastLogin, usage, status }: any) {
    let alertBorder = "border-slate-800";
    if (status === 'critical') alertBorder = "border-rose-900/50 bg-rose-950/10";

    return (
        <Card className={`bg-slate-900 ${alertBorder}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-center">
                    <div>
                        <h4 className="text-lg font-bold text-slate-200 flex items-center gap-2 mb-2">
                            <Fingerprint size={18} className="text-emerald-400" /> {identity}
                        </h4>
                        <div className="flex gap-6 text-sm text-slate-400">
                            <div><strong className="text-slate-300">Entitlement:</strong> {role}</div>
                            <div><strong className="text-slate-300">Last Login:</strong> <span className={status === 'critical' ? 'text-rose-400 font-bold' : ''}>{lastLogin}</span></div>
                            <div><strong className="text-slate-300">Usage:</strong> {usage}</div>
                        </div>
                    </div>
                    
                    <div className="flex gap-2 flex-col md:flex-row">
                        <Button className="bg-emerald-600 hover:bg-emerald-700 text-white px-8">
                            <Check size={16} className="mr-2" /> Certify Access
                        </Button>
                        <Button className="bg-rose-600 hover:bg-rose-700 text-white px-8">
                            <X size={16} className="mr-2" /> Revoke Access
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
