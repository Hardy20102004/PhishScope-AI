import { useState, useEffect } from 'react';
import { FileText, Plus, Search, Filter } from 'lucide-react';
import type {  GovernancePolicy  } from "../types";

export function PolicyDashboard() {
  const [policies, setPolicies] = useState<GovernancePolicy[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showDraft, setShowDraft] = useState(false);
  const [newPolicy, setNewPolicy] = useState({ name: '', framework: '', version: '1.0' });

  useEffect(() => {
    // Mock API
    setTimeout(() => {
      setPolicies([
        {
          id: '1', name: 'Information Security Policy', description: 'Master overarching ISMS policy',
          version: '3.1', framework: 'ISO 27001', status: 'ACTIVE', created_at: new Date().toISOString(), updated_at: new Date().toISOString()
        },
        {
          id: '2', name: 'Access Control Policy', description: 'Guidelines for IAM and Zero Trust',
          version: '2.0', framework: 'NIST CSF', status: 'IN_REVIEW', created_at: new Date().toISOString(), updated_at: new Date().toISOString()
        }
      ]);
      setLoading(false);
    }, 500);
  }, []);

  const handleDraft = () => {
    if (!newPolicy.name || !newPolicy.framework) return;
    setPolicies([
      {
        id: Math.random().toString(),
        name: newPolicy.name,
        description: 'Newly drafted policy',
        version: newPolicy.version,
        framework: newPolicy.framework,
        status: 'DRAFT',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      ...policies
    ]);
    setShowDraft(false);
    setNewPolicy({ name: '', framework: '', version: '1.0' });
  };

  const filteredPolicies = policies.filter(p => 
    p.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    p.framework.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold flex items-center">
            <FileText className="mr-2 h-5 w-5 text-primary" />
            Policy Governance
          </h2>
          <p className="text-sm text-muted-foreground">Manage organizational security policies and standards.</p>
        </div>
        <button 
          onClick={() => setShowDraft(!showDraft)}
          className="flex items-center px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
        >
          <Plus className="mr-2 h-4 w-4" />
          {showDraft ? 'Cancel' : 'Draft Policy'}
        </button>
      </div>

      {showDraft && (
        <div className="bg-card border rounded-lg p-5 space-y-4">
          <h3 className="font-medium text-foreground">Draft New Policy</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <input 
              placeholder="Policy Name" 
              value={newPolicy.name}
              onChange={(e) => setNewPolicy({...newPolicy, name: e.target.value})}
              className="px-3 py-2 bg-secondary border-none rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <input 
              placeholder="Framework (e.g. SOC2, NIST)" 
              value={newPolicy.framework}
              onChange={(e) => setNewPolicy({...newPolicy, framework: e.target.value})}
              className="px-3 py-2 bg-secondary border-none rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <input 
              placeholder="Version" 
              value={newPolicy.version}
              onChange={(e) => setNewPolicy({...newPolicy, version: e.target.value})}
              className="px-3 py-2 bg-secondary border-none rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
          <button 
            onClick={handleDraft}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Save Draft
          </button>
        </div>
      )}

      <div className="bg-card border rounded-lg overflow-hidden flex flex-col">
        <div className="p-4 border-b flex justify-between items-center bg-secondary/30">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Search policies..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-4 py-2 bg-background border rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary w-64" 
            />
          </div>
          <button className="p-2 border rounded-md hover:bg-secondary transition-colors">
            <Filter className="h-4 w-4" />
          </button>
        </div>
        {loading ? (
          <div className="h-40 flex items-center justify-center text-muted-foreground">Loading policies...</div>
        ) : (
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground uppercase bg-secondary/50">
              <tr>
                <th className="px-6 py-3 font-medium">Policy Name</th>
                <th className="px-6 py-3 font-medium">Framework</th>
                <th className="px-6 py-3 font-medium">Version</th>
                <th className="px-6 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filteredPolicies.map((p, idx) => (
                <tr key={idx} className="hover:bg-muted/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-foreground">{p.name}</td>
                  <td className="px-6 py-4 text-muted-foreground">{p.framework}</td>
                  <td className="px-6 py-4 text-muted-foreground">v{p.version}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      p.status === 'ACTIVE' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-amber-500/10 text-amber-500'
                    }`}>
                      {p.status.replace('_', ' ')}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
