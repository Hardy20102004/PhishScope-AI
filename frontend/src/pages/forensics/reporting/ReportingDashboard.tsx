import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileText, FileSignature, FilePlus2, Link } from 'lucide-react';

export default function ReportingDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-indigo-400">
            <FileSignature size={32} />
            Automated Forensic Reporting
          </h1>
          <p className="text-slate-400 mt-2">Generate tamper-evident, court-ready documentation with full chain of custody tracking.</p>
        </div>
        <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/20 gap-2">
            <FilePlus2 size={18} /> New Report
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ReportCard 
              title="Operation Crimson Falcon - Executive Brief" 
              type="EXECUTIVE" 
              status="FINALIZED"
              evidenceCount={14}
              author="admin@company.com"
          />
          <ReportCard 
              title="Memory Dump Analysis - SRV-01" 
              type="TECHNICAL" 
              status="DRAFT"
              evidenceCount={3}
              author="analyst1@company.com"
          />
          <ReportCard 
              title="State vs. John Doe - Digital Evidence" 
              type="COURT_READY" 
              status="FINALIZED"
              evidenceCount={42}
              author="admin@company.com"
          />
      </div>
    </div>
  );
}

function ReportCard({ title, type, status, evidenceCount, author }: any) {
    const isFinal = status === 'FINALIZED';
    const isCourt = type === 'COURT_READY';
    
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${isCourt ? 'border-t-4 border-t-amber-500' : 'border-t-4 border-t-indigo-500'}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                        <FileText size={20} className={isCourt ? "text-amber-500" : "text-indigo-400"} />
                        <h3 className="text-lg font-bold text-slate-200 truncate" title={title}>{title}</h3>
                    </div>
                </div>
                
                <div className="space-y-3 mb-6 font-mono text-sm">
                    <div className="flex justify-between">
                        <span className="text-slate-500">Report Type</span>
                        <span className={isCourt ? "text-amber-400 font-bold" : "text-slate-300"}>{type}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">Author</span>
                        <span className="text-slate-300">{author}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">Linked Evidence</span>
                        <span className="text-slate-300 flex items-center gap-1"><Link size={12}/> {evidenceCount} items</span>
                    </div>
                </div>

                <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                    <span className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded ${isFinal ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-500 border border-amber-500/20'}`}>
                        {status}
                    </span>
                    <Button variant="outline" className="text-xs h-8 border-slate-700 bg-slate-800 hover:bg-slate-700">View Document</Button>
                </div>
            </CardContent>
        </Card>
    );
}
