import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Play, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";

export default function TestingDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-2">
            <Play className="text-cyan-500" />
            Detection Testing Suite
          </h1>
          <p className="text-slate-400 mt-1">Run regression tests against historical and synthetic datasets.</p>
        </div>
        <Button className="bg-cyan-600 hover:bg-cyan-700 text-white">
          <Play size={16} className="mr-2 fill-current" />
          Run All Suites
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
         <Card className="bg-slate-900 border-slate-800">
           <CardContent className="p-6 text-center">
             <div className="text-4xl font-bold text-emerald-400 mb-2">94.2%</div>
             <p className="text-sm text-slate-400">Global Coverage Score</p>
           </CardContent>
         </Card>
         <Card className="bg-slate-900 border-slate-800">
           <CardContent className="p-6 text-center">
             <div className="text-4xl font-bold text-red-400 mb-2">12</div>
             <p className="text-sm text-slate-400">False Positives (Last 30d)</p>
           </CardContent>
         </Card>
         <Card className="bg-slate-900 border-slate-800">
           <CardContent className="p-6 text-center">
             <div className="text-4xl font-bold text-orange-400 mb-2">3</div>
             <p className="text-sm text-slate-400">Rules Failing Tests</p>
           </CardContent>
         </Card>
      </div>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-slate-200">Recent Test Runs</CardTitle>
        </CardHeader>
        <CardContent>
           <Table>
            <TableHeader className="bg-slate-950">
              <TableRow className="border-slate-800">
                <TableHead className="text-slate-400">Rule Name</TableHead>
                <TableHead className="text-slate-400">Dataset</TableHead>
                <TableHead className="text-slate-400">Coverage</TableHead>
                <TableHead className="text-slate-400">FP / FN</TableHead>
                <TableHead className="text-slate-400">Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow className="border-slate-800/50 hover:bg-slate-800/50 transition-colors">
                <TableCell className="font-medium text-slate-200">Suspicious PowerShell Download</TableCell>
                <TableCell className="text-slate-400">APT32 Historical</TableCell>
                <TableCell className="text-emerald-400">98%</TableCell>
                <TableCell className="text-slate-400">0 / 0</TableCell>
                <TableCell><Badge className="bg-emerald-500/20 text-emerald-400 border-0"><CheckCircle size={14} className="mr-1"/> Passed</Badge></TableCell>
              </TableRow>
              <TableRow className="border-slate-800/50 hover:bg-slate-800/50 transition-colors">
                <TableCell className="font-medium text-slate-200">Mimikatz LSASS Access</TableCell>
                <TableCell className="text-slate-400">Synthetic Ransomware</TableCell>
                <TableCell className="text-emerald-400">100%</TableCell>
                <TableCell className="text-slate-400">0 / 0</TableCell>
                <TableCell><Badge className="bg-emerald-500/20 text-emerald-400 border-0"><CheckCircle size={14} className="mr-1"/> Passed</Badge></TableCell>
              </TableRow>
              <TableRow className="border-slate-800/50 hover:bg-slate-800/50 transition-colors">
                <TableCell className="font-medium text-slate-200">Abnormal SMB Traffic</TableCell>
                <TableCell className="text-slate-400">Enterprise Baseline 2026</TableCell>
                <TableCell className="text-orange-400">72%</TableCell>
                <TableCell className="text-red-400 font-bold">14 / 2</TableCell>
                <TableCell><Badge className="bg-red-500/20 text-red-400 border-0"><XCircle size={14} className="mr-1"/> Failed</Badge></TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
