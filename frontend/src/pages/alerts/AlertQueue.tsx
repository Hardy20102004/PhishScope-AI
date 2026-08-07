import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Filter, ShieldAlert, ArrowRight, Activity, Search } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function AlertQueue() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/alerts?limit=50');
      setAlerts(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredAlerts = alerts.filter(alert => 
    alert.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    alert.source.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500 flex items-center gap-2">
            <ShieldAlert className="text-indigo-500" />
            Alert Queue
          </h1>
          <p className="text-slate-400 mt-1">Triage and investigate active enterprise security alerts.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" className="border-slate-700 hover:bg-slate-800 text-slate-300">
            <Filter size={16} className="mr-2" />
            Saved Views
          </Button>
          <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">
            <Activity size={16} className="mr-2" />
            Bulk Actions
          </Button>
        </div>
      </div>

      <div className="relative group">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <Search className="w-5 h-5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
        </div>
        <Input 
          type="text" 
          placeholder="Search alerts by title, source, or IOC..." 
          className="pl-10 bg-slate-900 border-slate-800 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 w-full md:w-1/2 lg:w-1/3 transition-all"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-md overflow-hidden shadow-2xl">
        <Table>
          <TableHeader className="bg-slate-900/80">
            <TableRow className="border-slate-800 hover:bg-transparent">
              <TableHead className="text-slate-400 font-medium">Severity</TableHead>
              <TableHead className="text-slate-400 font-medium">Title</TableHead>
              <TableHead className="text-slate-400 font-medium">Source</TableHead>
              <TableHead className="text-slate-400 font-medium">Status</TableHead>
              <TableHead className="text-slate-400 font-medium">Score</TableHead>
              <TableHead className="text-slate-400 font-medium text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-slate-500">
                  Loading alerts...
                </TableCell>
              </TableRow>
            ) : filteredAlerts.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-slate-500">
                  No alerts found.
                </TableCell>
              </TableRow>
            ) : (
              filteredAlerts.map((alert) => (
                <TableRow key={alert.id} className="border-slate-800/50 hover:bg-slate-800/50 transition-colors cursor-pointer" onClick={() => navigate(`/alerts/${alert.id}`)}>
                  <TableCell>
                    <Badge variant="outline" className={`
                      ${alert.severity === 'CRITICAL' ? 'border-red-500 text-red-400 shadow-[0_0_8px_rgba(239,68,68,0.2)]' : ''}
                      ${alert.severity === 'HIGH' ? 'border-orange-500 text-orange-400' : ''}
                      ${alert.severity === 'MEDIUM' ? 'border-yellow-500 text-yellow-400' : ''}
                      ${alert.severity === 'LOW' ? 'border-green-500 text-green-400' : ''}
                    `}>
                      {alert.severity}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium text-slate-200">{alert.title}</TableCell>
                  <TableCell className="text-slate-400">{alert.source}</TableCell>
                  <TableCell>
                     <Badge variant="secondary" className="bg-slate-800 text-slate-300 hover:bg-slate-700">
                      {alert.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-16 bg-slate-800 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full ${alert.priority_score > 80 ? 'bg-red-500' : alert.priority_score > 50 ? 'bg-orange-500' : 'bg-blue-500'}`} 
                          style={{ width: `${alert.priority_score}%` }} 
                        />
                      </div>
                      <span className="text-xs text-slate-400">{alert.priority_score.toFixed(0)}</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" className="text-slate-400 hover:text-indigo-400 hover:bg-indigo-500/10">
                      Investigate <ArrowRight size={14} className="ml-1" />
                    </Button>
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
