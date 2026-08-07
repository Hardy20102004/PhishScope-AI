import { useState, useEffect } from 'react';
import { Network, Search, Filter } from 'lucide-react';
import { knowledgeEvolutionApi } from '../api/knowledgeEvolutionApi';
import type {  DiscoveredRelationship  } from "../types";

export function RelationshipExplorer() {
  const [relationships, setRelationships] = useState<DiscoveredRelationship[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRelationships();
  }, []);

  const loadRelationships = async () => {
    try {
      setLoading(true);
      const res = await knowledgeEvolutionApi.discoverRelationships();
      setRelationships(res.data.data || []);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500 h-full flex flex-col">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold flex items-center">
            <Network className="mr-2 h-5 w-5 text-primary" />
            Relationship Explorer
          </h2>
          <p className="text-sm text-muted-foreground">Discover and validate inferred relationships.</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <input type="text" placeholder="Search relationships..." className="pl-9 pr-4 py-2 bg-secondary border-none rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary w-64" />
          </div>
          <button className="p-2 bg-secondary text-foreground rounded-md hover:bg-secondary/80 transition-colors">
            <Filter className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 bg-card border rounded-lg p-0 overflow-hidden flex flex-col">
        {loading ? (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">Analyzing graph relationships...</div>
        ) : (
          <div className="overflow-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-muted-foreground uppercase bg-secondary/50 sticky top-0">
                <tr>
                  <th className="px-6 py-3 font-medium">Source</th>
                  <th className="px-6 py-3 font-medium">Relationship</th>
                  <th className="px-6 py-3 font-medium">Target</th>
                  <th className="px-6 py-3 font-medium">Confidence</th>
                  <th className="px-6 py-3 font-medium">Evidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {relationships.map((rel, idx) => (
                  <tr key={idx} className="hover:bg-muted/50 transition-colors">
                    <td className="px-6 py-4 font-medium text-foreground">{rel.source_entity}</td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 bg-primary/10 text-primary rounded text-xs font-mono">
                        [{rel.relationship_type}]
                      </span>
                    </td>
                    <td className="px-6 py-4 font-medium text-foreground">{rel.target_entity}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="w-16 h-2 bg-secondary rounded-full mr-2 overflow-hidden">
                          <div className="h-full bg-emerald-500" style={{ width: `${rel.confidence * 100}%` }}></div>
                        </div>
                        <span>{(rel.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-muted-foreground truncate max-w-xs" title={rel.evidence}>
                      {rel.evidence}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
