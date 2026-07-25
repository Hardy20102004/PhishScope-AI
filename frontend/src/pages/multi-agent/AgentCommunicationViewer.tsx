import { useState } from "react"
import { MessageSquare, Radio, ArrowRightLeft } from "lucide-react"

export default function AgentCommunicationViewer() {
  const [messages] = useState([
    { id: "MSG-01", type: "BROADCAST", sender: "investigator-agent", content: "New IOCs discovered: 10.0.0.5. Initiating parallel triage.", time: "10:14:02" },
    { id: "MSG-02", type: "EVENT", sender: "url-analysis-agent", content: "URL analysis complete. Fast-flux detected.", time: "10:14:04" },
    { id: "MSG-03", type: "REQUEST", sender: "threat-intel-agent", receiver: "knowledge-agent", content: "Query organizational memory for 10.0.0.5.", time: "10:14:05" },
    { id: "MSG-04", type: "HANDOFF", sender: "threat-intel-agent", receiver: "report-writer-agent", content: "Intel correlation finished. Over to you.", time: "10:14:08" }
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Agent Communication Bus</h1>
        <p className="text-muted-foreground mt-1">Real-time inter-agent messaging and handoff tracking.</p>
      </div>

      <div className="rounded-xl border bg-card shadow-sm">
        <div className="border-b p-6 flex justify-between items-center">
          <h2 className="text-lg font-semibold">Live Messaging Stream</h2>
          <span className="flex items-center gap-2 text-sm text-emerald-500 font-medium">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            SSE Connected
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr>
                <th className="p-4">Time</th>
                <th className="p-4">Message Type</th>
                <th className="p-4">Sender &rarr; Receiver</th>
                <th className="p-4">Payload Summary</th>
              </tr>
            </thead>
            <tbody className="divide-y font-mono text-xs">
              {messages.map((m) => (
                <tr key={m.id} className="hover:bg-muted/30">
                  <td className="p-4 text-muted-foreground">{m.time}</td>
                  <td className="p-4">
                    <span className={`inline-flex items-center gap-1.5 rounded bg-secondary px-2 py-1 font-semibold text-secondary-foreground`}>
                      {m.type === 'BROADCAST' && <Radio className="h-3 w-3" />}
                      {m.type === 'HANDOFF' && <ArrowRightLeft className="h-3 w-3" />}
                      {m.type === 'EVENT' && <MessageSquare className="h-3 w-3" />}
                      {m.type}
                    </span>
                  </td>
                  <td className="p-4">
                    <span className="font-semibold text-primary">{m.sender}</span>
                    {m.receiver && <span className="text-muted-foreground"> &rarr; <span className="font-semibold text-primary">{m.receiver}</span></span>}
                  </td>
                  <td className="p-4 text-muted-foreground">{m.content}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
