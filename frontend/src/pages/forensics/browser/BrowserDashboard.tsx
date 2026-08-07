import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Globe, UploadCloud, History, Puzzle, ShieldAlert } from 'lucide-react';

export default function BrowserDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-amber-400">
            <Globe size={32} />
            Browser Forensics
          </h1>
          <p className="text-slate-400 mt-2">Extract and analyze web history, malicious downloads, and side-loaded extensions from Chromium/Firefox profiles.</p>
        </div>
        <Button className="bg-amber-600 hover:bg-amber-700 text-white shadow-lg shadow-amber-500/20 gap-2">
            <UploadCloud size={18} /> Import Browser Profile
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ProfileCard 
              name="jdoe_chrome_default" 
              browser="Google Chrome" 
              os="Windows 10" 
              status="THREATS DETECTED"
              historyCount={12450}
              extensionsCount={8}
              threats={2}
          />
          <ProfileCard 
              name="admin_firefox_dev" 
              browser="Mozilla Firefox" 
              os="macOS 14" 
              status="ANALYZED"
              historyCount={892}
              extensionsCount={3}
              threats={0}
          />
      </div>
    </div>
  );
}

function ProfileCard({ name, browser, os, status, historyCount, extensionsCount, threats }: any) {
    const hasThreats = threats > 0;
    
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${hasThreats ? 'border-t-4 border-t-rose-500' : 'border-t-4 border-t-amber-500'}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                        <Globe size={20} className="text-slate-400" />
                        <h3 className="text-lg font-bold text-slate-200 truncate" title={name}>{name}</h3>
                    </div>
                </div>
                
                <div className="space-y-3 mb-6 font-mono text-sm">
                    <div className="flex justify-between">
                        <span className="text-slate-500">Browser</span>
                        <span className="text-slate-300">{browser}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">Host OS</span>
                        <span className="text-slate-300">{os}</span>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2 mb-6">
                    <div className="bg-slate-950 p-2 rounded border border-slate-800 flex items-center gap-2">
                        <History size={14} className="text-amber-400" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-slate-500 uppercase font-bold">History</span>
                            <span className="text-xs font-mono text-slate-300">{historyCount.toLocaleString()}</span>
                        </div>
                    </div>
                    <div className="bg-slate-950 p-2 rounded border border-slate-800 flex items-center gap-2">
                        <Puzzle size={14} className="text-emerald-400" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-slate-500 uppercase font-bold">Extensions</span>
                            <span className="text-xs font-mono text-slate-300">{extensionsCount}</span>
                        </div>
                    </div>
                </div>

                <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                    <span className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded ${hasThreats ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}`}>
                        {hasThreats && <ShieldAlert size={12} />}
                        {status}
                    </span>
                    <Button variant="outline" className="text-xs h-8 border-slate-700 bg-slate-800 hover:bg-slate-700">Explore Artifacts</Button>
                </div>
            </CardContent>
        </Card>
    );
}
