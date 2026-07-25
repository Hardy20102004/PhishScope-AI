import { useNavigate } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { Badge } from "@/components/ui/Badge"
import { formatDistanceToNow } from "date-fns"
import { useGetInvestigations } from "@/features/investigations/api/investigations"

export function RecentInvestigations() {
  const navigate = useNavigate()
  const { data: investigations, isLoading } = useGetInvestigations()

  const getRiskBadge = (risk: string | null) => {
    switch (risk) {
      case "CRITICAL": return <Badge variant="destructive">Critical</Badge>
      case "HIGH": return <Badge variant="destructive">High</Badge>
      case "MEDIUM": return <Badge variant="warning">Medium</Badge>
      case "LOW": return <Badge variant="success">Low</Badge>
      default: return <Badge variant="secondary">{risk || "Unknown"}</Badge>
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
        case "COMPLETED": return <Badge variant="outline">Completed</Badge>
        case "FAILED": return <Badge variant="destructive">Failed</Badge>
        default: return <Badge variant="warning">Analyzing</Badge>
    }
  }

  return (
    <Card className="col-span-full">
      <CardHeader>
        <CardTitle>Recent Investigations</CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
            <div className="text-sm text-muted-foreground py-4">Loading history...</div>
        ) : !investigations || investigations.length === 0 ? (
            <div className="text-sm text-muted-foreground py-4">No investigations found. Launch a new investigation to get started.</div>
        ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground uppercase bg-muted/50">
              <tr>
                <th className="px-4 py-3 font-medium rounded-tl-lg">ID</th>
                <th className="px-4 py-3 font-medium">Target</th>
                <th className="px-4 py-3 font-medium">Type</th>
                <th className="px-4 py-3 font-medium">Risk Score</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium rounded-tr-lg">Time</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {investigations.slice(0, 5).map((inv) => (
                <tr key={inv.id} className="hover:bg-muted/30 transition-colors">
                  <td 
                    className="px-4 py-3 font-mono font-medium text-primary cursor-pointer hover:underline"
                    onClick={() => navigate(`/investigations/${inv.id}`)}
                  >
                    {inv.id.substring(0, 8).toUpperCase()}
                  </td>
                  <td className="px-4 py-3 font-medium truncate max-w-[200px]">{inv.target}</td>
                  <td className="px-4 py-3 text-muted-foreground">{inv.type}</td>
                  <td className="px-4 py-3">{getRiskBadge(inv.risk_level)}</td>
                  <td className="px-4 py-3">{getStatusBadge(inv.status)}</td>
                  <td className="px-4 py-3 text-muted-foreground whitespace-nowrap">
                    {formatDistanceToNow(new Date(inv.created_at), { addSuffix: true })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        )}
      </CardContent>
    </Card>
  )
}
