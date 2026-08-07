import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/Card';
import { BrainCircuit, Check, X, ShieldAlert, GitCommit, GitFork, ArrowLeft } from 'lucide-react';
import { apiClient as api } from '@/api/client';
import { Link } from 'react-router-dom';

export const ReasoningViewer: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [decision, setDecision] = useState<any>(null);
  const [comment, setComment] = useState("");
  
  useEffect(() => {
    if (id) fetchDecision(id);
  }, [id]);

  const fetchDecision = async (decisionId: string) => {
    try {
      const res = await api.get(`/decision/${decisionId}`);
      setDecision(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleReview = async (action: 'APPROVE' | 'REJECT') => {
    try {
      await api.post(`/decision/${id}/review`, {
        action,
        comments: comment
      });
      navigate('/decision/approval');
    } catch (err) {
      console.error(err);
    }
  };

  if (!decision) return <div className="p-8 text-white">Loading...</div>;

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <Link to="/decision/approval" className="text-cyan-500 hover:text-cyan-400 flex items-center gap-2 mb-6 transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to Approval Center
      </Link>
      
      <div className="flex justify-between items-start mb-8">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className={`px-2 py-1 rounded text-xs border ${
              decision.state === 'APPROVED' ? 'bg-emerald-900/30 border-emerald-900 text-emerald-400' :
              decision.state === 'REJECTED' ? 'bg-red-900/30 border-red-900 text-red-400' :
              'bg-orange-900/30 border-orange-900 text-orange-400'
            }`}>
              {decision.state}
            </span>
            <span className="text-gray-500 text-sm">{(decision.confidence * 100).toFixed(0)}% Confidence</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white">{decision.decision_type}</h1>
          <p className="text-gray-300 mt-2 max-w-3xl text-lg">{decision.summary}</p>
        </div>
        
        {(decision.state === 'PENDING_REVIEW' || decision.state === 'POLICY_BLOCKED') && (
          <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl w-80 shadow-2xl">
            <h3 className="text-sm font-medium text-white mb-3 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-orange-400" /> Human Review Required
            </h3>
            <textarea
              className="w-full bg-black/50 border border-gray-700 rounded p-2 text-sm text-gray-300 mb-3 focus:outline-none focus:border-cyan-500"
              placeholder="Add optional review comments..."
              rows={3}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            ></textarea>
            <div className="flex gap-2">
              <button onClick={() => handleReview('REJECT')} className="flex-1 bg-red-900/40 hover:bg-red-900/60 text-red-400 border border-red-900/50 py-2 rounded text-sm transition-colors flex justify-center items-center gap-1">
                <X className="w-4 h-4" /> Reject
              </button>
              <button onClick={() => handleReview('APPROVE')} className="flex-1 bg-emerald-900/40 hover:bg-emerald-900/60 text-emerald-400 border border-emerald-900/50 py-2 rounded text-sm transition-colors flex justify-center items-center gap-1">
                <Check className="w-4 h-4" /> Approve
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                <BrainCircuit className="w-5 h-5 text-cyan-400" /> Reasoning Chain
              </h2>
              
              <div className="relative border-l border-gray-700 ml-4 space-y-8">
                {decision.reasoning_chain.map((step: any, idx: number) => (
                  <div key={idx} className="relative pl-6">
                    <div className="absolute w-4 h-4 rounded-full bg-cyan-900 border-2 border-cyan-500 -left-[9px] top-1"></div>
                    <div className="bg-black/30 p-4 rounded-lg border border-gray-800">
                      <p className="text-sm text-gray-400 mb-2 font-mono">STEP {step.step}</p>
                      <p className="text-gray-200 mb-2"><span className="text-cyan-400 font-medium">Observation:</span> {step.observation}</p>
                      <p className="text-gray-200"><span className="text-purple-400 font-medium">Inference:</span> {step.inference}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
        
        <div className="space-y-6">
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-6">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <GitFork className="w-5 h-5 text-purple-400" /> Alternative Hypotheses
              </h2>
              <div className="space-y-4">
                {decision.alternatives.length === 0 ? (
                  <p className="text-sm text-gray-500">No alternatives generated.</p>
                ) : (
                  decision.alternatives.map((alt: any, idx: number) => (
                    <div key={idx} className="bg-purple-900/10 border border-purple-900/30 p-3 rounded text-sm">
                      <p className="text-gray-300 mb-2">{alt.hypothesis}</p>
                      <div className="flex justify-between items-center text-xs text-purple-400">
                        <span>Prob: {(alt.probability * 100).toFixed(0)}%</span>
                        <span className="italic">Missing evidence: {alt.missing_evidence.length}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-6">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <GitCommit className="w-5 h-5 text-orange-400" /> Recommendations
              </h2>
              <ul className="space-y-3 text-sm">
                {decision.recommendations.map((r: any, idx: number) => (
                  <li key={idx} className="bg-black/40 p-3 rounded border border-gray-800 flex items-start gap-2">
                    <Check className={`w-4 h-4 mt-0.5 ${r.priority === 'HIGH' ? 'text-red-400' : 'text-yellow-400'}`} />
                    <div>
                      <p className="text-gray-200 font-medium">{r.action.replace(/_/g, ' ')}</p>
                      <p className="text-gray-400 text-xs mt-1">{r.description}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
