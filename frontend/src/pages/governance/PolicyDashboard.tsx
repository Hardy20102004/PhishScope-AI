import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileText, Plus, CheckCircle, XCircle } from 'lucide-react';

export default function PolicyDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-emerald-400">
            <FileText size={32} />
            Enterprise Security Policy Management
          </h1>
          <p className="text-slate-400 mt-2">Centralized lifecycle management for all cloud governance and security policies.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-500/20 gap-2">
                <Plus size={18} /> Create New Policy
            </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <div className="lg:col-span-2 space-y-6">
              
              <Card className="bg-slate-900 border-slate-800">
                  <CardContent className="p-6">
                      <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                          <h3 className="text-lg font-bold text-slate-200">Active Governance Policies</h3>
                          <input type="text" placeholder="Search policies..." className="bg-slate-950 border border-slate-700 rounded px-3 py-1 text-sm text-slate-200 w-64 focus:outline-none focus:border-emerald-500" />
                      </div>
                      
                      <div className="space-y-4">
                          <PolicyRow name="Require KMS Customer Managed Keys for PII" domain="STORAGE" version="v2.1" active={true} />
                          <PolicyRow name="Prohibit Public Read Access on Storage" domain="STORAGE" version="v4.0" active={true} />
                          <PolicyRow name="Enforce MFA for Cloud Consoles" domain="IDENTITY" version="v1.2" active={true} />
                          <PolicyRow name="Restrict Default VPC Usage" domain="NETWORK" version="v1.0" active={false} />
                      </div>
                  </CardContent>
              </Card>

          </div>

          <div className="space-y-6">
              <Card className="bg-slate-900 border-slate-800">
                  <CardContent className="p-6">
                      <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Policy Distribution</h3>
                      
                      <div className="space-y-4">
                          <StatRow label="Identity & Access" count={42} />
                          <StatRow label="Storage & Data" count={28} />
                          <StatRow label="Network Security" count={15} />
                          <StatRow label="Compute Workloads" count={34} />
                      </div>
                  </CardContent>
              </Card>
          </div>

      </div>
    </div>
  );
}

function PolicyRow({ name, domain, version, active }: any) {
    return (
        <div className="flex justify-between items-center p-4 bg-slate-950/50 rounded border border-slate-800/50 hover:border-slate-600 transition-colors cursor-pointer">
            <div className="flex flex-col gap-1">
                <span className="text-sm font-bold text-slate-200">{name}</span>
                <div className="flex gap-3 text-xs text-slate-500">
                    <span className="font-mono text-indigo-400">{domain}</span>
                    <span>Version {version}</span>
                </div>
            </div>
            <div>
                {active ? (
                    <div className="flex items-center gap-1 text-xs font-bold text-emerald-400 bg-emerald-950/30 px-2 py-1 rounded border border-emerald-900/50">
                        <CheckCircle size={14} /> ACTIVE
                    </div>
                ) : (
                    <div className="flex items-center gap-1 text-xs font-bold text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-700">
                        <XCircle size={14} /> DRAFT
                    </div>
                )}
            </div>
        </div>
    );
}

function StatRow({ label, count }: any) {
    return (
        <div className="flex justify-between items-center text-sm border-b border-slate-800/50 pb-2">
            <span className="text-slate-300">{label}</span>
            <span className="font-bold text-emerald-400">{count}</span>
        </div>
    );
}
