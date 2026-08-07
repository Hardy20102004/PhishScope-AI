import { useState } from "react"
import { Globe, Server, Lock, FileText, AlertTriangle } from "lucide-react"
import { Badge } from "@/components/ui/Badge"

interface EvidenceTabsProps {
  evidence: Record<string, any>
}

export function EvidenceTabs({ evidence }: EvidenceTabsProps) {
  const [activeTab, setActiveTab] = useState("http")

  const tabs = [
    { id: "http", label: "HTTP Flow", icon: Globe },
    { id: "dns", label: "DNS Records", icon: Server },
    { id: "tls", label: "TLS / SSL", icon: Lock },
    { id: "content", label: "Page Content", icon: FileText },
  ]

  const renderHTTP = () => {
    const http = evidence.http || {}
    if (http.error) return <div className="text-destructive p-4 border rounded">{http.error}</div>
    
    return (
      <div className="space-y-4">
        <div>
          <h4 className="font-semibold text-sm mb-2">Final Destination</h4>
          <code className="text-sm bg-muted px-2 py-1 rounded">{http.final_url}</code>
          <Badge className="ml-2" variant={http.status_code === 200 ? 'success' : 'secondary'}>{http.status_code}</Badge>
        </div>
        
        <div>
          <h4 className="font-semibold text-sm mb-2">Redirect Chain</h4>
          {http.redirect_chain?.length > 1 ? (
             <ul className="space-y-2 text-sm text-muted-foreground border-l-2 border-primary pl-4">
               {http.redirect_chain.map((r: any, idx: number) => (
                 <li key={idx}><span className="font-mono text-primary">{r.status_code}</span> - {r.url}</li>
               ))}
             </ul>
          ) : (
            <p className="text-sm text-muted-foreground">No redirects detected.</p>
          )}
        </div>

        <div>
          <h4 className="font-semibold text-sm mb-2">Response Headers</h4>
          <pre className="bg-muted p-4 rounded-md text-xs font-mono overflow-auto max-h-[300px]">
            {JSON.stringify(http.headers, null, 2)}
          </pre>
        </div>
      </div>
    )
  }

  const renderDNS = () => {
    const dns = evidence.dns || {}
    if (dns.error) return <div className="text-destructive p-4 border rounded">{dns.error}</div>
    
    return (
      <div className="space-y-4">
        {['A', 'AAAA', 'MX', 'TXT', 'NS'].map(rtype => {
          if (!dns[rtype] || dns[rtype].length === 0) return null
          
          return (
            <div key={rtype} className="border rounded-md overflow-hidden">
               <div className="bg-muted/50 px-4 py-2 border-b font-semibold text-sm">{rtype} Records</div>
               <ul className="p-4 space-y-1 text-sm font-mono text-muted-foreground break-all">
                  {dns[rtype].map((rec: string, idx: number) => (
                    <li key={idx}>{rec}</li>
                  ))}
               </ul>
            </div>
          )
        })}
        {Object.keys(dns).length === 0 && <p className="text-sm text-muted-foreground">No DNS evidence collected.</p>}
      </div>
    )
  }

  const renderTLS = () => {
    const tls = evidence.tls || {}
    if (tls.error) return (
      <div className="rounded-xl border border-destructive/50 bg-destructive/10 text-destructive shadow p-4 flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 shrink-0 mt-0.5" />
            <div className="text-sm">
              <h4 className="font-semibold">TLS Handshake Failed</h4>
              <p>{tls.details || tls.error}</p>
            </div>
      </div>
    )
    if (!tls.valid) return <p className="text-sm text-muted-foreground">No TLS data.</p>
    
    return (
      <div className="space-y-4 text-sm">
        <div className="grid grid-cols-2 gap-4">
          <div className="border p-4 rounded-md">
            <h4 className="font-semibold mb-2 text-muted-foreground text-xs uppercase">Issuer</h4>
            <p className="font-medium">{tls.issuer?.organizationName || "Unknown"}</p>
            <p className="text-muted-foreground text-xs mt-1">{tls.issuer?.commonName}</p>
          </div>
          <div className="border p-4 rounded-md">
            <h4 className="font-semibold mb-2 text-muted-foreground text-xs uppercase">Subject</h4>
            <p className="font-medium">{tls.subject?.commonName || "Unknown"}</p>
            <p className="text-muted-foreground text-xs mt-1">Valid until: {tls.notAfter}</p>
          </div>
        </div>
        
        <div>
           <h4 className="font-semibold text-sm mb-2">Subject Alternative Names (SANs)</h4>
           <div className="flex flex-wrap gap-2">
             {tls.subjectAltName?.map((san: string, idx: number) => (
               <Badge key={idx} variant="secondary" className="font-mono">{san}</Badge>
             ))}
           </div>
        </div>
        
        <div className="text-xs text-muted-foreground mt-4">
          Protocol: <span className="font-mono">{tls.version}</span> • Cipher: <span className="font-mono">{tls.cipher?.[0]}</span>
        </div>
      </div>
    )
  }

  const renderContent = () => {
    const content = evidence.content || {}
    if (content.error) return <div className="text-destructive p-4 border rounded">{content.error}</div>
    if (Object.keys(content).length === 0) return <p className="text-sm text-muted-foreground">No content evidence collected.</p>
    
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4 text-sm">
           <div className="border p-3 rounded bg-muted/30 flex justify-between">
             <span className="text-muted-foreground">HTML Title:</span>
             <span className="font-medium truncate max-w-[200px]" title={content.title}>{content.title || "None"}</span>
           </div>
           <div className="border p-3 rounded bg-muted/30 flex justify-between">
             <span className="text-muted-foreground">Forms Found:</span>
             <span className="font-medium">{content.forms_count}</span>
           </div>
           <div className="border p-3 rounded bg-muted/30 flex justify-between">
             <span className="text-muted-foreground">Hidden Inputs:</span>
             <span className="font-medium text-destructive">{content.hidden_elements}</span>
           </div>
           <div className="border p-3 rounded bg-muted/30 flex justify-between">
             <span className="text-muted-foreground">Scripts Loaded:</span>
             <span className="font-medium">{content.scripts_count}</span>
           </div>
        </div>
        
        {content.suspicious_keywords_found?.length > 0 && (
          <div className="mt-4 border border-warning/50 bg-warning/10 p-4 rounded-md">
            <h4 className="text-sm font-semibold text-warning mb-2">Suspicious Keywords Detected</h4>
            <div className="flex flex-wrap gap-2">
               {content.suspicious_keywords_found.map((kw: string, idx: number) => (
                 <Badge key={idx} variant="outline" className="border-warning text-warning">{kw}</Badge>
               ))}
            </div>
          </div>
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
        {activeTab === "http" && renderHTTP()}
        {activeTab === "dns" && renderDNS()}
        {activeTab === "tls" && renderTLS()}
        {activeTab === "content" && renderContent()}
      </div>
    </div>
  )
}
