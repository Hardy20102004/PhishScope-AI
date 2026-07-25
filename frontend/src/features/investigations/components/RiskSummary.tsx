import { ShieldAlert, AlertTriangle } from "lucide-react"
import { Card, CardContent } from "@/components/ui/Card"

export function RiskSummary() {
  return (
    <Card className="border-destructive bg-destructive/5 overflow-hidden">
      <div className="bg-destructive px-4 py-2 text-destructive-foreground font-semibold flex items-center">
        <ShieldAlert className="mr-2 h-4 w-4" /> Critical Risk Detected
      </div>
      <CardContent className="p-4 pt-6 space-y-4">
        <div className="flex items-end gap-2">
          <span className="text-5xl font-black text-destructive">98</span>
          <span className="text-lg text-muted-foreground mb-1">/ 100</span>
        </div>
        
        <div className="space-y-2">
          <div className="flex items-start gap-2 text-sm">
            <AlertTriangle className="h-4 w-4 text-warning shrink-0 mt-0.5" />
            <span>Zero-day phishing kit detected on target domain.</span>
          </div>
          <div className="flex items-start gap-2 text-sm">
            <AlertTriangle className="h-4 w-4 text-warning shrink-0 mt-0.5" />
            <span>Domain registered 3 days ago.</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
