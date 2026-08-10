import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { BarChart3, TrendingDown, TrendingUp } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ExecutiveKPIDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <BarChart3 className="text-rose-400" />
                    Board-Level Metrics (KPIs)
                </h2>
                <p className="text-slate-400 mt-1">Standardized, high-level reporting metrics for non-technical stakeholders.</p>
            </div>
            <Button variant="outline" onClick={() => window.print()} className="bg-slate-900 border-slate-700 text-slate-300">
                Export PDF Report
            </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <KPICard 
                title="Mean Time to Detect (MTTD)" 
                value="4.2" 
                unit="Hours" 
                trend="-12% (Improving)" 
                trendIcon={<TrendingDown size={14} className="text-emerald-400" />} 
            />
            
            <KPICard 
                title="Mean Time to Contain (MTTC)" 
                value="1.8" 
                unit="Hours" 
                trend="-8% (Improving)" 
                trendIcon={<TrendingDown size={14} className="text-emerald-400" />} 
            />
            
            <KPICard 
                title="BAS Validation Success Rate" 
                value="88" 
                unit="%" 
                trend="+4% (Improving)" 
                trendIcon={<TrendingUp size={14} className="text-emerald-400" />} 
            />

            <KPICard 
                title="Critical Patches > 30 Days" 
                value="12" 
                unit="Assets" 
                trend="+2 (Degrading)" 
                trendIcon={<TrendingUp size={14} className="text-rose-400" />} 
                warning={true}
            />

            <KPICard 
                title="Phishing Simulation Failure Rate" 
                value="3.4" 
                unit="%" 
                trend="-1.2% (Improving)" 
                trendIcon={<TrendingDown size={14} className="text-emerald-400" />} 
            />
            
            <KPICard 
                title="MFA Enforcement" 
                value="99.8" 
                unit="%" 
                trend="Stable" 
            />

        </div>
    </div>
  );
}

function KPICard({ title, value, unit, trend, trendIcon, warning = false }: any) {
    return (
        <Card className={`bg-slate-900 border-slate-800 ${warning ? 'border-rose-900/50' : ''}`}>
            <CardContent className="p-6">
                <h3 className="text-sm font-bold text-slate-400 mb-4">{title}</h3>
                
                <div className="flex items-end gap-2 mb-4">
                    <span className={`text-4xl font-black ${warning ? 'text-rose-400' : 'text-slate-100'}`}>
                        {value}
                    </span>
                    <span className="text-sm text-slate-500 font-bold mb-1">{unit}</span>
                </div>
                
                <div className="flex items-center gap-2 text-xs font-bold text-slate-400 bg-slate-950 px-3 py-2 rounded w-fit border border-slate-800">
                    {trendIcon} {trend}
                </div>
            </CardContent>
        </Card>
    );
}
