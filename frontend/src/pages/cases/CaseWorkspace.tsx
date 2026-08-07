import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getCase, type Case } from "@/api/cases";
import { Badge } from "@/components/ui/Badge";
import { ArrowLeft, Loader2 } from "lucide-react";
import { ReportBuilder } from "@/features/reporting/components/ReportBuilder";
import { ExportCenter } from "@/features/reporting/components/ExportCenter";
// We will create some dummy sub-components for the tabs for now to satisfy the build

function CaseTasks({ caseData }: { caseData: Case }) {
  return (
    <div className="p-6">
      <h3 className="text-lg font-medium mb-4">Task Board</h3>
      {caseData.tasks && caseData.tasks.length > 0 ? (
        <ul className="space-y-2">
          {caseData.tasks.map(t => (
            <li key={t.id} className="p-3 border rounded shadow-sm bg-card flex justify-between">
              <span>{t.title}</span>
              <Badge>{t.status}</Badge>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-muted-foreground text-sm">No tasks assigned to this case.</p>
      )}
    </div>
  )
}

function CaseTimeline() {
  return (
    <div className="p-6">
      <h3 className="text-lg font-medium mb-4">Audit Timeline</h3>
      <p className="text-muted-foreground text-sm">Timeline events will appear here.</p>
    </div>
  )
}

export function CaseWorkspace() {
  const { id } = useParams<{ id: string }>();
  const [caseData, setCaseData] = useState<Case | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    if (id) {
      getCase(id).then(setCaseData).catch(console.error).finally(() => setLoading(false));
    }
  }, [id]);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!caseData) {
    return <div className="p-8 text-center text-destructive">Failed to load Case.</div>;
  }

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto flex flex-col h-full">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
            <Link to="/cases" className="hover:text-foreground flex items-center transition-colors">
              <ArrowLeft className="mr-1 h-3 w-3" /> Cases
            </Link>
          </div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-primary">{caseData.title}</h1>
            <Badge variant={caseData.status === 'CLOSED' ? 'secondary' : 'default'}>{caseData.status}</Badge>
            <Badge variant="outline">{caseData.priority} Priority</Badge>
          </div>
          <p className="text-sm text-muted-foreground mt-1">{caseData.description || "No description provided."}</p>
        </div>
      </div>

      <div className="flex gap-2 border-b">
        <button onClick={() => setActiveTab("overview")} className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${activeTab === 'overview' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'}`}>
          Overview
        </button>
        <button onClick={() => setActiveTab("tasks")} className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${activeTab === 'tasks' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'}`}>
          Tasks
        </button>
        <button onClick={() => setActiveTab("timeline")} className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${activeTab === 'timeline' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'}`}>
          Timeline
        </button>
        <button onClick={() => setActiveTab("reports")} className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${activeTab === 'reports' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'}`}>
          Reports
        </button>
        <button onClick={() => setActiveTab("export")} className={`px-4 py-2 border-b-2 font-medium text-sm transition-colors ${activeTab === 'export' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'}`}>
          Export & Custody
        </button>
      </div>

      <div className="flex-1 bg-card border rounded-xl overflow-hidden shadow-sm">
        {activeTab === "overview" && (
          <div className="p-6">
            <h3 className="text-lg font-medium mb-4">Case Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Created At</p>
                <p className="font-medium">{new Date(caseData.created_at).toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Owner ID</p>
                <p className="font-mono text-sm">{caseData.owner_id || "Unassigned"}</p>
              </div>
            </div>
          </div>
        )}
        {activeTab === "tasks" && <CaseTasks caseData={caseData} />}
        {activeTab === "timeline" && <CaseTimeline />}
        {activeTab === "reports" && <div className="p-6"><ReportBuilder caseId={id!} /></div>}
        {activeTab === "export" && <div className="p-6"><ExportCenter caseId={id!} /></div>}
      </div>
    </div>
  );
}
