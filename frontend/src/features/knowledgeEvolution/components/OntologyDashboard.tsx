import { useState, useEffect } from 'react';
import { Database, Plus, CheckCircle, Clock } from 'lucide-react';
import { knowledgeEvolutionApi } from '../api/knowledgeEvolutionApi';
import type {  OntologyNode  } from "../types";

export function OntologyDashboard() {
  const [nodes, setNodes] = useState<OntologyNode[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadNodes();
  }, []);

  const loadNodes = async () => {
    try {
      setLoading(true);
      // Simulate API call for now to avoid breaking if backend isn't up
      // const res = await knowledgeEvolutionApi.getOntologyNodes();
      // setNodes(res.data.data);
      setTimeout(() => {
        setNodes([
          {
            id: '1', name: 'Threat Actor', type: 'ENTITY_TYPE', description: 'Entity representing a cyber adversary',
            properties: {}, schema_version: '1.0', status: 'APPROVED', created_at: new Date().toISOString(), updated_at: new Date().toISOString()
          },
          {
            id: '2', name: 'TARGETS', type: 'RELATIONSHIP_TYPE', description: 'Adversary targeting a specific asset',
            properties: {}, schema_version: '1.0', status: 'PENDING', created_at: new Date().toISOString(), updated_at: new Date().toISOString()
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold flex items-center">
            <Database className="mr-2 h-5 w-5 text-primary" />
            Ontology Management
          </h2>
          <p className="text-sm text-muted-foreground">Manage entity types, relationships, and semantic models.</p>
        </div>
        <button className="flex items-center px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors">
          <Plus className="mr-2 h-4 w-4" />
          Create Node Type
        </button>
      </div>

      <div className="grid gap-4">
        {loading ? (
          <div className="h-32 flex items-center justify-center text-muted-foreground">Loading ontology nodes...</div>
        ) : (
          nodes.map(node => (
            <div key={node.id} className="bg-card border rounded-lg p-5 flex justify-between items-center hover:border-primary/50 transition-colors group">
              <div>
                <div className="flex items-center space-x-3 mb-1">
                  <h3 className="font-medium text-foreground">{node.name}</h3>
                  <span className="text-xs px-2 py-0.5 rounded bg-secondary text-secondary-foreground font-medium">
                    {node.type}
                  </span>
                  {node.status === 'APPROVED' ? (
                    <span className="flex items-center text-xs text-emerald-500 font-medium">
                      <CheckCircle className="mr-1 h-3 w-3" /> Approved
                    </span>
                  ) : (
                    <span className="flex items-center text-xs text-amber-500 font-medium">
                      <Clock className="mr-1 h-3 w-3" /> Pending Review
                    </span>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">{node.description}</p>
              </div>
              <div className="text-sm text-muted-foreground">
                v{node.schema_version}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
