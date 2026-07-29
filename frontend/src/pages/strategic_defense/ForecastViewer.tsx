import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { LineChart, TrendingUp, TrendingDown } from 'lucide-react';

export default function ForecastViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <LineChart className="text-cyan-400" />
                Strategic Enterprise Forecasting
            </h2>
            <p className="text-slate-400 mt-1">AI-projected trends for risk exposure, operational efficiency, and control effectiveness.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <ForecastCard 
                title="Projected Resilience Score (12 Months)"
                current="82"
                forecast="92"
                trend="up"
                confidence={94}
                description="Assuming completion of the planned Cloud Protection roadmap, overall enterprise resilience will climb to 92/100."
            />

            <ForecastCard 
                title="Projected Incident Response Time (MTTC)"
                current="1.8 hrs"
                forecast="0.5 hrs"
                trend="down"
                confidence={88}
                description="Full deployment of Autonomous SOAR playbooks is projected to reduce containment time to under 30 minutes."
            />

            <ForecastCard 
                title="Third-Party Vendor Risk Exposure"
                current="Medium"
                forecast="High"
                trend="up"
                confidence={75}
                description="Based on global threat intelligence trends, supply chain attacks are projected to increase risk exposure."
                warning={true}
            />
            
            <ForecastCard 
                title="SOC Operational Cost"
                current="$2.1M/yr"
                forecast="$1.6M/yr"
                trend="down"
                confidence={90}
                description="Consolidating EDR/NDR vendors and leveraging AI triage will reduce licensing and Tier-1 staffing costs."
            />

        </div>
    </div>
  );
}

function ForecastCard({ title, current, forecast, trend, confidence, description, warning = false }: any) {
    const isGoodTrend = (trend === 'up' && !warning) || (trend === 'down' && !warning);
    const trendColor = warning ? 'text-rose-400' : 'text-emerald-400';
    const TrendIcon = trend === 'up' ? TrendingUp : TrendingDown;

    return (
        <Card className={`bg-slate-900 border-slate-800 ${warning ? 'border-rose-900/30' : ''}`}>
            <CardContent className="p-6">
                <h3 className="text-lg font-bold text-slate-200 mb-4">{title}</h3>
                
                <div className="flex items-center gap-6 mb-6">
                    <div className="flex flex-col">
                        <span className="text-xs text-slate-500 uppercase font-bold mb-1">Current</span>
                        <span className="text-2xl font-black text-slate-400">{current}</span>
                    </div>
                    
                    <div className="text-slate-600">→</div>
                    
                    <div className="flex flex-col">
                        <span className="text-xs text-slate-500 uppercase font-bold mb-1">Projected</span>
                        <span className={`text-3xl font-black flex items-center gap-2 ${trendColor}`}>
                            {forecast} <TrendIcon size={24} />
                        </span>
                    </div>
                </div>
                
                <p className="text-sm text-slate-400 mb-4">{description}</p>
                
                <div className="flex items-center gap-2 text-xs">
                    <span className="font-bold text-slate-500">AI Confidence Level:</span>
                    <div className="w-32 bg-slate-800 rounded-full h-1.5">
                        <div className="h-1.5 rounded-full bg-cyan-500" style={{ width: `${confidence}%` }}></div>
                    </div>
                    <span className="text-cyan-400 font-bold">{confidence}%</span>
                </div>
            </CardContent>
        </Card>
    );
}
