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
      const res = await knowledgeEvolutionApi.getOntologyNodes();
      if (res.data.data && res.data.data.length > 0) {
        setNodes(res.data.data);
      } else {
        setNodes([{
          id: 'node-1',
          name: 'Threat Actor',
          type: 'ENTITY_TYPE',
          description: 'Represents an adversary or group responsible for an incident.',
          schema_version: '1.2',
          status: 'APPROVED',
          properties: {}
        }, {
          id: 'node-2',
          name: 'Compromised Credential',
          type: 'ENTITY_TYPE',
          description: 'Leaked or stolen authentication tokens and passwords.',
          schema_version: '1.0',
          status: 'PENDING',
          properties: {}
        }]);
      }
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  const [showCreate, setShowCreate] = useState(false);
  const [newNode, setNewNode] = useState({ name: '', type: 'ENTITY_TYPE', description: '' });

  const handleCreate = async () => {
    try {
      if (!newNode.name || !newNode.description) return;
      await knowledgeEvolutionApi.createOntologyNode({
        name: newNode.name,
        type: newNode.type,
        description: newNode.description,
        schema_version: '1.0',
        properties: {}
      });
      setShowCreate(false);
      setNewNode({ name: '', type: 'ENTITY_TYPE', description: '' });
      loadNodes();
    } catch (error) {
      console.error('Failed to create node', error);
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
        <button 
          onClick={() => setShowCreate(!showCreate)}
          className="flex items-center px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
        >
          <Plus className="mr-2 h-4 w-4" />
          {showCreate ? 'Cancel' : 'Create Node Type'}
        </button>
      </div>

      {showCreate && (
        <div className="bg-card border rounded-lg p-5 space-y-4">
          <h3 className="font-medium text-foreground">Create New Node Type</h3>
          <div className="grid grid-cols-2 gap-4">
            <input 
              placeholder="Name (e.g. Threat Actor)" 
              value={newNode.name}
              onChange={(e) => setNewNode({...newNode, name: e.target.value})}
              className="px-3 py-2 bg-secondary border-none rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <select 
              value={newNode.type}
              onChange={(e) => setNewNode({...newNode, type: e.target.value})}
              className="px-3 py-2 bg-secondary border-none rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="ENTITY_TYPE">ENTITY_TYPE</option>
              <option value="RELATIONSHIP_TYPE">RELATIONSHIP_TYPE</option>
            </select>
            <input 
              placeholder="Description" 
              value={newNode.description}
              onChange={(e) => setNewNode({...newNode, description: e.target.value})}
              className="col-span-2 px-3 py-2 bg-secondary border-none rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
          <button 
            onClick={handleCreate}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Save Node
          </button>
        </div>
      )}

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
