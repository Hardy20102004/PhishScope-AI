import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, LineChart, Activity, Clock } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function OperationalMetrics() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <BarChart className="text-teal-500" />
                SOC Operational Analytics
            </h1>
            <p className="text-slate-400 mt-1">Detailed performance KPIs and team velocity tracking.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="bg-slate-900 border-slate-800">
                <CardHeader>
                    <CardTitle className="text-slate-200 flex items-center gap-2 text-sm uppercase tracking-wider">
                        <Clock size={16} className="text-slate-500" /> Resolution Velocity (MTTR)
                    </CardTitle>
                </CardHeader>
                <CardContent className="h-64 flex flex-col items-center justify-center border-t border-slate-800/50 bg-slate-950/50 relative">
                    {/* Placeholder for Recharts/Chart.js */}
                    <LineChart size={48} className="text-slate-700 mb-4" />
                    <p className="text-slate-500 text-sm">MTTR Time-Series Visualization</p>
                    <div className="absolute bottom-4 left-4 right-4 flex justify-between text-xs text-slate-400">
                        <span>June 1</span>
                        <span>July 29</span>
                    </div>
                </CardContent>
            </Card>

            <Card className="bg-slate-900 border-slate-800">
                <CardHeader>
                    <CardTitle className="text-slate-200 flex items-center gap-2 text-sm uppercase tracking-wider">
                        <Activity size={16} className="text-slate-500" /> SLA Compliance Rate
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6 pt-4">
                    <div>
                        <div className="flex justify-between text-sm text-slate-300 mb-2">
                            <span>Critical Incidents (< 1 hr response)</span>
                            <span className="text-emerald-400 font-mono">98.5%</span>
                        </div>
                        <Progress value={98.5} className="h-2 bg-slate-800" indicatorClassName="bg-emerald-500" />
                    </div>
                    <div>
                        <div className="flex justify-between text-sm text-slate-300 mb-2">
                            <span>High Incidents (< 4 hr response)</span>
                            <span className="text-emerald-400 font-mono">94.2%</span>
                        </div>
                        <Progress value={94.2} className="h-2 bg-slate-800" indicatorClassName="bg-emerald-500" />
                    </div>
                    <div>
                        <div className="flex justify-between text-sm text-slate-300 mb-2">
                            <span>Medium Incidents (< 24 hr response)</span>
                            <span className="text-amber-400 font-mono">82.1%</span>
                        </div>
                        <Progress value={82.1} className="h-2 bg-slate-800" indicatorClassName="bg-amber-500" />
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>
  );
}
