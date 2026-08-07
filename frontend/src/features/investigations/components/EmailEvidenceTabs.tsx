import { useState } from "react"
import { Mail, ShieldAlert, FileText, Link, Paperclip } from "lucide-react"
import { Badge } from "@/components/ui/Badge"

interface EmailEvidenceTabsProps {
  evidence: Record<string, any>
}

export function EmailEvidenceTabs({ evidence }: EmailEvidenceTabsProps) {
  const [activeTab, setActiveTab] = useState("headers")

  const tabs = [
    { id: "headers", label: "Headers", icon: Mail },
    { id: "auth", label: "Authentication", icon: ShieldAlert },
    { id: "content", label: "Content", icon: FileText },
    { id: "links", label: "Links", icon: Link },
    { id: "attachments", label: "Attachments", icon: Paperclip },
  ]

  const parsed = evidence.parsed || {}
  const auth = evidence.auth || {}

  const renderHeaders = () => {
    return (
      <div className="space-y-4">
         <div className="grid grid-cols-2 gap-4 text-sm">
           <div className="border p-3 rounded bg-muted/30">
             <span className="text-muted-foreground block text-xs uppercase mb-1">From</span>
             <span className="font-medium">{parsed.from || "Unknown"}</span>
           </div>
           <div className="border p-3 rounded bg-muted/30">
             <span className="text-muted-foreground block text-xs uppercase mb-1">To</span>
             <span className="font-medium">{parsed.to || "Unknown"}</span>
           </div>
           <div className="border p-3 rounded bg-muted/30">
             <span className="text-muted-foreground block text-xs uppercase mb-1">Date</span>
             <span className="font-medium">{parsed.date || "Unknown"}</span>
           </div>
           <div className="border p-3 rounded bg-muted/30">
             <span className="text-muted-foreground block text-xs uppercase mb-1">Subject</span>
             <span className="font-medium">{parsed.subject || "Unknown"}</span>
           </div>
         </div>
         
         <div className="mt-4">
           <h4 className="font-semibold text-sm mb-2">Raw Headers</h4>
           <pre className="bg-muted p-4 rounded-md text-xs font-mono overflow-auto max-h-[400px]">
             {JSON.stringify(parsed.headers, null, 2)}
           </pre>
         </div>
      </div>
    )
  }

  const renderAuth = () => {
    return (
      <div className="space-y-6">
         <div className="grid grid-cols-3 gap-4">
            <div className={`border p-4 rounded-md flex flex-col items-center justify-center gap-2 ${auth.spf === 'fail' ? 'bg-destructive/10 border-destructive text-destructive' : auth.spf === 'pass' ? 'bg-success/10 border-success text-success' : 'bg-muted text-muted-foreground'}`}>
               <span className="font-bold">SPF</span>
               <Badge variant={auth.spf === 'fail' ? 'destructive' : auth.spf === 'pass' ? 'success' : 'secondary'} className="uppercase">
                 {auth.spf}
               </Badge>
            </div>
            
            <div className={`border p-4 rounded-md flex flex-col items-center justify-center gap-2 ${auth.dkim === 'fail' ? 'bg-destructive/10 border-destructive text-destructive' : auth.dkim === 'pass' ? 'bg-success/10 border-success text-success' : 'bg-muted text-muted-foreground'}`}>
               <span className="font-bold">DKIM</span>
               <Badge variant={auth.dkim === 'fail' ? 'destructive' : auth.dkim === 'pass' ? 'success' : 'secondary'} className="uppercase">
                 {auth.dkim}
               </Badge>
            </div>
            
            <div className={`border p-4 rounded-md flex flex-col items-center justify-center gap-2 ${auth.dmarc === 'fail' ? 'bg-destructive/10 border-destructive text-destructive' : auth.dmarc === 'pass' ? 'bg-success/10 border-success text-success' : 'bg-muted text-muted-foreground'}`}>
               <span className="font-bold">DMARC</span>
               <Badge variant={auth.dmarc === 'fail' ? 'destructive' : auth.dmarc === 'pass' ? 'success' : 'secondary'} className="uppercase">
                 {auth.dmarc}
               </Badge>
            </div>
         </div>
         
         <div>
            <h4 className="font-semibold text-sm mb-2">Authentication-Results Header</h4>
            <pre className="bg-muted p-3 rounded text-xs font-mono whitespace-pre-wrap break-words">
              {auth.raw_header || "No Authentication-Results header found."}
            </pre>
         </div>
      </div>
    )
  }

  const renderContent = () => {
    return (
      <div className="space-y-4">
        {parsed.body_html ? (
          <div>
            <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">HTML Body Preview</h4>
            <div className="border rounded-md p-4 bg-white text-black max-h-[500px] overflow-auto">
               <div dangerouslySetInnerHTML={{ __html: parsed.body_html }} />
            </div>
          </div>
        ) : (
          <div>
            <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Plain Text Body</h4>
            <pre className="border rounded-md p-4 bg-muted text-sm max-h-[500px] overflow-auto whitespace-pre-wrap font-sans">
               {parsed.body_text || "No body content found."}
            </pre>
          </div>
        )}
      </div>
    )
  }

  const renderLinks = () => {
    const urls = parsed.urls_extracted || []
    return (
      <div className="space-y-4">
         <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Extracted Links ({urls.length})</h4>
         {urls.length > 0 ? (
           <ul className="space-y-2">
             {urls.map((url: string, idx: number) => (
               <li key={idx} className="bg-muted/50 p-2 rounded text-sm font-mono break-all flex items-start gap-2">
                 <Link className="h-4 w-4 shrink-0 text-muted-foreground mt-0.5" />
                 <a href={url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">{url}</a>
               </li>
             ))}
           </ul>
         ) : (
           <p className="text-sm text-muted-foreground">No links extracted from email body.</p>
         )}
      </div>
    )
  }
  
  const renderAttachments = () => {
    const attachments = parsed.attachments || []
    return (
      <div className="space-y-4">
         <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Attachments ({attachments.length})</h4>
         {attachments.length > 0 ? (
           <ul className="space-y-2">
             {attachments.map((att: any, idx: number) => (
               <li key={idx} className="border p-3 rounded-md text-sm flex justify-between items-center bg-card">
                 <div className="flex items-center gap-3">
                   <Paperclip className="h-4 w-4 text-muted-foreground" />
                   <span className="font-medium">{att.filename}</span>
                 </div>
                 <div className="text-xs text-muted-foreground flex gap-4">
                    <span>{att.content_type}</span>
                    <span>{(att.size_bytes / 1024).toFixed(1)} KB</span>
                 </div>
               </li>
             ))}
           </ul>
         ) : (
           <p className="text-sm text-muted-foreground">No attachments found.</p>
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
        {activeTab === "headers" && renderHeaders()}
        {activeTab === "auth" && renderAuth()}
        {activeTab === "content" && renderContent()}
        {activeTab === "links" && renderLinks()}
        {activeTab === "attachments" && renderAttachments()}
      </div>
    </div>
  )
}
