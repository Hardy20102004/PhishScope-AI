import { useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ReactFlow, Controls, Background, addEdge, applyNodeChanges, applyEdgeChanges, type Node, type Edge, type Connection } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Button } from "@/components/ui/Button";
import { Save, Play, ArrowLeft } from "lucide-react";
import { createWorkflow } from "@/api/automation";

const initialNodes: Node[] = [
  { id: "1", type: "input", position: { x: 250, y: 50 }, data: { label: "Trigger: Manual" } },
];
const initialEdges: Edge[] = [];

export function WorkflowBuilder() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [saving, setSaving] = useState(false);

  const onNodesChange = useCallback((changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)), []);
  const onEdgesChange = useCallback((changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)), []);
  const onConnect = useCallback((connection: Connection) => setEdges((eds) => addEdge(connection, eds)), []);

  const handleAddAction = (actionType: string, label: string) => {
    const newNode: Node = {
      id: Math.random().toString(),
      position: { x: 250, y: nodes.length * 100 + 50 },
      data: { label, action_type: actionType },
      type: "default",
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const definition = { nodes, edges };
      await createWorkflow({
        name: "New Playbook " + Math.floor(Math.random() * 1000),
        description: "Created via builder",
        trigger_type: "MANUAL",
        is_active: true,
        definition_json: definition
      });
      alert("Saved successfully!");
      navigate("/automation");
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      <div className="flex items-center justify-between p-4 border-b bg-card">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate("/automation")}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h2 className="text-lg font-medium">{id === "new" ? "Create Workflow" : "Edit Workflow"}</h2>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Play className="mr-2 h-4 w-4" /> Simulate
          </Button>
          <Button size="sm" onClick={handleSave} disabled={saving}>
            <Save className="mr-2 h-4 w-4" /> Save
          </Button>
        </div>
      </div>
      
      <div className="flex-1 flex">
        {/* Sidebar */}
        <div className="w-64 border-r bg-card p-4 space-y-4">
          <h3 className="font-medium text-sm text-muted-foreground uppercase tracking-wider">Actions Library</h3>
          <div className="space-y-2">
            <Button variant="outline" className="w-full justify-start text-left text-xs" onClick={() => handleAddAction("CREATE_CASE", "Create Case")}>+ Create Case</Button>
            <Button variant="outline" className="w-full justify-start text-left text-xs" onClick={() => handleAddAction("ENRICH_IP", "Enrich IP (Threat Intel)")}>+ Enrich IP</Button>
            <Button variant="outline" className="w-full justify-start text-left text-xs" onClick={() => handleAddAction("GENERATE_REPORT", "Generate Report")}>+ Generate Report</Button>
          </div>
        </div>
        
        {/* Canvas */}
        <div className="flex-1 bg-muted/30">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </div>
      </div>
    </div>
  );
}
