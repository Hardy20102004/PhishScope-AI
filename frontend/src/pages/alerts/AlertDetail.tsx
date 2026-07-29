import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { ArrowLeft, BrainCircuit, Network, ShieldCheck, Activity, Users, Clock } from 'lucide-react';

export default function AlertDetail() {
  const { alertId } = useParams();
  const navigate = useNavigate();
  const [alert, setAlert] = useState<any>(null);
  const [auditTrail, setAuditTrail] = useState<any[]>([]);

  useEffect(() => {
    if (alertId) {
      apiClient.get(`/alerts/${alertId}`).then(res => setAlert(res.data)).catch(console.error);
      apiClient.get(`/alerts/${alertId}/audit`).then(res => setAuditTrail(res.data)).catch(console.error);
    }
  }, [alertId]);

  if (!alert) {
    return <div className="flex items-center justify-center h-full text-slate-400 min-h-screen bg-slate-950">Loading Alert Details...</div>;
  }

  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={() => navigate('/alerts')} className="text-slate-400 hover:text-white hover:bg-slate-800">
            <ArrowLeft size={20} />
          </Button>
          <div>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-2xl font-bold text-slate-100">{alert.title}</h1>
              <Badge variant="outline" className={`
                  ${alert.severity === 'CRITICAL' ? 'border-red-500 text-red-400' : ''}
                  ${alert.severity === 'HIGH' ? 'border-orange-500 text-orange-400' : ''}
                  ${alert.severity === 'MEDIUM' ? 'border-yellow-500 text-yellow-400' : ''}
                  ${alert.severity === 'LOW' ? 'border-green-500 text-green-400' : ''}
                `}>
                {alert.severity}
              </Badge>
            </div>
            <p className="text-slate-400 text-sm flex items-center gap-2">
              <span className="bg-slate-800 px-2 py-0.5 rounded text-xs">{alert.source}</span>
              <span>ID: {alert.id.substring(0, 8)}...</span>
              <span>•</span>
              <Clock size={12}/>
              <span>{new Date(alert.created_at).toLocaleString()}</span>
            </p>
          </div>
        </div>
        
        <div className="flex gap-2">
           <Button className="bg-slate-800 hover:bg-slate-700 text-white">
            <Users size={16} className="mr-2" />
            Assign to Me
          </Button>
          <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-[0_0_15px_rgba(79,70,229,0.3)]">
            <BrainCircuit size={16} className="mr-2" />
            AI Investigate
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Core Info */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="bg-slate-900 border-slate-800 shadow-xl">
            <CardHeader>
              <CardTitle className="text-lg text-slate-200">Alert Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-slate-300 leading-relaxed">
                {alert.description || "No description provided by source."}
              </p>
              {alert.ai_summary && (
                <div className="mt-6 p-4 rounded-lg bg-indigo-950/30 border border-indigo-500/20">
                  <div className="flex items-center gap-2 text-indigo-400 font-semibold mb-2">
                    <BrainCircuit size={18} />
                    AI Context & Summary
                  </div>
                  <p className="text-slate-300 text-sm leading-relaxed">{alert.ai_summary}</p>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-slate-900 border-slate-800 shadow-xl">
            <CardHeader>
              <CardTitle className="text-lg text-slate-200 flex items-center gap-2">
                <Network size={18} className="text-blue-400" />
                Evidence & Indicators
              </CardTitle>
            </CardHeader>
            <CardContent>
              {alert.evidence?.length > 0 ? (
                <div className="space-y-3">
                  {alert.evidence.map((ev: any) => (
                    <div key={ev.id} className="flex items-center justify-between p-3 rounded-md bg-slate-950 border border-slate-800 group hover:border-slate-700 transition-colors">
                      <div className="flex items-center gap-3">
                        <Badge className="bg-slate-800 hover:bg-slate-700 text-slate-300">{ev.evidence_type}</Badge>
                        <span className="font-mono text-slate-300 text-sm group-hover:text-white transition-colors">{ev.value}</span>
                      </div>
                      <Button variant="ghost" size="sm" className="text-xs text-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity">
                        Query Graph
                      </Button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-500 italic">No IOCs or evidence attached to this alert.</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Meta & Lifecycle */}
        <div className="space-y-6">
          <Card className="bg-slate-900 border-slate-800 shadow-xl">
             <CardHeader>
              <CardTitle className="text-lg text-slate-200">Risk & Priority</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm text-slate-400">Priority Score</span>
                  <span className="text-sm font-bold text-slate-200">{alert.priority_score.toFixed(0)}</span>
                </div>
                <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-red-500" style={{ width: `${alert.priority_score}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm text-slate-400">Threat Confidence</span>
                  <span className="text-sm font-bold text-slate-200">{alert.confidence.toFixed(0)}</span>
                </div>
                <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500" style={{ width: `${alert.confidence}%` }} />
                </div>
              </div>
              
              {alert.mitre_techniques && (
                <div className="pt-4 border-t border-slate-800">
                  <h4 className="text-sm font-medium text-slate-400 mb-3">MITRE ATT&CK</h4>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(alert.mitre_techniques).map(([tid, name]) => (
                      <Badge key={tid} variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800 cursor-default">
                        {tid}: {String(name)}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-slate-900 border-slate-800 shadow-xl">
             <CardHeader>
              <CardTitle className="text-lg text-slate-200 flex items-center gap-2">
                <Activity size={18} className="text-green-400" />
                Audit Trail
              </CardTitle>
            </CardHeader>
            <CardContent>
               <div className="relative border-l border-slate-800 ml-3 space-y-4 pb-2">
                {auditTrail.map((log: any, idx) => (
                  <div key={log.id} className="relative pl-6">
                    <div className="absolute w-3 h-3 bg-indigo-500 rounded-full -left-[6.5px] top-1 ring-4 ring-slate-900"></div>
                    <p className="text-sm text-slate-200">
                      Status changed to <span className="font-semibold text-indigo-400">{log.new_status}</span>
                    </p>
                    <p className="text-xs text-slate-500 mt-1">{new Date(log.changed_at).toLocaleString()}</p>
                    {log.comment && (
                      <div className="mt-2 p-2 bg-slate-950 rounded border border-slate-800 text-xs text-slate-400 italic">
                        "{log.comment}"
                      </div>
                    )}
                  </div>
                ))}
                {auditTrail.length === 0 && (
                  <div className="pl-6 text-sm text-slate-500">No lifecycle events recorded.</div>
                )}
               </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
