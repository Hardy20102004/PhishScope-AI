import { CheckCircle2, ShieldAlert, FileSearch, Zap } from "lucide-react"

export function EvidenceTimeline() {
  const events = [
    { id: 1, title: "Investigation Started", description: "Analyst initiated URL scan.", time: "10:00 AM", icon: <Zap className="h-4 w-4 text-blue-500" /> },
    { id: 2, title: "DNS Resolution Complete", description: "Resolved to 192.168.1.105 (Cloudflare)", time: "10:01 AM", icon: <FileSearch className="h-4 w-4 text-indigo-500" /> },
    { id: 3, title: "Malicious Payload Detected", description: "Found embedded obfuscated JavaScript.", time: "10:03 AM", icon: <ShieldAlert className="h-4 w-4 text-destructive" /> },
    { id: 4, title: "AI Analysis Complete", description: "Confidence score: 98% Phishing.", time: "10:05 AM", icon: <CheckCircle2 className="h-4 w-4 text-success" /> },
  ]

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-medium">Activity Timeline</h3>
      <div className="relative border-l border-muted ml-3 space-y-6 pb-4">
        {events.map((event) => (
          <div key={event.id} className="relative pl-6">
            <div className="absolute -left-[9px] top-1 flex h-4 w-4 items-center justify-center rounded-full border bg-background">
              {event.icon}
            </div>
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-1">
              <div>
                <h4 className="text-sm font-medium">{event.title}</h4>
                <p className="text-sm text-muted-foreground">{event.description}</p>
              </div>
              <span className="text-xs text-muted-foreground whitespace-nowrap">{event.time}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
