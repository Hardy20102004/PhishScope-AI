import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Filter, Search, FileCode, CheckCircle, Clock } from 'lucide-react';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";

export default function RuleExplorer() {
  const [rules, setRules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchRules();
  }, []);

  const fetchRules = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/detection');
      setRules(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredRules = rules.filter(r => r.name.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-2">
            <FileCode className="text-emerald-500" />
            Rule Registry
          </h1>
          <p className="text-slate-400 mt-1">Explore and manage enterprise detection content.</p>
        </div>
        <Button onClick={() => navigate('/detection/editor')} className="bg-emerald-600 hover:bg-emerald-700 text-white">
          Create New Rule
        </Button>
      </div>

      <div className="relative group">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <Search className="w-5 h-5 text-slate-500 group-focus-within:text-emerald-400 transition-colors" />
        </div>
        <Input 
          type="text" 
          placeholder="Search rules by name, MITRE technique, or tags..." 
          className="pl-10 bg-slate-900 border-slate-800 text-slate-200 focus:border-emerald-500 w-full md:w-1/2"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-md overflow-hidden shadow-2xl">
        <Table>
          <TableHeader className="bg-slate-900/80">
            <TableRow className="border-slate-800 hover:bg-transparent">
              <TableHead className="text-slate-400 font-medium">Name</TableHead>
              <TableHead className="text-slate-400 font-medium">Type</TableHead>
              <TableHead className="text-slate-400 font-medium">Severity</TableHead>
              <TableHead className="text-slate-400 font-medium">Status</TableHead>
              <TableHead className="text-slate-400 font-medium text-right">Version</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow><TableCell colSpan={5} className="text-center py-10 text-slate-500">Loading rules...</TableCell></TableRow>
            ) : filteredRules.length === 0 ? (
              <TableRow><TableCell colSpan={5} className="text-center py-10 text-slate-500">No rules found.</TableCell></TableRow>
            ) : (
              filteredRules.map((rule) => (
                <TableRow key={rule.id} className="border-slate-800/50 hover:bg-slate-800/50 transition-colors cursor-pointer" onClick={() => navigate(`/detection/editor?id=${rule.id}`)}>
                  <TableCell className="font-medium text-slate-200">{rule.name}</TableCell>
                  <TableCell><Badge variant="outline" className="border-slate-700 text-slate-300">{rule.rule_type}</Badge></TableCell>
                  <TableCell>
                    <span className={`text-sm ${rule.severity === 'CRITICAL' ? 'text-red-400' : rule.severity === 'HIGH' ? 'text-orange-400' : 'text-yellow-400'}`}>
                      {rule.severity}
                    </span>
                  </TableCell>
                  <TableCell>
                     <Badge variant="secondary" className={`
                        ${rule.status === 'APPROVED' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-400'}
                     `}>
                      {rule.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right text-slate-400 font-mono">v{rule.current_version}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
