import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Lightbulb, Users, Cog } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function OptimizationDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <h1 className="text-2xl font-bold text-slate-200 mb-6 flex items-center gap-2">
            <Lightbulb className="text-amber-400" />
            AI Optimization Recommendations
        </h1>
        
        <div className="space-y-4">
            <RecommendationCard 
                category="STAFFING"
                title="Increase L1 Headcount by 3"
                description="Simulation Q4 M&A Forecast indicates a 115% utilization rate, leading to catastrophic SLA breaches. Hiring 3 additional L1 analysts restores utilization to a sustainable 82%."
                impact="Restores SLA compliance to 95%. Drops MTTR by 12 mins."
                icon={<Users size={24} className="text-blue-400" />}
            />
            
            <RecommendationCard 
                category="AUTOMATION"
                title="Deploy 'Suspicious Login' SOAR Playbook"
                description="Currently, 22% of analyst time is spent investigating Okta Impossible Travel alerts. Implementing the automated playbook will drastically reduce manual queueing."
                impact="Increases automation rate by +12%. Reduces backlog."
                icon={<Cog size={24} className="text-emerald-400" />}
            />
        </div>
    </div>
  );
}

function RecommendationCard({ category, title, description, impact, icon }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
            <CardContent className="p-6 flex gap-6 items-start">
                <div className="p-4 bg-slate-950 rounded-xl border border-slate-800">
                    {icon}
                </div>
                <div className="flex-1 space-y-2">
                    <span className="text-[10px] font-bold text-slate-500 tracking-widest">{category}</span>
                    <h3 className="text-lg font-bold text-slate-200">{title}</h3>
                    <p className="text-sm text-slate-400 leading-relaxed max-w-3xl">{description}</p>
                    <div className="mt-4 inline-block px-3 py-1 bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-medium rounded">
                        Expected Impact: {impact}
                    </div>
                </div>
                <div>
                    <Button variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800 text-xs">View Plan</Button>
                </div>
            </CardContent>
        </Card>
    );
}
