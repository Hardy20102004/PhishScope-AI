import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Network, ShieldAlert, GitMerge } from 'lucide-react';

export default function CorrelationExplorer() {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [group, setGroup] = useState<any>(null);

  useEffect(() => {
    if (groupId) {
      apiClient.get(`/alerts/correlations/${groupId}`).then(res => setGroup(res.data)).catch(console.error);
    }
  }, [groupId]);

  if (!group) {
    return <div className="flex items-center justify-center h-full text-slate-400 min-h-screen bg-slate-950">Loading Correlation Data...</div>;
  }

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/alerts')} className="text-slate-400 hover:text-white hover:bg-slate-800">
          <ArrowLeft size={20} />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500 flex items-center gap-3">
            <Network className="text-indigo-500" />
            Correlation Group
          </h1>
          <p className="text-slate-400 mt-2 flex items-center gap-2">
            <GitMerge size={14} />
            Reason: <span className="font-semibold text-slate-300">{group.correlation_reason}</span>
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Col - Group Meta */}
        <div className="space-y-6">
           <Card className="bg-slate-900 border-slate-800 shadow-xl">
             <CardHeader>
              <CardTitle className="text-lg text-slate-200">Group Metadata</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm text-slate-400">Name</p>
                <p className="text-sm font-medium text-slate-200">{group.name}</p>
              </div>
              <div>
                <p className="text-sm text-slate-400">Created At</p>
                <p className="text-sm font-medium text-slate-200">{new Date(group.created_at).toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-slate-400">Total Alerts</p>
                <p className="text-2xl font-bold text-indigo-400">{group.alerts.length}</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Col - Correlated Alerts List */}
        <div className="lg:col-span-3 space-y-4">
          <h2 className="text-xl font-semibold text-slate-200 flex items-center gap-2 mb-4">
            <ShieldAlert size={18} className="text-blue-400" />
            Correlated Alerts
          </h2>
          {group.alerts.map((alert: any) => (
             <Card key={alert.id} className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors shadow-lg cursor-pointer" onClick={() => navigate(`/alerts/${alert.id}`)}>
               <CardContent className="p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
                 <div>
                   <div className="flex items-center gap-3 mb-1">
                      <Badge variant="outline" className={`
                        ${alert.severity === 'CRITICAL' ? 'border-red-500 text-red-400' : ''}
                        ${alert.severity === 'HIGH' ? 'border-orange-500 text-orange-400' : ''}
                        ${alert.severity === 'MEDIUM' ? 'border-yellow-500 text-yellow-400' : ''}
                        ${alert.severity === 'LOW' ? 'border-green-500 text-green-400' : ''}
                      `}>
                        {alert.severity}
                      </Badge>
                      <h3 className="font-semibold text-slate-200">{alert.title}</h3>
                   </div>
                   <p className="text-xs text-slate-400 flex items-center gap-2">
                     <span className="bg-slate-800 px-1.5 rounded">{alert.source}</span>
                     <span>{new Date(alert.created_at).toLocaleString()}</span>
                   </p>
                 </div>
                 
                 <div className="flex items-center gap-6">
                    <div className="text-right">
                      <p className="text-xs text-slate-500">Priority</p>
                      <p className="font-mono text-slate-300">{alert.priority_score.toFixed(0)}</p>
                    </div>
                    <Badge variant="secondary" className="bg-slate-800 text-slate-300">
                      {alert.status}
                    </Badge>
                 </div>
               </CardContent>
             </Card>
          ))}
          
          {group.alerts.length === 0 && (
            <div className="p-8 text-center border border-dashed border-slate-700 rounded-xl text-slate-500">
              No alerts found in this correlation group.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
