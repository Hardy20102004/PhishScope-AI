import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Crosshair, Plus, Shield, Activity, Target } from 'lucide-react';

export default function CampaignDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-rose-500">
            <Crosshair size={32} />
            Red Team Campaign Management
          </h1>
          <p className="text-slate-400 mt-2">Governance, tracking, and measurement for authorized adversarial simulations.</p>
        </div>
        <Button className="bg-rose-600 hover:bg-rose-700 text-white shadow-lg shadow-rose-500/20 gap-2">
            <Plus size={18} /> New Campaign
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard title="Active Campaigns" value={2} icon={<Activity className="text-emerald-400" />} />
          <StatCard title="Pending Approvals" value={1} icon={<Shield className="text-amber-400" />} />
          <StatCard title="Open Findings" value={14} icon={<Target className="text-rose-400" />} />
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4 text-slate-200">Campaign Portfolio</h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <CampaignCard 
                name="Operation Silent Drop (Ransomware Sim)" 
                status="IN_PROGRESS" 
                approvals="3/3"
                findings={4}
            />
            <CampaignCard 
                name="Cloud Data Exfiltration Validation" 
                status="PENDING_APPROVAL" 
                approvals="1/3"
                findings={0}
            />
            <CampaignCard 
                name="Supply Chain Compromise - Q2" 
                status="COMPLETED" 
                approvals="3/3"
                findings={12}
            />
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-2">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">{title}</h3>
                    {icon}
                </div>
                <div className="text-3xl font-black text-slate-200 mb-1">{value}</div>
            </CardContent>
        </Card>
    );
}

function CampaignCard({ name, status, approvals, findings }: any) {
    const isPending = status === 'PENDING_APPROVAL';
    
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${isPending ? 'border-t-4 border-t-amber-500' : 'border-t-4 border-t-rose-500'}`}>
            <CardContent className="p-6">
                <h3 className="text-lg font-bold text-slate-200 mb-1">{name}</h3>
                
                <div className="flex items-center gap-2 mb-4">
                    <span className={`text-[10px] font-bold px-2 py-1 rounded ${isPending ? 'bg-amber-500/10 text-amber-500' : (status === 'COMPLETED' ? 'bg-slate-800 text-slate-400' : 'bg-emerald-500/10 text-emerald-400')}`}>
                        {status}
                    </span>
                </div>
                
                <div className="space-y-2 font-mono text-xs">
                    <div className="flex justify-between">
                        <span className="text-slate-500">Sign-offs</span>
                        <span className={isPending ? "text-amber-400" : "text-emerald-400"}>{approvals}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">Findings</span>
                        <span className="text-rose-400">{findings}</span>
                    </div>
                </div>
                
                <div className="mt-6 pt-4 border-t border-slate-800 flex justify-end">
                    <Button variant="ghost" className="text-xs h-8 text-rose-400 hover:text-rose-300 hover:bg-rose-950/30">View Details</Button>
                </div>
            </CardContent>
        </Card>
    );
}
