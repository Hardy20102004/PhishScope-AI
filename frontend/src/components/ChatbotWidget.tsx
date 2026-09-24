import { useState, useRef, useEffect, useCallback } from "react";
import { sendChatMessage, type ChatMessage } from "@/api/chatbot";
import {
  MessageCircle,
  X,
  Send,
  Loader2,
  Bot,
  User,
  Sparkles,
  ChevronDown,
  Trash2,
  RefreshCw,
} from "lucide-react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface DisplayMessage extends ChatMessage {
  id: string;
  timestamp: Date;
  error?: boolean;
}

// ─── Markdown-lite renderer ───────────────────────────────────────────────────

function renderMarkdown(text: string): string {
  return text
    // Bold
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    // Italic
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    // Inline code
    .replace(/`([^`]+)`/g, '<code style="background:rgba(99,102,241,0.15);padding:1px 5px;border-radius:4px;font-size:0.85em">$1</code>')
    // Headers (h3)
    .replace(/^### (.+)$/gm, '<p style="font-weight:700;color:#a5b4fc;margin:10px 0 4px;font-size:0.85em;text-transform:uppercase;letter-spacing:0.05em">$1</p>')
    // Headers (h2)
    .replace(/^## (.+)$/gm, '<p style="font-weight:700;color:#c4b5fd;margin:12px 0 4px;font-size:0.9em">$1</p>')
    // Bullet points
    .replace(/^[-•] (.+)$/gm, '<div style="display:flex;gap:6px;margin:3px 0"><span style="color:#6366f1;margin-top:1px;flex-shrink:0">•</span><span>$1</span></div>')
    // Numbered list
    .replace(/^\d+\. (.+)$/gm, '<div style="display:flex;gap:6px;margin:3px 0"><span style="color:#6366f1;flex-shrink:0">›</span><span>$1</span></div>')
    // Line breaks
    .replace(/\n\n/g, '<div style="height:8px"></div>')
    .replace(/\n/g, "<br/>");
}

// ─── Quick Prompts ────────────────────────────────────────────────────────────

const QUICK_PROMPTS = [
  "How do I create a new case?",
  "What is URL Intelligence?",
  "How to analyze a QR code threat?",
  "What features does this platform have?",
  "How to change case priority?",
  "What is the AI Security Brain?",
];

// ─── Message Bubble ───────────────────────────────────────────────────────────

function MessageBubble({ msg }: { msg: DisplayMessage }) {
  const isUser = msg.role === "user";

  return (
    <div
      className={`flex gap-2.5 ${isUser ? "flex-row-reverse" : "flex-row"}`}
      style={{ animation: "msgIn 0.2s cubic-bezier(.22,1,.36,1)" }}
    >
      {/* Avatar */}
      <div
        className="flex-shrink-0 flex h-7 w-7 items-center justify-center rounded-full"
        style={{
          background: isUser
            ? "linear-gradient(135deg,#6366f1,#8b5cf6)"
            : "linear-gradient(135deg,#0ea5e9,#6366f1)",
          boxShadow: isUser
            ? "0 0 10px rgba(99,102,241,0.4)"
            : "0 0 10px rgba(14,165,233,0.4)",
        }}
      >
        {isUser ? (
          <User size={13} className="text-white" />
        ) : (
          <Bot size={13} className="text-white" />
        )}
      </div>

      {/* Bubble */}
      <div
        className="max-w-[82%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed"
        style={{
          background: isUser
            ? "linear-gradient(135deg,rgba(99,102,241,0.25),rgba(139,92,246,0.2))"
            : "rgba(255,255,255,0.06)",
          border: isUser
            ? "1px solid rgba(99,102,241,0.3)"
            : "1px solid rgba(255,255,255,0.08)",
          color: msg.error ? "#f87171" : "#e2e8f0",
          borderTopRightRadius: isUser ? "4px" : "16px",
          borderTopLeftRadius: isUser ? "16px" : "4px",
        }}
      >
        {isUser ? (
          <p style={{ margin: 0 }}>{msg.content}</p>
        ) : (
          <div
            dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }}
          />
        )}
        <p
          className="mt-1.5"
          style={{
            color: "rgba(148,163,184,0.6)",
            fontSize: "10px",
            textAlign: isUser ? "right" : "left",
            margin: "6px 0 0",
          }}
        >
          {msg.timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>
    </div>
  );
}

// ─── Typing Indicator ─────────────────────────────────────────────────────────

function TypingIndicator() {
  return (
    <div className="flex gap-2.5 items-end" style={{ animation: "msgIn 0.2s ease" }}>
      <div
        className="flex-shrink-0 flex h-7 w-7 items-center justify-center rounded-full"
        style={{ background: "linear-gradient(135deg,#0ea5e9,#6366f1)" }}
      >
        <Bot size={13} className="text-white" />
      </div>
      <div
        className="flex items-center gap-1 rounded-2xl px-4 py-3"
        style={{
          background: "rgba(255,255,255,0.06)",
          border: "1px solid rgba(255,255,255,0.08)",
          borderTopLeftRadius: "4px",
        }}
      >
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="block h-1.5 w-1.5 rounded-full"
            style={{
              background: "#6366f1",
              animation: `typingDot 1.2s ease ${i * 0.2}s infinite`,
            }}
          />
        ))}
      </div>
    </div>
  );
}

// ─── Main Chatbot Widget ──────────────────────────────────────────────────────

export function ChatbotWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<DisplayMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "👋 **Hello! I'm PhishScope Assistant.**\n\nI can help you with:\n- Understanding platform features\n- Managing cases & investigations\n- Cybersecurity guidance\n- Any question about this platform\n\nHow can I assist you today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const [showScrollBtn, setShowScrollBtn] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  const scrollToBottom = useCallback((force = false) => {
    if (!scrollAreaRef.current) return;
    const el = scrollAreaRef.current;
    const isNearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 80;
    if (force || isNearBottom) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading, scrollToBottom]);

  const handleScroll = () => {
    const el = scrollAreaRef.current;
    if (!el) return;
    setShowScrollBtn(el.scrollHeight - el.scrollTop - el.clientHeight > 120);
  };

  // Focus input when opened
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 150);
      setHasUnread(false);
    }
  }, [open]);

  // ── Send message ───────────────────────────────────────────────────────────

  const sendMessage = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    const userMsg: DisplayMessage = {
      id: Date.now().toString(),
      role: "user",
      content: trimmed,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    // Build history for API (exclude welcome message)
    const history = messages
      .filter((m) => m.id !== "welcome")
      .map((m) => ({ role: m.role, content: m.content }));

    try {
      const res = await sendChatMessage(trimmed, history);
      const assistantMsg: DisplayMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: res.reply,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      if (!open) setHasUnread(true);
    } catch {
      const errMsg: DisplayMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "⚠️ Unable to reach the AI service. Please check your connection and try again.",
        timestamp: new Date(),
        error: true,
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: "welcome-" + Date.now(),
        role: "assistant",
        content:
          "Chat cleared. How can I help you? 😊",
        timestamp: new Date(),
      },
    ]);
  };

  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <>
      <style>{`
        @keyframes msgIn {
          from { opacity: 0; transform: translateY(6px) scale(0.98); }
          to   { opacity: 1; transform: translateY(0)   scale(1); }
        }
        @keyframes typingDot {
          0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
          30%            { opacity: 1;   transform: translateY(-4px); }
        }
        @keyframes widgetIn {
          from { opacity: 0; transform: scale(0.9) translateY(16px); }
          to   { opacity: 1; transform: scale(1)   translateY(0); }
        }
        @keyframes pulse-ring {
          0%   { transform: scale(1);    opacity: 0.6; }
          70%  { transform: scale(1.35); opacity: 0; }
          100% { transform: scale(1.35); opacity: 0; }
        }
        .chatbot-input::-webkit-scrollbar { display: none; }
        .chat-scroll::-webkit-scrollbar { width: 4px; }
        .chat-scroll::-webkit-scrollbar-track { background: transparent; }
        .chat-scroll::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 4px; }
      `}</style>

      {/* ── Floating Button ── */}
      <div className="fixed bottom-6 right-6 z-[200]" id="chatbot-toggle">
        {/* Pulse ring */}
        {!open && (
          <span
            className="absolute inset-0 rounded-full"
            style={{
              background: "rgba(99,102,241,0.4)",
              animation: "pulse-ring 2s ease-out infinite",
            }}
          />
        )}
        <button
          onClick={() => { setOpen((o) => !o); setHasUnread(false); }}
          className="relative flex h-14 w-14 items-center justify-center rounded-full shadow-2xl transition-all hover:scale-105 active:scale-95"
          style={{
            background: open
              ? "linear-gradient(135deg,#ef4444,#dc2626)"
              : "linear-gradient(135deg,#6366f1,#8b5cf6)",
            boxShadow: "0 0 30px rgba(99,102,241,0.5)",
          }}
          title={open ? "Close chat" : "Ask PhishScope Assistant"}
        >
          {open ? (
            <X size={22} className="text-white" />
          ) : (
            <MessageCircle size={22} className="text-white" />
          )}

          {/* Unread badge */}
          {hasUnread && !open && (
            <span
              className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full text-white"
              style={{
                background: "#ef4444",
                fontSize: "9px",
                fontWeight: 700,
              }}
            >
              1
            </span>
          )}
        </button>
      </div>

      {/* ── Chat Window ── */}
      {open && (
        <div
          id="chatbot-window"
          className="fixed bottom-24 right-6 z-[199] flex flex-col rounded-2xl shadow-2xl overflow-hidden"
          style={{
            width: "min(380px, calc(100vw - 24px))",
            height: "min(560px, calc(100vh - 120px))",
            background: "linear-gradient(180deg, #131728 0%, #0d1117 100%)",
            border: "1px solid rgba(99,102,241,0.2)",
            animation: "widgetIn 0.22s cubic-bezier(.22,1,.36,1)",
            boxShadow:
              "0 32px 64px rgba(0,0,0,0.6), 0 0 0 1px rgba(99,102,241,0.1)",
          }}
        >
          {/* Header */}
          <div
            className="flex items-center justify-between px-4 py-3 flex-shrink-0"
            style={{
              background:
                "linear-gradient(135deg,rgba(99,102,241,0.15),rgba(139,92,246,0.1))",
              borderBottom: "1px solid rgba(99,102,241,0.15)",
            }}
          >
            <div className="flex items-center gap-2.5">
              <div
                className="flex h-9 w-9 items-center justify-center rounded-xl"
                style={{ background: "linear-gradient(135deg,#6366f1,#8b5cf6)" }}
              >
                <Sparkles size={16} className="text-white" />
              </div>
              <div>
                <p className="text-sm font-bold text-white leading-none">
                  PhishScope Assistant
                </p>
                <div className="flex items-center gap-1.5 mt-0.5">
                  <span
                    className="h-1.5 w-1.5 rounded-full"
                    style={{ background: "#10b981", boxShadow: "0 0 4px #10b981" }}
                  />
                  <span className="text-[10px] text-slate-400">
                    Gemini AI · Online
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                id="chatbot-clear"
                onClick={clearChat}
                title="Clear chat"
                className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-500 hover:text-slate-300 hover:bg-white/10 transition-colors"
              >
                <Trash2 size={13} />
              </button>
              <button
                id="chatbot-close"
                onClick={() => setOpen(false)}
                title="Close"
                className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-500 hover:text-slate-300 hover:bg-white/10 transition-colors"
              >
                <X size={14} />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div
            ref={scrollAreaRef}
            onScroll={handleScroll}
            className="flex-1 overflow-y-auto px-4 py-4 space-y-3 chat-scroll"
          >
            {messages.map((msg) => (
              <MessageBubble key={msg.id} msg={msg} />
            ))}
            {loading && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>

          {/* Scroll-to-bottom button */}
          {showScrollBtn && (
            <button
              onClick={() => scrollToBottom(true)}
              className="absolute right-3 bottom-20 flex h-7 w-7 items-center justify-center rounded-full shadow-lg transition-all hover:scale-110"
              style={{
                background: "rgba(99,102,241,0.9)",
                border: "1px solid rgba(99,102,241,0.5)",
              }}
            >
              <ChevronDown size={14} className="text-white" />
            </button>
          )}

          {/* Quick prompts — show only when few messages */}
          {messages.length <= 2 && (
            <div className="px-3 pb-2 flex-shrink-0">
              <p className="text-[10px] text-slate-600 mb-1.5 px-1">
                Suggested questions:
              </p>
              <div className="flex flex-wrap gap-1.5">
                {QUICK_PROMPTS.slice(0, 4).map((p) => (
                  <button
                    key={p}
                    onClick={() => sendMessage(p)}
                    className="rounded-full px-2.5 py-1 text-[11px] font-medium transition-all hover:scale-105 active:scale-95"
                    style={{
                      background: "rgba(99,102,241,0.12)",
                      border: "1px solid rgba(99,102,241,0.25)",
                      color: "#a5b4fc",
                    }}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div
            className="flex-shrink-0 p-3"
            style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
          >
            <div
              className="flex items-end gap-2 rounded-xl px-3 py-2"
              style={{
                background: "rgba(255,255,255,0.05)",
                border: "1px solid rgba(99,102,241,0.2)",
                transition: "border-color 0.2s",
              }}
              onFocus={(e) =>
                ((e.currentTarget as HTMLElement).style.borderColor =
                  "rgba(99,102,241,0.5)")
              }
              onBlur={(e) =>
                ((e.currentTarget as HTMLElement).style.borderColor =
                  "rgba(99,102,241,0.2)")
              }
            >
              <textarea
                ref={inputRef}
                id="chatbot-input"
                value={input}
                onChange={(e) => {
                  setInput(e.target.value);
                  e.target.style.height = "auto";
                  e.target.style.height =
                    Math.min(e.target.scrollHeight, 96) + "px";
                }}
                onKeyDown={handleKeyDown}
                disabled={loading}
                placeholder="Ask anything about PhishScope..."
                rows={1}
                className="flex-1 bg-transparent text-xs text-white placeholder-slate-600 resize-none outline-none chatbot-input"
                style={{ maxHeight: "96px", lineHeight: "1.5" }}
              />
              <button
                id="chatbot-send"
                onClick={() => sendMessage(input)}
                disabled={!input.trim() || loading}
                className="flex-shrink-0 flex h-7 w-7 items-center justify-center rounded-lg transition-all hover:scale-110 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed"
                style={{
                  background: "linear-gradient(135deg,#6366f1,#8b5cf6)",
                }}
              >
                {loading ? (
                  <RefreshCw size={12} className="text-white animate-spin" />
                ) : (
                  <Send size={12} className="text-white" />
                )}
              </button>
            </div>
            <p className="text-center text-[10px] text-slate-700 mt-1.5">
              Powered by Google Gemini · Press Enter to send
            </p>
          </div>
        </div>
      )}
    </>
  );
}
