import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Mail, UploadCloud, FileText, ShieldAlert } from 'lucide-react';

export default function EmailDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-indigo-400">
            <Mail size={32} />
            Email Forensics
          </h1>
          <p className="text-slate-400 mt-2">Ingest EML/PST files to analyze headers, validate DKIM/SPF, and identify spoofed senders.</p>
        </div>
        <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/20 gap-2">
            <UploadCloud size={18} /> Import Mailbox/EML
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <MailboxCard 
              name="Phishing_Sample_01.eml" 
              type="EML File" 
              owner="jdoe@company.com" 
              status="SPOOF DETECTED"
              messageCount={1}
              isSpoofed={true}
          />
          <MailboxCard 
              name="jdoe_archive.pst" 
              type="PST Export" 
              owner="jdoe@company.com" 
              status="ANALYZED"
              messageCount={4215}
              isSpoofed={false}
          />
      </div>
    </div>
  );
}

function MailboxCard({ name, type, owner, status, messageCount, isSpoofed }: any) {
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${isSpoofed ? 'border-t-4 border-t-rose-500' : 'border-t-4 border-t-indigo-500'}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                        <Mail size={20} className="text-slate-400" />
                        <h3 className="text-lg font-bold text-slate-200 truncate" title={name}>{name}</h3>
                    </div>
                </div>
                
                <div className="space-y-3 mb-6 font-mono text-sm">
                    <div className="flex justify-between">
                        <span className="text-slate-500">Source</span>
                        <span className="text-slate-300">{type}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">Target User</span>
                        <span className="text-slate-300">{owner}</span>
                    </div>
                </div>

                <div className="bg-slate-950 p-2 rounded border border-slate-800 flex items-center gap-2 mb-6 w-1/2">
                    <FileText size={14} className="text-indigo-400" />
                    <div className="flex flex-col">
                        <span className="text-[10px] text-slate-500 uppercase font-bold">Messages</span>
                        <span className="text-xs font-mono text-slate-300">{messageCount.toLocaleString()}</span>
                    </div>
                </div>

                <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                    <span className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded ${isSpoofed ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}`}>
                        {isSpoofed && <ShieldAlert size={12} />}
                        {status}
                    </span>
                    <Button variant="outline" className="text-xs h-8 border-slate-700 bg-slate-800 hover:bg-slate-700">Open Viewer</Button>
                </div>
            </CardContent>
        </Card>
    );
}
