import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { HardDrive, UploadCloud, ShieldCheck, Hash } from 'lucide-react';

export default function DiskDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-cyan-400">
            <HardDrive size={32} />
            Disk Image Forensics
          </h1>
          <p className="text-slate-400 mt-2">Upload, hash-verify, and parse raw disk images (E01, RAW) for deep forensic analysis.</p>
        </div>
        <Button className="bg-cyan-600 hover:bg-cyan-700 text-white shadow-lg shadow-cyan-500/20 gap-2">
            <UploadCloud size={18} /> Import Evidence
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ImageCard 
              filename="DESKTOP-HR05-ACQ.E01" 
              size="256 GB" 
              status="VERIFIED" 
              caseId="INV-2026-992" 
          />
          <ImageCard 
              filename="SRV-DB01-MEM.RAW" 
              size="64 GB" 
              status="PARSING" 
              caseId="INV-2026-910" 
          />
      </div>
    </div>
  );
}

function ImageCard({ filename, size, status, caseId }: any) {
    const isVerified = status === 'VERIFIED';
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${isVerified ? 'border-t-4 border-t-emerald-500' : 'border-t-4 border-t-cyan-500'}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                        <HardDrive size={20} className="text-slate-400" />
                        <h3 className="text-lg font-bold text-slate-200 truncate" title={filename}>{filename}</h3>
                    </div>
                </div>
                
                <div className="space-y-3 mb-6">
                    <div className="flex justify-between text-sm">
                        <span className="text-slate-500">Size</span>
                        <span className="text-slate-300 font-mono">{size}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                        <span className="text-slate-500">Linked Case</span>
                        <span className="text-cyan-400">{caseId}</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs bg-slate-950 p-2 rounded border border-slate-800">
                        <Hash size={14} className="text-slate-500" />
                        <span className="text-slate-400 font-mono truncate">MD5: a1b2c3d4e5f6g7h8i9j0</span>
                    </div>
                </div>

                <div className="flex justify-between items-center">
                    <span className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded ${isVerified ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'}`}>
                        {isVerified && <ShieldCheck size={12} />}
                        {status}
                    </span>
                    <Button variant="outline" className="text-xs h-8 border-slate-700 bg-slate-800 hover:bg-slate-700">Explore Files</Button>
                </div>
            </CardContent>
        </Card>
    );
}
