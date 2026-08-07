import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, BrainCircuit, Activity, AlertTriangle } from 'lucide-react';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";

export default function GroupedAlertsQueue() {
  const [groups, setGroups] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/ai-triage/groups');
      setGroups(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredGroups = groups.filter(g => g.name.toLowerCase().includes(searchTerm.toLowerCase()));

  const getPriorityColor = (tier: string) => {
      switch(tier) {
          case 'CRITICAL': return 'bg-red-500/20 text-red-400 border-red-500/50';
          case 'HIGH': return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
          case 'MEDIUM': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
          default: return 'bg-slate-800 text-slate-400 border-slate-700';
      }
  };

  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-2">
            <BrainCircuit className="text-violet-500" />
            AI Triage Queue
          </h1>
          <p className="text-slate-400 mt-1">Investigate grouped alerts prioritized by threat severity and business impact.</p>
        </div>
      </div>

      <div className="relative group">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <Search className="w-5 h-5 text-slate-500 group-focus-within:text-violet-400 transition-colors" />
        </div>
        <Input 
          type="text" 
          placeholder="Search clusters by name or reason..." 
          className="pl-10 bg-slate-900 border-slate-800 text-slate-200 focus:border-violet-500 w-full md:w-1/2"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-md overflow-hidden shadow-2xl">
        <Table>
          <TableHeader className="bg-slate-900/80">
            <TableRow className="border-slate-800 hover:bg-transparent">
              <TableHead className="text-slate-400 font-medium w-12">Priority</TableHead>
              <TableHead className="text-slate-400 font-medium">Cluster Name</TableHead>
              <TableHead className="text-slate-400 font-medium">Reasoning</TableHead>
              <TableHead className="text-slate-400 font-medium">Impact Score</TableHead>
              <TableHead className="text-slate-400 font-medium">AI Confidence</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow><TableCell colSpan={5} className="text-center py-10 text-slate-500">Loading clusters...</TableCell></TableRow>
            ) : filteredGroups.length === 0 ? (
              <TableRow><TableCell colSpan={5} className="text-center py-10 text-slate-500">No clusters in queue.</TableCell></TableRow>
            ) : (
              filteredGroups.map((group) => (
                <TableRow key={group.id} className="border-slate-800/50 hover:bg-slate-800/80 transition-colors cursor-pointer" onClick={() => navigate(`/ai-triage/group/${group.id}`)}>
                  <TableCell>
                    <Badge variant="outline" className={getPriorityColor(group.priority_tier)}>
                        {group.priority_tier}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium text-slate-200">{group.name}</TableCell>
                  <TableCell><span className="text-sm text-slate-400">{group.grouping_reason}</span></TableCell>
                  <TableCell>
                      <div className="flex items-center gap-2">
                          <Activity size={14} className={group.business_impact_score > 80 ? 'text-orange-400' : 'text-slate-500'} />
                          <span className={group.business_impact_score > 80 ? 'text-orange-400 font-bold' : 'text-slate-300'}>{group.business_impact_score}</span>
                      </div>
                  </TableCell>
                  <TableCell>
                      <span className="text-violet-400 text-sm font-mono bg-violet-500/10 px-2 py-1 rounded">
                          {(group.confidence * 100).toFixed(1)}%
                      </span>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
