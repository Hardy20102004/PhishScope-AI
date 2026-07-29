import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { History, ShieldAlert, ExternalLink, Globe } from 'lucide-react';

export default function HistoryExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <History className="text-amber-400" />
                Web History Explorer
            </h2>
            <p className="text-slate-400 mt-1">Searchable chronological log of all visited URLs, cross-referenced with Threat Intelligence.</p>
        </div>

        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-0">
                <div className="grid grid-cols-12 gap-4 p-4 border-b border-slate-800 bg-slate-950/50 text-xs font-bold text-slate-500 tracking-wider">
                    <div className="col-span-2">TIMESTAMP</div>
                    <div className="col-span-8">URL & TITLE</div>
                    <div className="col-span-2">THREAT STATUS</div>
                </div>
                
                <div className="divide-y divide-slate-800/50 font-mono text-sm">
                    <HistoryRow 
                        time="Jul 27, 2026 14:00:12" 
                        url="https://mail.google.com/mail/u/0/#inbox" 
                        title="Inbox - Google Workspace"
                        isThreat={false}
                    />
                    <HistoryRow 
                        time="Jul 27, 2026 14:02:45" 
                        url="https://admin.google.com/Dashboard" 
                        title="Google Workspace Admin Console"
                        isThreat={false}
                    />
                    <HistoryRow 
                        time="Jul 27, 2026 14:05:01" 
                        url="http://login-microsoft-secure.com/auth" 
                        title="Microsoft Account Login"
                        isThreat={true}
                        category="Credential Phishing"
                    />
                </div>
            </CardContent>
        </Card>
    </div>
  );
}

function HistoryRow({ time, url, title, isThreat, category }: any) {
    return (
        <div className={`grid grid-cols-12 gap-4 p-4 items-center ${isThreat ? 'bg-rose-950/20' : 'hover:bg-slate-800/20'}`}>
            <div className="col-span-2 text-slate-500 text-xs">{time}</div>
            
            <div className="col-span-8 flex flex-col gap-1">
                <div className="flex items-center gap-2">
                    <Globe size={14} className={isThreat ? 'text-rose-500' : 'text-sky-400'} />
                    <span className={`font-bold truncate ${isThreat ? 'text-rose-400' : 'text-slate-200'}`} title={title}>{title}</span>
                </div>
                <div className="flex items-center gap-2 ml-5">
                    <span className="text-xs text-slate-400 truncate max-w-xl">{url}</span>
                    <a href={url} target="_blank" rel="noreferrer" className="text-slate-600 hover:text-slate-400">
                        <ExternalLink size={12} />
                    </a>
                </div>
            </div>

            <div className="col-span-2">
                {isThreat ? (
                    <div className="flex flex-col">
                        <span className="flex items-center gap-1 text-xs font-bold text-rose-500">
                            <ShieldAlert size={12} /> KNOWN THREAT
                        </span>
                        <span className="text-[10px] text-rose-400">{category}</span>
                    </div>
                ) : (
                    <span className="text-xs text-slate-600">CLEAN</span>
                )}
            </div>
        </div>
    );
}
