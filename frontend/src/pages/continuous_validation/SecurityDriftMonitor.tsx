import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Activity, AlertTriangle, TrendingDown } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function SecurityDriftMonitor() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <TrendingDown className="text-rose-500" />
                Security Drift Monitor
            </h2>
            <p className="text-slate-400 mt-1">Automatic detection of regressions in security controls, detections, or response capabilities.</p>
        </div>

        <div className="space-y-4 font-mono">
            
            {/* Active Drift Record */}
            <Card className="bg-rose-950/20 border-rose-900/50">
                <CardContent className="p-4 grid grid-cols-12 gap-4 items-center">
                    
                    <div className="col-span-1 flex justify-center">
                        <AlertTriangle size={24} className="text-rose-500 animate-pulse" />
                    </div>

                    <div className="col-span-5 flex flex-col gap-1">
                        <span className="text-[10px] text-rose-400 font-bold uppercase">CONTROL_FAILURE</span>
                        <span className="text-sm text-slate-200">EDR Block Rate Dropped in AWS Production Environment</span>
                        <span className="text-[10px] text-slate-400">Detected via automated BAS simulation (T1059.001)</span>
                    </div>
                    
                    <div className="col-span-3 flex flex-col gap-1 text-center border-x border-slate-800 px-2">
                        <span className="text-[10px] text-slate-500 font-bold uppercase">Regression</span>
                        <div className="flex justify-center items-center gap-2 text-xs">
                            <span className="text-slate-400 line-through">98%</span>
                            <span className="text-rose-500 font-bold">➔ 72%</span>
                        </div>
                    </div>

                    <div className="col-span-3 flex justify-end gap-2">
                        <Button variant="outline" className="text-xs h-8 bg-slate-900 border-slate-700 text-slate-300">Acknowledge</Button>
                        <Button className="text-xs h-8 bg-rose-600 hover:bg-rose-700 text-white">Create Ticket</Button>
                    </div>
                    
                </CardContent>
            </Card>

            {/* Historical Drift Record (Acknowledged) */}
            <Card className="bg-slate-900 border-slate-800 opacity-60">
                <CardContent className="p-4 grid grid-cols-12 gap-4 items-center">
                    <div className="col-span-1 flex justify-center">
                        <Activity size={20} className="text-amber-500" />
                    </div>
                    <div className="col-span-5 flex flex-col gap-1">
                        <span className="text-[10px] text-amber-500 font-bold uppercase">DETECTION_DEGRADATION</span>
                        <span className="text-sm text-slate-300">Splunk Rule 'Suspicious Login' FP Rate Spiked</span>
                    </div>
                    <div className="col-span-3 flex justify-center text-xs">
                        <span className="text-slate-500">ACKNOWLEDGED</span>
                    </div>
                    <div className="col-span-3 flex justify-end">
                         <span className="text-[10px] text-slate-500">Ticket: SOC-9912</span>
                    </div>
                </CardContent>
            </Card>

        </div>
    </div>
  );
}
