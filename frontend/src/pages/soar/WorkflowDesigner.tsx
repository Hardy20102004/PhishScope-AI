import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { GitCommit, Save, Play, Search, Network } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function WorkflowDesigner() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      
      {/* Left Sidebar - Step Library */}
      <div className="w-64 border-r border-slate-800 bg-slate-900 flex flex-col">
          <div className="p-4 border-b border-slate-800">
              <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider">Step Library</h2>
          </div>
          <div className="p-4 space-y-4 flex-1 overflow-y-auto">
              <div className="space-y-2">
                  <h3 className="text-xs font-semibold text-slate-500">Triggers</h3>
                  <DraggableStep icon={<Play size={14}/>} label="On Incident Creation" color="blue" />
                  <DraggableStep icon={<Play size={14}/>} label="On High Priority Alert" color="blue" />
              </div>
              <div className="space-y-2">
                  <h3 className="text-xs font-semibold text-slate-500">Enrichment</h3>
                  <DraggableStep icon={<Search size={14}/>} label="VirusTotal IP Lookup" color="indigo" />
                  <DraggableStep icon={<Search size={14}/>} label="Query Knowledge Graph" color="indigo" />
              </div>
              <div className="space-y-2">
                  <h3 className="text-xs font-semibold text-slate-500">Containment</h3>
                  <DraggableStep icon={<Network size={14}/>} label="Isolate Host (EDR)" color="rose" />
                  <DraggableStep icon={<Network size={14}/>} label="Block IP (Firewall)" color="rose" />
              </div>
              <div className="space-y-2">
                  <h3 className="text-xs font-semibold text-slate-500">Flow Control</h3>
                  <DraggableStep icon={<GitCommit size={14}/>} label="Approval Gate" color="amber" />
                  <DraggableStep icon={<GitCommit size={14}/>} label="If/Else Branch" color="slate" />
              </div>
          </div>
      </div>

      {/* Main Canvas Area */}
      <div className="flex-1 flex flex-col relative">
          <div className="h-14 border-b border-slate-800 flex justify-between items-center px-4 bg-slate-900/50">
              <h1 className="text-lg font-bold text-slate-200">Ransomware Containment (Standard)</h1>
              <div className="flex gap-2">
                  <Button variant="outline" className="bg-slate-900 border-slate-700 h-8 text-xs">
                      <Save size={14} className="mr-2" /> Save Draft
                  </Button>
                  <Button className="bg-cyan-600 hover:bg-cyan-700 h-8 text-xs text-white">
                      Publish Playbook
                  </Button>
              </div>
          </div>
          
          {/* Mock Canvas Area */}
          <div className="flex-1 bg-slate-950 p-8 relative overflow-hidden" style={{ backgroundImage: 'radial-gradient(#334155 1px, transparent 1px)', backgroundSize: '20px 20px' }}>
              
              {/* Node 1 */}
              <div className="absolute top-10 left-[40%] w-64 bg-slate-900 border-2 border-blue-500/50 rounded-lg p-3 shadow-lg">
                  <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded bg-blue-500/20 flex items-center justify-center text-blue-400"><Play size={12}/></div>
                      <span className="text-sm font-semibold text-slate-200">On Incident Created</span>
                  </div>
                  <p className="text-[10px] text-slate-500">Trigger: Severity &gt;= HIGH</p>
              </div>

              {/* Edge 1 */}
              <div className="absolute top-[88px] left-[46.5%] w-0.5 h-12 bg-slate-600"></div>

              {/* Node 2 */}
              <div className="absolute top-[136px] left-[40%] w-64 bg-slate-900 border-2 border-indigo-500/50 rounded-lg p-3 shadow-lg">
                  <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded bg-indigo-500/20 flex items-center justify-center text-indigo-400"><Search size={12}/></div>
                      <span className="text-sm font-semibold text-slate-200">Enrich IPs (VirusTotal)</span>
                  </div>
                  <p className="text-[10px] text-slate-500">Action: Extract IPs & Lookup</p>
              </div>

              {/* Edge 2 */}
              <div className="absolute top-[214px] left-[46.5%] w-0.5 h-12 bg-slate-600"></div>

              {/* Node 3 (Approval Gate) */}
              <div className="absolute top-[262px] left-[40%] w-64 bg-slate-900 border-2 border-amber-500/80 rounded-lg p-3 shadow-lg shadow-amber-500/10">
                  <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded bg-amber-500/20 flex items-center justify-center text-amber-400"><GitCommit size={12}/></div>
                      <span className="text-sm font-semibold text-slate-200">Approval Gate</span>
                  </div>
                  <p className="text-[10px] text-slate-500">Required: SOC L2 Approval</p>
              </div>

              {/* Edge 3 */}
              <div className="absolute top-[340px] left-[46.5%] w-0.5 h-12 bg-slate-600"></div>

              {/* Node 4 (Containment) */}
              <div className="absolute top-[388px] left-[40%] w-64 bg-slate-900 border-2 border-rose-500/50 rounded-lg p-3 shadow-lg">
                  <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 rounded bg-rose-500/20 flex items-center justify-center text-rose-400"><Network size={12}/></div>
                      <span className="text-sm font-semibold text-slate-200">Isolate Host (CrowdStrike)</span>
                  </div>
                  <p className="text-[10px] text-slate-500">Action: Network Containment</p>
              </div>

          </div>
      </div>
    </div>
  );
}

function DraggableStep({ icon, label, color }: any) {
    return (
        <div className="flex items-center gap-3 p-2 bg-slate-950 rounded border border-slate-800 cursor-grab hover:border-slate-600 transition-colors">
            <div className={`w-8 h-8 rounded bg-${color}-500/10 flex items-center justify-center text-${color}-400`}>
                {icon}
            </div>
            <span className="text-xs text-slate-300 font-medium">{label}</span>
        </div>
    );
}
