import { useState } from "react"
import { QrCode, Link as LinkIcon } from "lucide-react"

interface QREvidenceTabsProps {
  evidence: Record<string, any>
}

export function QREvidenceTabs({ evidence }: QREvidenceTabsProps) {
  const [activeTab, setActiveTab] = useState("payload")

  const tabs = [
    { id: "payload", label: "Decoded Payload", icon: QrCode },
    { id: "analysis", label: "URL Threat Analysis", icon: LinkIcon },
  ]

  const qr = evidence.qr || {}
  const urlAnalysis = evidence.url_analysis || {}

  const renderPayload = () => {
    return (
      <div className="space-y-4">
         {qr.error ? (
           <div className="p-4 bg-destructive/10 text-destructive border border-destructive rounded-md text-sm">
             <strong>Error:</strong> {qr.error}
           </div>
         ) : (
           <>
             <div className="flex items-center gap-4 mb-4">
                <span className="text-xs uppercase text-muted-foreground font-bold tracking-wider">Format:</span>
                <span className="px-2 py-1 bg-muted rounded font-mono text-xs">{qr.format || "UNKNOWN"}</span>
             </div>
             
             <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Raw Payload</h4>
             <pre className="border rounded-md p-4 bg-muted text-lg max-h-[500px] overflow-auto whitespace-pre-wrap font-mono text-primary font-bold break-all">
                {qr.decoded_text || "No payload found."}
             </pre>
           </>
         )}
      </div>
    )
  }

  const renderAnalysis = () => {
    const urls = Object.keys(urlAnalysis)
    return (
      <div className="space-y-4">
         <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Nested URL Analysis</h4>
         {urls.length > 0 ? (
           <ul className="space-y-4">
             {urls.map((url: string, idx: number) => {
               const analysis = urlAnalysis[url]
               return (
                 <li key={idx} className="border p-4 rounded-md bg-card space-y-4">
                   <div className="flex items-start justify-between">
                     <a href={url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline font-mono text-sm break-all pr-4">{url}</a>
                     {analysis && (
                       <span className={`px-2 py-1 text-xs font-bold rounded uppercase whitespace-nowrap ${analysis.risk_level === 'CRITICAL' || analysis.risk_level === 'HIGH' ? 'bg-destructive/10 text-destructive' : 'bg-muted text-muted-foreground'}`}>
                         {analysis.risk_level}
                       </span>
                     )}
                   </div>
                   
                   {analysis.evidence && analysis.evidence.http && analysis.evidence.http.redirect_chain && (
                     <div className="text-sm mt-4 p-4 bg-muted/50 rounded border">
                       <h5 className="font-semibold mb-2">Redirect Chain</h5>
                       <ul className="space-y-1">
                         {analysis.evidence.http.redirect_chain.map((r: any, rIdx: number) => (
                           <li key={rIdx} className="text-muted-foreground break-all">
                             <span className="font-mono">{r.status_code}</span> &rarr; {r.url}
                           </li>
                         ))}
                       </ul>
                     </div>
                   )}
                 </li>
               )
             })}
           </ul>
         ) : (
           <p className="text-sm text-muted-foreground">The QR code did not contain a valid URL.</p>
         )}
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full border rounded-xl overflow-hidden bg-card text-card-foreground shadow">
      <div className="flex border-b overflow-x-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon
          const isActive = activeTab === tab.id
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
                isActive 
                  ? "border-primary text-primary bg-primary/5" 
                  : "border-transparent text-muted-foreground hover:text-foreground hover:bg-muted/50"
              }`}
            >
              <Icon className="h-4 w-4" />
              {tab.label}
            </button>
          )
        })}
      </div>
      
      <div className="p-6 overflow-auto">
        {activeTab === "payload" && renderPayload()}
        {activeTab === "analysis" && renderAnalysis()}
      </div>
    </div>
  )
}
