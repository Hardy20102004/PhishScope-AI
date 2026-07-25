import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { ShieldAlert, AlertTriangle, Check, FileSearch } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiClient as api } from '@/api/client';

export const ApprovalCenter: React.FC = () => {
  const [pending, setPending] = useState<any[]>([]);
  
  useEffect(() => {
    fetchPending();
  }, []);

  const fetchPending = async () => {
    try {
      const res = await api.get('/decision/');
      setPending(res.data.filter((d: any) => d.state === 'PENDING_REVIEW' || d.state === 'POLICY_BLOCKED'));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-orange-500" />
            Approval Center
          </h1>
          <p className="text-gray-400 mt-2 max-w-3xl">
            Review decisions blocked by organizational policy or requiring explicit human oversight.
          </p>
        </div>
        <button 
          className="bg-gray-800 hover:bg-gray-700 border border-gray-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors"
          onClick={() => {
            // Trigger a mock evaluation for demonstration
            api.post('/decision/evaluate', {
              decision_type: "THREAT_CLASSIFICATION",
              summary: "Requesting classification",
              confidence: 0,
              evidence: [
                { source_type: "KNOWLEDGE_GRAPH", source_id: "ip_123" }
              ]
            }).then(() => fetchPending());
          }}
        >
          <AlertTriangle className="w-5 h-5 text-yellow-400" /> Simulate High-Risk Decision
        </button>
      </div>

      <div className="space-y-4">
        {pending.length === 0 ? (
          <div className="text-center py-12 text-gray-500 bg-gray-900/50 rounded-lg border border-gray-800 border-dashed">
            <Check className="w-12 h-12 text-emerald-500/50 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-400">All clear!</h3>
            <p>No decisions are currently pending review.</p>
          </div>
        ) : (
          pending.map((d) => (
            <Card key={d.id} className="bg-gray-900 border-orange-900/50 shadow-lg relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-orange-500"></div>
              <CardContent className="p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="bg-orange-900/30 text-orange-400 px-2 py-0.5 rounded text-xs border border-orange-900">
                        {d.state}
                      </span>
                      <span className="text-xs text-gray-500 font-mono">ID: {d.id}</span>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">{d.decision_type}</h3>
                    <p className="text-gray-300 mb-4">{d.summary}</p>
                    
                    <div className="flex gap-4 mb-4">
                      <div className="bg-black/30 p-3 rounded-lg border border-gray-800">
                        <p className="text-xs text-gray-500 mb-1">Confidence Score</p>
                        <p className="text-lg font-semibold text-white">{(d.confidence * 100).toFixed(0)}%</p>
                      </div>
                      <div className="bg-black/30 p-3 rounded-lg border border-gray-800">
                        <p className="text-xs text-gray-500 mb-1">Recommendations</p>
                        <ul className="text-sm text-gray-300 list-disc list-inside">
                          {d.recommendations.map((r: any, i: number) => (
                            <li key={i}>{r.action}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex flex-col gap-2 min-w-[140px]">
                    <Link 
                      to={`/decision/view/${d.id}`}
                      className="w-full bg-gray-800 hover:bg-gray-700 text-white px-3 py-2 rounded flex justify-center items-center gap-2 text-sm transition-colors border border-gray-700"
                    >
                      <FileSearch className="w-4 h-4" /> View Reasoning
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};
