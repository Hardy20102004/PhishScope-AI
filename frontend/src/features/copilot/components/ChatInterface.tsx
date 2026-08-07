import { useState, useRef, useEffect } from "react";
import { sendCopilotMessage, type CopilotMessage } from "@/api/copilot";
import { Send, Bot, User, Loader2 } from "lucide-react";

interface ChatInterfaceProps {
  investigationId: string;
  initialHistory: CopilotMessage[];
}

export function ChatInterface({ investigationId, initialHistory }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<CopilotMessage[]>(initialHistory);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput("");
    
    // Optimistic UI update for user message
    const tempUserMsg: CopilotMessage = {
      id: Date.now().toString(),
      role: "USER",
      content: userMsg,
      evidence_references: [],
      created_at: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, tempUserMsg]);
    setLoading(true);

    try {
      const responseMsg = await sendCopilotMessage(investigationId, userMsg);
      setMessages(prev => [...prev.filter(m => m.id !== tempUserMsg.id), tempUserMsg, responseMsg]);
    } catch (err) {
      console.error("Failed to send message", err);
      // Revert optimistic update on failure
      setMessages(prev => prev.filter(m => m.id !== tempUserMsg.id));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground pt-10">
            <Bot className="h-10 w-10 mx-auto mb-2 opacity-50" />
            <p>I am your Investigation Copilot.</p>
            <p className="text-sm">Ask me to summarize findings or suggest next steps.</p>
          </div>
        )}
        
        {messages.map((msg) => (
          <div key={msg.id} className={`flex gap-3 ${msg.role === 'USER' ? 'flex-row-reverse' : ''}`}>
            <div className={`flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow-sm ${msg.role === 'USER' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
              {msg.role === 'USER' ? <User size={16} /> : <Bot size={16} />}
            </div>
            <div className={`flex max-w-[85%] flex-col gap-2 rounded-lg px-4 py-3 text-sm ${msg.role === 'USER' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
              {/* Very simple text rendering. A real app would use a Markdown component here. */}
              <div className="whitespace-pre-wrap">{msg.content}</div>
              
              {msg.evidence_references?.length > 0 && (
                <div className="mt-2 border-t border-border/50 pt-2 text-xs opacity-80">
                  <span className="font-semibold">Citations: </span>
                  {msg.evidence_references.length} evidence artifacts
                </div>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex gap-3">
            <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow-sm bg-muted">
              <Bot size={16} />
            </div>
            <div className="flex items-center px-4 py-3 text-sm">
              <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>
      
      <div className="p-4 border-t bg-background">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask Copilot about this investigation..."
            className="w-full rounded-md border border-input bg-background px-3 py-2 pr-10 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={!input.trim() || loading}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-muted-foreground hover:text-foreground disabled:opacity-50"
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  );
}
