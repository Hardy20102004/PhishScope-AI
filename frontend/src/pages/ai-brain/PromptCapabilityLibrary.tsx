import { useState } from "react"
import { Sparkles, Terminal } from "lucide-react"

export default function PromptCapabilityLibrary() {
  const [capabilities] = useState([
    { name: "Threat Analysis", defaultModel: "claude-3-5-sonnet", fallback: "gpt-4o / gemini-3.1-pro", temp: 0.2, desc: "Deep cryptographic and behavioural threat profiling of indicators." },
    { name: "Summarization", defaultModel: "gemini-3.1-pro", fallback: "mistral-large / claude-3.5-sonnet", temp: 0.1, desc: "Concise condensation of multi-channel logs and emails." },
    { name: "Evidence Explanation", defaultModel: "gemini-3.1-pro", fallback: "ollama-local / llama-3.3-70b", temp: 0.1, desc: "Forensic breakdown of obscure DNS records, headers, and hex dumps." },
    { name: "Threat Hunting", defaultModel: "deepseek-reasoning", fallback: "claude-3-5-sonnet / ollama-local", temp: 0.2, desc: "Proactive hypothesis generation and automated Sigma rule creation." },
    { name: "Recommendation Generation", defaultModel: "gpt-4o", fallback: "claude-3-5-sonnet / enterprise-self-hosted", temp: 0.3, desc: "Prioritized immediate containment and eradication SOC checklists." }
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Capability & Prompt Registry</h1>
        <p className="text-muted-foreground mt-1">Map cybersecurity intelligence tasks to specific models and system directives.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {capabilities.map((c, idx) => (
          <div key={idx} className="flex flex-col justify-between rounded-xl border bg-card p-6 shadow-sm transition-all hover:border-primary/50 hover:shadow-md">
            <div>
              <div className="flex items-center gap-2 font-semibold text-lg text-primary">
                <Sparkles className="h-5 w-5 text-indigo-500" />
                {c.name}
              </div>
              <p className="text-sm text-muted-foreground mt-2">{c.desc}</p>

              <div className="mt-6 border-t pt-4 text-xs space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground font-medium">Default Routing:</span>
                  <span className="font-semibold text-foreground">{c.defaultModel}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground font-medium">Fallback Cascade:</span>
                  <span className="font-medium text-muted-foreground">{c.fallback}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground font-medium">Inference Temp:</span>
                  <span className="font-semibold text-emerald-500">{c.temp}</span>
                </div>
              </div>
            </div>

            <button className="mt-6 flex items-center justify-center gap-2 w-full rounded-lg bg-secondary py-2 text-xs font-semibold text-secondary-foreground hover:bg-muted transition-all">
              <Terminal className="h-3.5 w-3.5" />
              Edit System Directive & Variables
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
