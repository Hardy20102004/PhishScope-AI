import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { BrainCircuit, Target, AlertTriangle, MessageSquare, ThumbsUp, ThumbsDown, CheckCircle } from 'lucide-react';
import { Textarea } from '@/components/ui/textarea';

export default function TriageDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [group, setGroup] = useState<any>(null);
  const [feedbackNotes, setFeedbackNotes] = useState('');

  useEffect(() => {
    // In a real app we'd fetch the specific group. 
    // For this demonstration, we'll hit the /groups endpoint and filter, or use a specific endpoint if one exists.
    // Mocking the fetch for simplicity since we don't have a GET /groups/:id implemented yet.
    setGroup({
        id,
        name: "AI Cluster: LATERAL_MOVEMENT_PATH",
        priority_tier: "HIGH",
        business_impact_score: 95.0,
        recommendation: {
            alert_summary: "AI Analysis indicates a coordinated credential stuffing attack followed by lateral movement attempts via SMB.",
            priority_explanation: "Elevated priority due to target asset hosting the primary Financial SQL Database (High Business Impact).",
            business_impact_summary: "If successful, this could lead to CONFIDENTIAL data exfiltration.",
            investigation_steps: [
                "Isolate the affected host from the internal network.",
                "Review Azure AD logs for successful authentications.",
                "Check for recent lateral movement tools execution."
            ],
            alternative_interpretations: ["Could be an authorized vulnerability scan."],
            ai_confidence_score: 0.88,
            uncertainty_factors: ["Log gap between 02:00 and 02:15 UTC."]
        }
    });
  }, [id]);

  const submitFeedback = async (type: string) => {
    try {
        await apiClient.post(`/ai-triage/groups/${id}/feedback`, {
            feedback_type: type,
            comments: feedbackNotes
        });
        alert(`Feedback '${type}' submitted to Learning Engine.`);
        setFeedbackNotes('');
    } catch (err) {
        console.error(err);
    }
  };

  if (!group) return <div className="p-8 text-slate-100">Loading...</div>;

  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
       <div className="flex justify-between items-start">
           <div>
               <div className="flex items-center gap-3 mb-2">
                   <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/50 hover:bg-orange-500/30">
                       {group.priority_tier} PRIORITY
                   </Badge>
                   <span className="text-slate-500 text-sm font-mono">ID: {group.id}</span>
               </div>
               <h1 className="text-3xl font-bold">{group.name}</h1>
           </div>
           <div className="flex gap-2">
               <Button onClick={() => navigate('/investigation')} className="bg-emerald-600 hover:bg-emerald-700 text-white">
                   Open in Investigation Canvas
               </Button>
           </div>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
           {/* Left Column: AI Recommendations */}
           <div className="lg:col-span-2 space-y-6">
               <Card className="bg-slate-900 border-slate-800 shadow-2xl relative overflow-hidden">
                   <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
                       <BrainCircuit size={120} />
                   </div>
                   <CardHeader>
                       <CardTitle className="text-violet-400 flex items-center gap-2">
                           <BrainCircuit size={20} />
                           AI Executive Summary
                       </CardTitle>
                   </CardHeader>
                   <CardContent className="space-y-4">
                       <div>
                           <h3 className="text-sm font-semibold text-slate-300 mb-1">Alert Summary</h3>
                           <p className="text-slate-400 text-sm leading-relaxed">{group.recommendation.alert_summary}</p>
                       </div>
                       <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-800">
                           <div>
                               <h3 className="text-sm font-semibold text-slate-300 mb-1 flex items-center gap-2">
                                   <Target size={14} className="text-orange-400"/> Priority Justification
                               </h3>
                               <p className="text-slate-400 text-sm leading-relaxed">{group.recommendation.priority_explanation}</p>
                           </div>
                           <div>
                               <h3 className="text-sm font-semibold text-slate-300 mb-1 flex items-center gap-2">
                                   <AlertTriangle size={14} className="text-yellow-400"/> Business Impact
                               </h3>
                               <p className="text-slate-400 text-sm leading-relaxed">{group.recommendation.business_impact_summary}</p>
                           </div>
                       </div>
                   </CardContent>
               </Card>

               <Card className="bg-slate-900 border-slate-800">
                   <CardHeader>
                       <CardTitle className="text-slate-200">Recommended Next Steps</CardTitle>
                   </CardHeader>
                   <CardContent>
                       <ul className="space-y-3">
                           {group.recommendation.investigation_steps.map((step: string, i: number) => (
                               <li key={i} className="flex items-start gap-3 text-sm text-slate-300 bg-slate-950/50 p-3 rounded-lg border border-slate-800/50">
                                   <CheckCircle size={16} className="text-emerald-500 mt-0.5 shrink-0" />
                                   <span>{step}</span>
                               </li>
                           ))}
                       </ul>
                   </CardContent>
               </Card>
           </div>

           {/* Right Column: Context & Feedback */}
           <div className="space-y-6">
               <Card className="bg-slate-900 border-slate-800">
                   <CardHeader>
                       <CardTitle className="text-sm text-slate-300">Confidence & Uncertainty</CardTitle>
                   </CardHeader>
                   <CardContent>
                       <div className="mb-4">
                           <div className="flex justify-between text-xs text-slate-400 mb-1">
                               <span>AI Confidence</span>
                               <span className="text-violet-400">{(group.recommendation.ai_confidence_score * 100)}%</span>
                           </div>
                           <div className="w-full bg-slate-950 rounded-full h-1.5">
                               <div className="bg-violet-500 h-1.5 rounded-full" style={{width: `${group.recommendation.ai_confidence_score * 100}%`}}></div>
                           </div>
                       </div>
                       <div>
                           <span className="text-xs font-semibold text-slate-500">Uncertainty Factors:</span>
                           <ul className="mt-2 space-y-1">
                               {group.recommendation.uncertainty_factors.map((f: string, i: number) => (
                                   <li key={i} className="text-xs text-slate-400 flex items-center gap-2">
                                       <span className="w-1 h-1 rounded-full bg-yellow-500"></span>
                                       {f}
                                   </li>
                               ))}
                           </ul>
                       </div>
                   </CardContent>
               </Card>

               <Card className="bg-indigo-950/20 border-indigo-500/20">
                   <CardHeader>
                       <CardTitle className="text-sm text-indigo-400 flex items-center gap-2">
                           <MessageSquare size={16} />
                           Analyst Feedback Loop
                       </CardTitle>
                       <CardDescription className="text-xs text-indigo-300/60">
                           Train the AI by correcting its triage logic.
                       </CardDescription>
                   </CardHeader>
                   <CardContent className="space-y-4">
                       <Textarea 
                           placeholder="Optional reasoning..." 
                           className="bg-slate-950 border-indigo-500/20 text-sm focus-visible:ring-indigo-500"
                           value={feedbackNotes}
                           onChange={e => setFeedbackNotes(e.target.value)}
                       />
                       <div className="grid grid-cols-2 gap-2">
                           <Button onClick={() => submitFeedback('TRUE_POSITIVE')} variant="outline" className="bg-emerald-950/30 border-emerald-500/30 text-emerald-400 hover:bg-emerald-900/50">
                               <ThumbsUp size={14} className="mr-2" /> True Positive
                           </Button>
                           <Button onClick={() => submitFeedback('FALSE_POSITIVE')} variant="outline" className="bg-red-950/30 border-red-500/30 text-red-400 hover:bg-red-900/50">
                               <ThumbsDown size={14} className="mr-2" /> False Positive
                           </Button>
                       </div>
                   </CardContent>
               </Card>
           </div>
       </div>
    </div>
  );
}
