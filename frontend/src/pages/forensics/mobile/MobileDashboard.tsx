import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Smartphone, UploadCloud, MessageSquare, MapPin } from 'lucide-react';

export default function MobileDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-sky-400">
            <Smartphone size={32} />
            Mobile Forensics
          </h1>
          <p className="text-slate-400 mt-2">Ingest and extract artifacts from iOS/Android logical backups and physical acquisitions.</p>
        </div>
        <Button className="bg-sky-600 hover:bg-sky-700 text-white shadow-lg shadow-sky-500/20 gap-2">
            <UploadCloud size={18} /> Import Mobile Backup
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <DeviceCard 
              name="CEO_iPhone_14_Pro" 
              os="iOS 17.2" 
              type="iTunes Backup" 
              status="ANALYZED"
              messages={1420}
              locations={85}
          />
          <DeviceCard 
              name="Suspect_Samsung_S23" 
              os="Android 14" 
              type="ADB Logical" 
              status="ANALYZED"
              messages={802}
              locations={412}
          />
      </div>
    </div>
  );
}

function DeviceCard({ name, os, type, status, messages, locations }: any) {
    const isAnalyzed = status === 'ANALYZED';
    
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${isAnalyzed ? 'border-t-4 border-t-emerald-500' : 'border-t-4 border-t-sky-500'}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                        <Smartphone size={20} className="text-slate-400" />
                        <h3 className="text-lg font-bold text-slate-200 truncate" title={name}>{name}</h3>
                    </div>
                </div>
                
                <div className="space-y-3 mb-6 font-mono text-sm">
                    <div className="flex justify-between">
                        <span className="text-slate-500">OS Version</span>
                        <span className="text-slate-300">{os}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">Acquisition</span>
                        <span className="text-slate-300">{type}</span>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2 mb-6">
                    <div className="bg-slate-950 p-2 rounded border border-slate-800 flex items-center gap-2">
                        <MessageSquare size={14} className="text-sky-400" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-slate-500 uppercase font-bold">Messages</span>
                            <span className="text-xs font-mono text-slate-300">{messages}</span>
                        </div>
                    </div>
                    <div className="bg-slate-950 p-2 rounded border border-slate-800 flex items-center gap-2">
                        <MapPin size={14} className="text-emerald-400" />
                        <div className="flex flex-col">
                            <span className="text-[10px] text-slate-500 uppercase font-bold">Locations</span>
                            <span className="text-xs font-mono text-slate-300">{locations}</span>
                        </div>
                    </div>
                </div>

                <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                    <span className="text-xs font-bold px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {status}
                    </span>
                    <Button variant="outline" className="text-xs h-8 border-slate-700 bg-slate-800 hover:bg-slate-700">Explore Artifacts</Button>
                </div>
            </CardContent>
        </Card>
    );
}
