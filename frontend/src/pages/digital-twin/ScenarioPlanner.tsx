import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Play, Settings2, BarChart4 } from 'lucide-react';

export default function ScenarioPlanner() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-indigo-400">
            <Settings2 size={32} />
            Digital Twin Scenario Planner
          </h1>
          <p className="text-slate-400 mt-2">Adjust operational parameters to forecast future SOC capacity and SLA impacts.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader>
              <CardTitle className="text-slate-200">What-If Parameters</CardTitle>
              <CardDescription className="text-slate-500">Define the variables for your simulation.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-8">
                
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <Label className="text-slate-300">Alert Volume Multiplier</Label>
                        <span className="text-indigo-400 font-mono bg-indigo-500/10 px-2 py-1 rounded">1.5x</span>
                    </div>
                    <Slider defaultValue={[1.5]} max={3} step={0.1} className="py-2" />
                    <p className="text-xs text-slate-500">Simulate a 50% increase in daily alerts (e.g. M&A or new telemetry).</p>
                </div>

                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <Label className="text-slate-300">L1 Analyst Headcount</Label>
                        <span className="text-indigo-400 font-mono bg-indigo-500/10 px-2 py-1 rounded">12</span>
                    </div>
                    <Slider defaultValue={[12]} max={50} step={1} className="py-2" />
                    <p className="text-xs text-slate-500">Available staff for alert triage per 24hr cycle.</p>
                </div>

                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <Label className="text-slate-300">Playbook Automation Rate</Label>
                        <span className="text-indigo-400 font-mono bg-indigo-500/10 px-2 py-1 rounded">45%</span>
                    </div>
                    <Slider defaultValue={[45]} max={100} step={5} className="py-2" />
                    <p className="text-xs text-slate-500">Percentage of alerts resolved entirely via SOAR.</p>
                </div>

                <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white gap-2 shadow-lg shadow-indigo-500/20">
                    <Play size={16} /> Execute Simulation
                </Button>
            </CardContent>
          </Card>

          <Card className="bg-slate-900 border-slate-800 flex items-center justify-center relative overflow-hidden">
             <div className="absolute opacity-5"><BarChart4 size={300} /></div>
             <div className="text-center z-10 space-y-2">
                 <Settings2 size={48} className="mx-auto text-slate-600 animate-spin-slow" />
                 <h3 className="text-xl font-bold text-slate-400">Awaiting Simulation</h3>
                 <p className="text-slate-500 text-sm">Configure parameters and click Execute to generate forecasts.</p>
             </div>
          </Card>
      </div>
    </div>
  );
}
