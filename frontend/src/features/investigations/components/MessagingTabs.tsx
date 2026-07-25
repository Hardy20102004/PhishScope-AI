import { useState } from "react"
import { MessageSquare, Link as LinkIcon, Phone } from "lucide-react"

interface MessagingTabsProps {
  evidence: Record<string, any>
}

export function MessagingTabs({ evidence }: MessagingTabsProps) {
  const [activeTab, setActiveTab] = useState("content")

  const tabs = [
    { id: "content", label: "Message Content", icon: MessageSquare },
    { id: "links", label: "Extracted Links", icon: LinkIcon },
    { id: "phones", label: "Phone Numbers", icon: Phone },
  ]

  const parsed = evidence.parsed || {}
  const urlAnalysis = evidence.url_analysis || {}

  const renderContent = () => {
    return (
      <div className="space-y-4">
         <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Raw Message</h4>
         <pre className="border rounded-md p-4 bg-muted text-sm max-h-[500px] overflow-auto whitespace-pre-wrap font-sans">
            {parsed.raw_text || "No message content found."}
         </pre>
      </div>
    )
  }

  const renderLinks = () => {
    const urls = parsed.urls || []
    return (
      <div className="space-y-4">
         <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Extracted Links ({urls.length})</h4>
         {urls.length > 0 ? (
           <ul className="space-y-4">
             {urls.map((url: string, idx: number) => {
               const analysis = urlAnalysis[url]
               return (
                 <li key={idx} className="border p-4 rounded-md bg-card">
                   <div className="flex items-start justify-between">
                     <a href={url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline font-mono text-sm break-all pr-4">{url}</a>
                     {analysis && (
                       <span className={`px-2 py-1 text-xs font-bold rounded uppercase whitespace-nowrap ${analysis.risk_level === 'CRITICAL' || analysis.risk_level === 'HIGH' ? 'bg-destructive/10 text-destructive' : 'bg-muted text-muted-foreground'}`}>
                         {analysis.risk_level}
                       </span>
                     )}
                   </div>
                 </li>
               )
             })}
           </ul>
         ) : (
           <p className="text-sm text-muted-foreground">No links extracted from message.</p>
         )}
      </div>
    )
  }
  
  const renderPhones = () => {
    const phones = parsed.phone_numbers || []
    return (
      <div className="space-y-4">
         <h4 className="font-semibold text-sm mb-2 text-muted-foreground uppercase">Phone Numbers ({phones.length})</h4>
         {phones.length > 0 ? (
           <ul className="space-y-2">
             {phones.map((phone: string, idx: number) => (
               <li key={idx} className="bg-muted/50 p-3 rounded text-sm font-mono flex items-center gap-3">
                 <Phone className="h-4 w-4 text-muted-foreground" />
                 {phone}
               </li>
             ))}
           </ul>
         ) : (
           <p className="text-sm text-muted-foreground">No phone numbers found.</p>
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
        {activeTab === "content" && renderContent()}
        {activeTab === "links" && renderLinks()}
        {activeTab === "phones" && renderPhones()}
      </div>
    </div>
  )
}
