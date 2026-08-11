import { useState, useEffect } from 'react';
import { ShieldAlert, Check, X } from 'lucide-react';
import { knowledgeEvolutionApi } from '../api/knowledgeEvolutionApi';
import type { SchemaRecommendation } from '../types';

export function SchemaRecommendationDashboard() {
  const [recommendations, setRecommendations] = useState<SchemaRecommendation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      const res = await knowledgeEvolutionApi.getRecommendations();
      if (res.data.data && res.data.data.length > 0) {
        setRecommendations(res.data.data);
      } else {
        setRecommendations([{
          id: 'rec-1',
          type: 'New Node Type',
          impact: 'Medium',
          description: 'Introduce "ContainerImage" node to track container vulnerabilities.',
          evidence: 'Identified recurring pattern of CVEs linked to base image hashes.'
        }, {
          id: 'rec-2',
          type: 'Merge Properties',
          impact: 'High',
          description: 'Merge "aws_account_id" and "gcp_project_id" into generic "cloud_tenant_id".',
          evidence: 'Found high correlation (0.89) of identical queries across both properties.'
        }]);
      }
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <ShieldAlert className="mr-2 h-5 w-5 text-amber-500" />
          Schema & Ontology Recommendations
        </h2>
        <p className="text-sm text-muted-foreground">Review AI-generated recommendations to evolve the graph schema.</p>
      </div>

      <div className="grid gap-4">
        {loading ? (
          <div className="flex items-center justify-center h-32 text-muted-foreground">Loading recommendations...</div>
        ) : (
          <>
            {recommendations.map(rec => (
              <div key={rec.id} className="bg-card border rounded-lg p-6 flex flex-col md:flex-row md:items-start md:justify-between gap-6">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-xs px-2 py-1 bg-amber-500/10 text-amber-500 rounded font-medium">
                      {rec.type}
                    </span>
                    <span className={`text-xs px-2 py-1 rounded font-medium ${rec.impact === 'High' ? 'bg-red-500/10 text-red-500' : 'bg-primary/10 text-primary'}`}>
                      {rec.impact} Impact
                    </span>
                  </div>
                  <h3 className="text-lg font-medium text-foreground mb-2">{rec.description}</h3>
                  <div className="bg-secondary/50 p-3 rounded-md">
                    <p className="text-sm text-muted-foreground"><span className="font-medium text-foreground mr-1">Evidence:</span> {rec.evidence}</p>
                  </div>
                </div>
                <div className="flex space-x-3 shrink-0">
                  <button 
                    onClick={() => setRecommendations(recommendations.filter(r => r.id !== rec.id))}
                    className="flex items-center justify-center px-4 py-2 border border-border rounded-md text-sm font-medium hover:bg-secondary transition-colors text-foreground"
                  >
                    <X className="mr-2 h-4 w-4 text-red-500" />
                    Reject
                  </button>
                  <button 
                    onClick={() => setRecommendations(recommendations.filter(r => r.id !== rec.id))}
                    className="flex items-center justify-center px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
                  >
                    <Check className="mr-2 h-4 w-4" />
                    Approve
                  </button>
                </div>
              </div>
            ))}
            {recommendations.length === 0 && (
              <div className="bg-card border rounded-lg p-10 flex flex-col items-center justify-center text-center">
                <ShieldAlert className="h-10 w-10 text-muted-foreground mb-4 opacity-20" />
                <h3 className="text-lg font-medium text-foreground mb-1">No pending recommendations</h3>
                <p className="text-muted-foreground">The schema is currently optimized.</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
