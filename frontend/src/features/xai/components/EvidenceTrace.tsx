import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient as api } from '@/api/client';
import { ArrowLeft, GitBranch, Target, Layers } from 'lucide-react';
import { NarrativeViewer } from './NarrativeViewer';
import { Card, CardContent } from '@/components/ui/Card';

export const EvidenceTrace: React.FC = () => {
  const { decisionId } = useParams();
  const [explanation, setExplanation] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  useEffect(() => {
    if (decisionId) {
      fetchExplanation(decisionId);
    }
  }, [decisionId]);

  const fetchExplanation = async (id: string) => {
    try {
      setLoading(true);
      const res = await api.get(`/xai/${id}`);
      setExplanation(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to load explanation. Make sure the decision exists.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-white">Loading Trace...</div>;
  if (error) return <div className="p-8 text-red-400">{error}</div>;
  if (!explanation) return null;

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <Link to="/xai" className="text-yellow-500 hover:text-yellow-400 flex items-center gap-2 mb-6 transition-colors w-max">
        <ArrowLeft className="w-4 h-4" /> Back to XAI Dashboard
      </Link>
      
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <GitBranch className="w-8 h-8 text-purple-500" />
          Evidence Trace & Attribution
        </h1>
        <p className="text-gray-400 mt-2 font-mono text-sm">Target Decision: {explanation.decision_id}</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6 h-[600px] mb-6">
        <NarrativeViewer 
          executive={explanation.executive_summary} 
          technical={explanation.technical_summary} 
        />
        
        <div className="flex flex-col gap-6 h-full">
          <Card className="bg-gray-900 border-gray-800 flex-1">
            <CardContent className="p-6 h-full flex flex-col">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Target className="w-5 h-5 text-rose-400" /> Confidence Breakdown
              </h2>
              <div className="space-y-4 overflow-y-auto flex-1 pr-2">
                {explanation.confidence_breakdown.map((f: any, idx: number) => (
                  <div key={idx} className="bg-black/40 p-3 rounded-lg border border-gray-800">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-medium text-gray-200">{f.factor}</span>
                      <span className="text-xs bg-rose-900/30 text-rose-400 px-2 py-0.5 rounded border border-rose-900/50">
                        +{(f.impact * 100).toFixed(0)}%
                      </span>
                    </div>
                    <p className="text-xs text-gray-400">{f.description}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-gray-900 border-gray-800 flex-1">
            <CardContent className="p-6 h-full flex flex-col">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-400" /> Feature Ranking
              </h2>
              <div className="space-y-3 overflow-y-auto flex-1 pr-2">
                {explanation.feature_importance.map((feat: any, idx: number) => (
                  <div key={idx} className="flex items-center gap-4 bg-indigo-900/10 border border-indigo-900/30 p-2 rounded">
                    <div className="w-8 h-8 rounded-full bg-indigo-900/50 flex items-center justify-center font-bold text-indigo-400 text-sm">
                      #{feat.rank}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-200">{feat.feature_name}</p>
                      <p className="text-xs text-indigo-400/70">{feat.category}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      
      {/* Attributions Table */}
      <h2 className="text-xl font-semibold mb-4 text-white">Raw Evidence Attributions</h2>
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-400 uppercase bg-gray-800/50">
                <tr>
                  <th className="px-6 py-3 font-medium">Source</th>
                  <th className="px-6 py-3 font-medium">Attribution Details</th>
                  <th className="px-6 py-3 font-medium text-right">Weight</th>
                </tr>
              </thead>
              <tbody>
                {explanation.attributions.length === 0 ? (
                  <tr><td colSpan={3} className="px-6 py-4 text-center text-gray-500">No evidence attributions found.</td></tr>
                ) : (
                  explanation.attributions.map((attr: any) => (
                    <tr key={attr.id} className="border-b border-gray-800 hover:bg-gray-800/30 transition-colors">
                      <td className="px-6 py-4">
                        <span className="bg-gray-800 text-gray-300 px-2 py-1 rounded text-xs border border-gray-700">
                          {attr.source_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-gray-300">
                        {attr.attribution_text}
                        <br/>
                        <span className="text-xs text-gray-500 font-mono mt-1 block">ID: {attr.source_id}</span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <div className="w-24 h-2 bg-gray-800 rounded-full overflow-hidden">
                            <div className="h-full bg-yellow-500" style={{ width: `${attr.importance_weight * 100}%`}}></div>
                          </div>
                          <span className="text-xs text-gray-400 w-8">{(attr.importance_weight * 100).toFixed(0)}%</span>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
