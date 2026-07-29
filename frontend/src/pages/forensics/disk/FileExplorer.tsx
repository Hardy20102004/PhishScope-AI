import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Folder, File, FileWarning, Search, Binary } from 'lucide-react';
import { Input } from '@/components/ui/input';

export default function FileExplorer() {
  return (
    <div className="flex h-[calc(100vh-4rem)] bg-slate-950 text-slate-100 font-sans border-t border-slate-800">
        
        {/* Left Tree Pane */}
        <div className="w-1/3 border-r border-slate-800 flex flex-col bg-slate-900/50">
            <div className="p-4 border-b border-slate-800">
                <div className="flex items-center gap-2 bg-slate-900 rounded border border-slate-700 px-3 py-1.5">
                    <Search size={16} className="text-slate-400" />
                    <Input className="border-none h-6 bg-transparent text-sm focus-visible:ring-0 placeholder:text-slate-600" placeholder="Search MFT..." />
                </div>
            </div>
            <div className="p-4 space-y-2 overflow-y-auto font-mono text-sm">
                <TreeItem icon={<Folder className="text-blue-400" size={16} />} text="Windows" />
                <div className="pl-6 space-y-2 border-l border-slate-800 ml-2">
                    <TreeItem icon={<Folder className="text-blue-400" size={16} />} text="System32" />
                    <div className="pl-6 space-y-2 border-l border-slate-800 ml-2">
                        <TreeItem icon={<File className="text-slate-400" size={16} />} text="cmd.exe" />
                        <TreeItem icon={<File className="text-slate-400" size={16} />} text="svchost.exe" />
                    </div>
                </div>
                <TreeItem icon={<Folder className="text-blue-400" size={16} />} text="Temp" />
                <div className="pl-6 space-y-2 border-l border-slate-800 ml-2">
                    <TreeItem icon={<FileWarning className="text-rose-500" size={16} />} text="malware.exe" danger />
                </div>
                <TreeItem icon={<Folder className="text-rose-900" size={16} />} text="[UNALLOCATED]" />
                <div className="pl-6 space-y-2 border-l border-slate-800 ml-2">
                    <TreeItem icon={<File className="text-amber-500" size={16} />} text="carved_file_001.pdf (Deleted)" warning />
                </div>
            </div>
        </div>

        {/* Right Detail Pane (Hex Viewer Simulation) */}
        <div className="w-2/3 flex flex-col">
            <div className="p-4 border-b border-slate-800 bg-slate-900 flex justify-between items-center">
                <div>
                    <h3 className="font-bold text-slate-200 flex items-center gap-2">
                        <FileWarning className="text-rose-500" size={18} /> malware.exe
                    </h3>
                    <p className="text-xs text-slate-500 mt-1 font-mono">MFT Record: 49212 | Size: 1.2 MB | C:\Temp\malware.exe</p>
                </div>
                <div className="flex items-center gap-2 bg-slate-950 px-3 py-1 rounded border border-slate-800 font-mono text-xs text-slate-400">
                    <Binary size={14} /> HEX VIEW
                </div>
            </div>
            <div className="flex-1 p-6 overflow-y-auto bg-slate-950 font-mono text-sm leading-relaxed">
                <div className="flex gap-8 text-slate-500">
                    <div className="flex flex-col text-slate-600 select-none">
                        <span>00000000</span>
                        <span>00000010</span>
                        <span>00000020</span>
                        <span>00000030</span>
                    </div>
                    <div className="flex flex-col text-emerald-400/70">
                        <span>4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00</span>
                        <span>B8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00</span>
                        <span>00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00</span>
                        <span>00 00 00 00 00 00 00 00 00 00 00 00 80 00 00 00</span>
                    </div>
                    <div className="flex flex-col text-slate-400 hidden lg:flex">
                        <span>MZ..........ÿÿ..</span>
                        <span>¸.......@.......</span>
                        <span>................</span>
                        <span>............€...</span>
                    </div>
                </div>
            </div>
        </div>

    </div>
  );
}

function TreeItem({ icon, text, danger, warning }: any) {
    let colorClass = 'text-slate-300';
    if (danger) colorClass = 'text-rose-400 font-bold';
    if (warning) colorClass = 'text-amber-400 italic';
    
    return (
        <div className="flex items-center gap-2 cursor-pointer hover:bg-slate-800/50 py-1 px-2 rounded group">
            {icon}
            <span className={colorClass}>{text}</span>
        </div>
    );
}
