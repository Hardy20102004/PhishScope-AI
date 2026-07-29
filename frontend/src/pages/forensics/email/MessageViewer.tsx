import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Mail, ShieldAlert, User, ShieldCheck } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function MessageViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6 flex justify-between items-end">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Mail className="text-indigo-400" />
                    Email Message Viewer
                </h2>
                <p className="text-slate-400 mt-1">Review the raw body and extracted metadata of the target email.</p>
            </div>
            <div className="flex gap-2">
                <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/50 flex gap-1">
                    <ShieldAlert size={14} /> SPF FAIL
                </Badge>
                <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/50 flex gap-1">
                    <ShieldAlert size={14} /> DKIM FAIL
                </Badge>
                <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/50 flex gap-1 font-bold shadow-[0_0_10px_rgba(244,63,94,0.3)]">
                    <ShieldAlert size={14} /> SPOOFED SENDER
                </Badge>
            </div>
        </div>

        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-0">
                {/* Email Header Block */}
                <div className="p-6 border-b border-slate-800 bg-slate-900/50 space-y-4">
                    <div className="flex justify-between items-start">
                        <h3 className="text-xl font-bold text-slate-200">URGENT: Password Expiry Notification</h3>
                        <span className="text-sm font-mono text-slate-500">Jul 27, 2026 14:00 UTC</span>
                    </div>
                    
                    <div className="grid grid-cols-[80px_1fr] gap-2 text-sm">
                        <span className="text-slate-500 font-bold text-right">From:</span>
                        <div className="flex items-center gap-2">
                            <User size={16} className="text-slate-400" />
                            <span className="text-slate-200">IT Support</span>
                            <span className="text-rose-400 font-mono bg-rose-950 px-1 rounded">&lt;admin@microsoft-secure-update.com&gt;</span>
                        </div>
                        
                        <span className="text-slate-500 font-bold text-right">To:</span>
                        <span className="text-slate-300 font-mono">&lt;jdoe@company.com&gt;</span>
                    </div>
                </div>
                
                {/* Email Body */}
                <div className="p-6 text-slate-300 whitespace-pre-wrap font-sans text-sm leading-relaxed">
                    Dear user,
                    <br/><br/>
                    Your password expires in 24 hours. Please click here to retain access: 
                    <br/>
                    <a href="#" className="text-sky-400 hover:underline">http://login-microsoft-secure.com/auth</a>
                    <br/><br/>
                    IT Support
                </div>
            </CardContent>
        </Card>
    </div>
  );
}
