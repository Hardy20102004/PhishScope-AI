import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { listWorkflows, executeWorkflow, type Workflow } from "@/api/automation";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Play, Plus, Search, GitBranch } from "lucide-react";

export function WorkflowDashboard() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState<string | null>(null);

  const loadWorkflows = async () => {
    try {
      const data = await listWorkflows();
      setWorkflows(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    loadWorkflows();
  }, []);

  const handleExecute = async (id: string) => {
    setExecuting(id);
    try {
      await executeWorkflow(id, { source: "manual_ui" });
      alert("Workflow executed successfully. Check logs for details.");
    } catch (err) {
      console.error(err);
    } finally {
      setExecuting(null);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto p-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Automation Playbooks</h2>
          <p className="text-muted-foreground">Manage and orchestrate automated investigation workflows.</p>
        </div>
        <Link to="/automation/builder/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create Workflow
          </Button>
        </Link>
      </div>

      <div className="bg-card border rounded-xl shadow-sm">
        <div className="p-4 border-b flex items-center gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Search workflows..." 
              className="w-full pl-9 pr-4 py-2 bg-background border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>
        <div className="divide-y">
          {loading ? (
            <div className="p-8 text-center text-muted-foreground">Loading workflows...</div>
          ) : workflows.length === 0 ? (
            <div className="p-12 text-center border-dashed">
              <GitBranch className="mx-auto h-12 w-12 text-muted-foreground opacity-20 mb-4" />
              <h3 className="text-lg font-medium">No Playbooks Found</h3>
              <p className="text-sm text-muted-foreground mt-2">Create your first automated workflow to get started.</p>
            </div>
          ) : (
            workflows.map((wf) => (
              <div key={wf.id} className="p-4 flex items-center justify-between hover:bg-muted/50 transition-colors">
                <div className="flex items-start gap-4">
                  <div className="p-2 bg-primary/10 rounded-lg">
                    <GitBranch className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="font-medium">{wf.name}</h4>
                    <p className="text-sm text-muted-foreground">{wf.description || "No description provided."}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Badge variant={wf.is_active ? "default" : "secondary"}>{wf.is_active ? "Active" : "Draft"}</Badge>
                      <Badge variant="outline">Trigger: {wf.trigger_type}</Badge>
                      <span className="text-xs text-muted-foreground">v{wf.versions?.[0]?.version_number || 1}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={() => handleExecute(wf.id)}
                    disabled={executing === wf.id}
                  >
                    <Play className="mr-2 h-4 w-4" />
                    {executing === wf.id ? "Running..." : "Run"}
                  </Button>
                  <Link to={`/automation/builder/${wf.id}`}>
                    <Button variant="secondary" size="sm">Edit</Button>
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
