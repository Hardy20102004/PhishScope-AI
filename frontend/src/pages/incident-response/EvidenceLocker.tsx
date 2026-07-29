import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Lock, FileText, ArrowRight, ShieldCheck, Upload } from 'lucide-react';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";

export default function EvidenceLocker() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="flex justify-between items-end border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Lock className="text-emerald-500" />
                Evidence Locker & Chain of Custody
            </h1>
            <p className="text-slate-400 mt-1">Immutable ledger of digital artifacts logged during INC-2026-084.</p>
          </div>
          <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
              <Upload size={16} className="mr-2" /> Log New Evidence
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
                <Card className="bg-slate-900 border-slate-800 shadow-2xl h-full">
                    <Table>
                      <TableHeader className="bg-slate-900/80">
                        <TableRow className="border-slate-800">
                          <TableHead className="text-slate-400">Type</TableHead>
                          <TableHead className="text-slate-400">Value / Artifact</TableHead>
                          <TableHead className="text-slate-400">Source</TableHead>
                          <TableHead className="text-slate-400 text-right">Integrity Status</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        <TableRow className="border-slate-800/50 hover:bg-slate-800/80 cursor-pointer">
                          <TableCell><Badge variant="outline" className="text-blue-400 border-blue-400/50">MEMORY_DUMP</Badge></TableCell>
                          <TableCell className="font-mono text-xs text-slate-300">hr-05-memdump.raw</TableCell>
                          <TableCell className="text-sm text-slate-400">Velociraptor Agent</TableCell>
                          <TableCell className="text-right">
                              <span className="inline-flex items-center gap-1 text-emerald-400 text-xs font-semibold bg-emerald-500/10 px-2 py-1 rounded">
                                  <ShieldCheck size={12} /> Verified
                              </span>
                          </TableCell>
                        </TableRow>
                        <TableRow className="border-slate-800/50 hover:bg-slate-800/80 cursor-pointer bg-slate-800/30">
                          <TableCell><Badge variant="outline" className="text-orange-400 border-orange-400/50">FILE_HASH</Badge></TableCell>
                          <TableCell className="font-mono text-xs text-slate-300">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</TableCell>
                          <TableCell className="text-sm text-slate-400">EDR Alert 9942</TableCell>
                          <TableCell className="text-right">
                              <span className="inline-flex items-center gap-1 text-emerald-400 text-xs font-semibold bg-emerald-500/10 px-2 py-1 rounded">
                                  <ShieldCheck size={12} /> Verified
                              </span>
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                </Card>
            </div>
            
            <div>
                <Card className="bg-slate-900 border-slate-800">
                    <CardHeader>
                        <CardTitle className="text-sm text-slate-200">Chain of Custody Audit Log</CardTitle>
                        <CardDescription className="text-xs text-slate-500">Selected: FILE_HASH (e3b0...)</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="relative border-l border-slate-700 ml-3 space-y-6">
                            <div className="pl-6 relative">
                                <div className="absolute w-3 h-3 bg-emerald-500 rounded-full -left-1.5 top-1"></div>
                                <h4 className="text-xs font-bold text-slate-200">COLLECTED</h4>
                                <p className="text-xs text-slate-500 mt-1">Today, 08:15 UTC by System</p>
                                <div className="mt-2 bg-slate-950 p-2 rounded border border-slate-800">
                                    <p className="text-[10px] text-slate-500 font-mono">SHA256 Signature:</p>
                                    <p className="text-[10px] text-emerald-400 font-mono break-all">a423f0343a...8f949b</p>
                                </div>
                            </div>
                            <div className="pl-6 relative">
                                <div className="absolute w-3 h-3 bg-blue-500 rounded-full -left-1.5 top-1"></div>
                                <h4 className="text-xs font-bold text-slate-200">TRANSFERRED</h4>
                                <p className="text-xs text-slate-500 mt-1">Today, 09:00 UTC by Jane Doe</p>
                                <p className="text-xs text-slate-400 mt-1 italic">"Transferred to Sandbox for detonation."</p>
                                <div className="mt-2 bg-slate-950 p-2 rounded border border-slate-800">
                                    <p className="text-[10px] text-slate-500 font-mono">SHA256 Verified Match:</p>
                                    <p className="text-[10px] text-emerald-400 font-mono break-all">a423f0343a...8f949b</p>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </div>
  );
}
