import { useParams, Link } from "react-router-dom"
import { ArrowLeft, ExternalLink, Download, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Badge } from "@/components/ui/Badge"
import { useGetInvestigation } from "@/features/investigations/api/investigations"
import { EvidenceTabs } from "@/features/investigations/components/EvidenceTabs"
import { EmailEvidenceTabs } from "@/features/investigations/components/EmailEvidenceTabs"
import { MessagingTabs } from "@/features/investigations/components/MessagingTabs"
import { QREvidenceTabs } from "@/features/investigations/components/QREvidenceTabs"
import { formatDistanceToNow } from "date-fns"
import { Bot } from "lucide-react"
import { useState } from "react"
import { CopilotPanel } from "@/features/copilot/components/CopilotPanel"
import { parseUTCDate } from "@/lib/utils"

export function Workspace() {
  const { id } = useParams<{ id: string }>()
  const { data: investigation, isLoading, isError } = useGetInvestigation(id!)
  const [showCopilot, setShowCopilot] = useState(false)

  if (isLoading) return <div className="p-8 text-center text-muted-foreground">Loading Investigation Data...</div>
  if (isError || !investigation) return <div className="p-8 text-center text-destructive">Failed to load investigation or not found.</div>

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-[1600px] mx-auto">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
            <Link to="/dashboard" className="hover:text-foreground flex items-center transition-colors">
              <ArrowLeft className="mr-1 h-3 w-3" /> Dashboard
            </Link>
            <span>/</span>
            <span>Investigations</span>
          </div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-primary">INV-{investigation.id.substring(0, 8).toUpperCase()}</h1>
            <Badge variant={investigation.risk_level === 'CRITICAL' || investigation.risk_level === 'HIGH' ? 'destructive' : 'secondary'}>
              {investigation.risk_level || "UNKNOWN"} Risk
            </Badge>
            <Badge variant="outline">{investigation.type} Analysis</Badge>
            {investigation.status === "FAILED" && <Badge variant="destructive">FAILED</Badge>}
          </div>
          <a href={investigation.target} target="_blank" rel="noreferrer" className="text-primary hover:underline flex items-center text-sm font-mono mt-1">
            {investigation.target} <ExternalLink className="ml-1 h-3 w-3" />
          </a>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={() => setShowCopilot(!showCopilot)} className={showCopilot ? "bg-primary text-primary-foreground" : ""}>
            <Bot className="mr-2 h-4 w-4" /> Copilot
          </Button>
          <Button variant="outline"><Download className="mr-2 h-4 w-4" /> Export PDF</Button>
        </div>
      </div>

      {investigation.status === "FAILED" && (
        <div className="rounded-xl border border-destructive/50 bg-destructive/10 text-destructive shadow p-6 flex items-start gap-3">
            <AlertTriangle className="h-6 w-6 shrink-0 mt-0.5" />
            <div>
              <h3 className="text-lg font-bold">Investigation Failed</h3>
              <p className="mt-1">{investigation.error_message}</p>
            </div>
        </div>
      )}

      {/* Grid Layout */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-xl border bg-card text-card-foreground shadow p-6">
            <h3 className="text-lg font-medium mb-4">Findings & Heuristics</h3>
            {investigation.findings && investigation.findings.length > 0 ? (
                <div className="space-y-4">
                  {investigation.findings.map((finding, idx) => (
                    <div key={idx} className="border-l-4 border-primary pl-4 py-1">
                      <h4 className="font-semibold">{finding.title}</h4>
                      <p className="text-sm text-muted-foreground">{finding.description}</p>
                    </div>
                  ))}
                </div>
            ) : (
                <p className="text-sm text-muted-foreground">No suspicious indicators found.</p>
            )}
          </div>

          <div className="rounded-xl border bg-card text-card-foreground shadow h-[500px]">
             {investigation.type === "EMAIL" ? (
                 <EmailEvidenceTabs evidence={investigation.evidence} />
             ) : investigation.type === "MESSAGING" ? (
                 <MessagingTabs evidence={investigation.evidence} />
             ) : investigation.type === "QR" ? (
                 <QREvidenceTabs evidence={investigation.evidence} />
             ) : (
                 <EvidenceTabs evidence={investigation.evidence} />
             )}
          </div>
        </div>

        {/* Sidebar / Copilot */}
        {showCopilot ? (
          <div className="lg:col-span-1 h-[700px]">
            <CopilotPanel investigationId={investigation.id} />
          </div>
        ) : (
          <div className="lg:col-span-1 space-y-6">
            
            <div className="rounded-xl border bg-card text-card-foreground shadow p-6 text-center">
              <h3 className="text-lg font-medium text-muted-foreground mb-2">Risk Score</h3>
              <div className="text-6xl font-black text-primary">{investigation.risk_score || 0}</div>
            </div>
            
            <div className="rounded-xl border bg-card text-card-foreground shadow p-6">
              <h3 className="text-lg font-medium mb-4">Metadata</h3>
              <dl className="space-y-4 text-sm">
                <div>
                  <dt className="text-muted-foreground">Status</dt>
                  <dd className="mt-1 font-medium">{investigation.status}</dd>
                </div>
                <div>
                  <dt className="text-muted-foreground">Created</dt>
                  <dd className="mt-1">{formatDistanceToNow(parseUTCDate(investigation.created_at), { addSuffix: true })}</dd>
                </div>
              </dl>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
