import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Brain, Send, Shield, Users, Lock, Network, AlertTriangle, CheckCircle, ChevronRight, Zap, TrendingUp } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sections?: { title: string; content: string; type?: string }[];
  timestamp: Date;
}

const MOCK_RESPONSE = (query: string): Message => ({
  id: Date.now().toString(),
  role: 'assistant',
  timestamp: new Date(),
  content: `I've analyzed the enterprise identity security posture for your query: "${query}"`,
  sections: [
    {
      title: '📋 Observed Evidence',
      type: 'evidence',
      content: '• 847 total identities discovered across 6 connected providers (Entra ID, Active Directory, Okta, AWS IAM, GCP IAM, Kubernetes RBAC)\n• 74.2% MFA coverage — 219 identities without MFA protection\n• 43 privileged accounts identified, 7 without MFA\n• 67 dormant identities, 12 orphaned identities\n• 156 open governance findings (18 critical, 47 high)\n• Zero Trust readiness score: 42.8/100 — INITIAL maturity'
    },
    {
      title: '📊 Calculated Metrics',
      type: 'metrics',
      content: '• Authentication Score: 61.4/100 (below 80 target)\n• Average Identity Risk Score: 31.7/100\n• Critical-risk identities: 23 (2.7% of inventory)\n• Phishing-resistant auth coverage: 22.1% (target: 80%)\n• SSO coverage: 68.5% (target: 80%)\n• NIST SP 800-63 compliance: 67.3%'
    },
    {
      title: '🧠 Analytical Assessment',
      type: 'assessment',
      content: 'The enterprise identity posture presents elevated risk across three critical dimensions:\n\n1. AUTHENTICATION GAP: With 25.8% of identities lacking MFA and 7 privileged accounts using password-only authentication, the organization is materially exposed to credential-based attacks (MITRE T1078, T1110). SMS-based MFA (15% of MFA methods) provides weak protection against SIM-swap attacks.\n\n2. PRIVILEGE SPRAWL: 73 excess permission grants and 7 detected SoD violations indicate significant privilege creep. Admin sprawl (43 privileged accounts = 5.1% of total) exceeds the recommended 3-5% threshold.\n\n3. ZERO TRUST DEFICIT: At INITIAL maturity, the organization lacks continuous identity verification, device trust enforcement, and session risk evaluation — three foundational Zero Trust pillars (NIST SP 800-207).'
    },
    {
      title: '✅ Recommendations',
      type: 'recommendations',
      content: '1. [CRITICAL] Immediately enforce MFA for all 7 privileged accounts without MFA\n2. [CRITICAL] Disable orphaned-svc-legacy (risk score: 94.1 — dormant 241 days with privileged access)\n3. [HIGH] Initiate enterprise-wide MFA enrollment campaign targeting 95% coverage in 60 days\n4. [HIGH] Begin JIT (Just-in-Time) privileged access implementation via PAM/PIM\n5. [MEDIUM] Implement FIDO2/passkey rollout for 80% of identities within 90 days\n6. [MEDIUM] Run access certification campaign for 67 dormant identities'
    },
    {
      title: '⚠️ Assumptions',
      type: 'assumptions',
      content: '• Risk scores are calculated from available discovery data and may not reflect all behavioral signals\n• Governance findings are based on policy rules and may require business context validation\n• Zero Trust pillar scores for non-identity pillars (Devices, Networks, Data) include estimated values from adjacent telemetry\n• Threat intelligence enrichment reflects sample data in this deployment'
    }
  ]
});

const SUGGESTED_QUERIES = [
  'What are the highest-risk identities in the enterprise?',
  'How is our Zero Trust readiness compared to NIST SP 800-207?',
  'Summarize all dormant and orphaned identity risks',
  'Which privileged accounts lack MFA protection?',
  'What is our NIST SP 800-63 compliance posture?',
  'Generate an identity security improvement roadmap',
  'Analyze authentication method gaps and risks',
  'What SoD violations are detected?',
];

const TypeColors: Record<string, string> = {
  evidence: '#6366f1', metrics: '#06b6d4', assessment: '#8b5cf6',
  recommendations: '#10b981', assumptions: '#f59e0b'
};

export default function ISPMAIAssistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      timestamp: new Date(),
      content: '',
      sections: [
        { title: '👋 Welcome to the ISPM AI Assistant', type: 'evidence', content: 'I am the PHOENIX X Identity Security AI — powered by the AI Security Brain and Multi-Agent AI Framework.\n\nI analyze your enterprise identity security posture using 5-layer explainable AI output:\n\n• Observed Evidence (from identity discovery)\n• Calculated Metrics (computed scores)\n• Analytical Assessment (AI reasoning)\n• Recommendations (actionable guidance)\n• Assumptions (data completeness caveats)\n\nAsk me anything about your identity security posture, Zero Trust readiness, or governance findings.' }
      ]
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const submit = (query: string = input) => {
    if (!query.trim() || loading) return;
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: query, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setTimeout(() => {
      setMessages(prev => [...prev, MOCK_RESPONSE(query)]);
      setLoading(false);
    }, 1200);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{AI_STYLES}</style>

      {/* Header */}
      <div className="ai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="ai-header-icon"><Brain size={22} /></div>
          <div>
            <h1 className="ai-header-title">Identity Security AI Assistant</h1>
            <p className="ai-header-subtitle">5-Layer XAI · NIST SP 800-63 · Zero Trust · Governance Analysis · MITRE ATT&CK</p>
          </div>
        </div>
        <Link to="/ispm" style={{ textDecoration: 'none', color: '#818cf8', fontSize: '0.8rem', padding: '7px 13px', background: 'rgba(99,102,241,0.12)', borderRadius: 9, border: '1px solid rgba(99,102,241,0.3)' }}>← ISPM</Link>
      </div>

      {/* Suggested Queries */}
      {messages.length <= 1 && (
        <div className="ai-suggestions">
          {SUGGESTED_QUERIES.map(q => (
            <button key={q} className="ai-suggestion-btn" onClick={() => submit(q)}>
              <Zap size={12} />
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Chat Area */}
      <div className="ai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`ai-message ai-message-${msg.role}`}>
            {msg.role === 'assistant' && (
              <div className="ai-avatar"><Brain size={16} /></div>
            )}
            <div className="ai-message-content">
              {msg.content && <p className="ai-message-text">{msg.content}</p>}
              {msg.sections?.map(section => (
                <div key={section.title} className="ai-section" style={{ borderLeftColor: TypeColors[section.type || ''] || '#6366f1' }}>
                  <div className="ai-section-title" style={{ color: TypeColors[section.type || ''] || '#6366f1' }}>{section.title}</div>
                  <div className="ai-section-body">{section.content}</div>
                </div>
              ))}
              <div className="ai-message-time">{msg.timestamp.toLocaleTimeString()}</div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="ai-message ai-message-assistant">
            <div className="ai-avatar"><Brain size={16} /></div>
            <div className="ai-loading">
              <span /><span /><span />
              <span style={{ fontSize: '0.78rem', color: '#64748b', marginLeft: 8 }}>Analyzing identity security posture...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="ai-input-area">
        <div className="ai-input-box">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && submit()}
            placeholder="Ask about identity risks, Zero Trust readiness, governance findings, MFA coverage..."
            disabled={loading}
          />
          <button className="ai-send-btn" onClick={() => submit()} disabled={!input.trim() || loading}>
            <Send size={16} />
          </button>
        </div>
        <p className="ai-disclaimer">AI outputs are explainable and include evidence, metrics, assessment, recommendations, and assumptions.</p>
      </div>
    </div>
  );
}

const AI_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.ai-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; background: rgba(255,255,255,0.02); border-bottom: 1px solid rgba(255,255,255,0.07); flex-shrink: 0; }
.ai-header-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 11px; display: flex; align-items: center; justify-content: center; color: white; }
.ai-header-title { font-size: 1.1rem; font-weight: 800; color: #fff; margin: 0 0 2px; }
.ai-header-subtitle { font-size: 0.72rem; color: #64748b; margin: 0; }
.ai-suggestions { display: flex; gap: 8px; padding: 14px 24px; flex-wrap: wrap; background: rgba(255,255,255,0.01); border-bottom: 1px solid rgba(255,255,255,0.05); flex-shrink: 0; }
.ai-suggestion-btn { display: flex; align-items: center; gap: 6px; padding: 7px 12px; border-radius: 8px; background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.25); color: #818cf8; font-size: 0.75rem; cursor: pointer; transition: all 0.15s; }
.ai-suggestion-btn:hover { background: rgba(99,102,241,0.2); }
.ai-chat-area { flex: 1; overflow-y: auto; padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; }
.ai-message { display: flex; gap: 12px; }
.ai-message-assistant { align-items: flex-start; }
.ai-message-user { flex-direction: row-reverse; }
.ai-avatar { width: 34px; height: 34px; border-radius: 10px; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0; }
.ai-message-content { max-width: 85%; }
.ai-message-user .ai-message-content { background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3); border-radius: 14px 4px 14px 14px; padding: 12px 16px; }
.ai-message-assistant .ai-message-content { flex: 1; }
.ai-message-text { font-size: 0.85rem; color: #e2e8f0; margin: 0 0 10px; line-height: 1.5; }
.ai-message-user .ai-message-text { color: #c4b5fd; }
.ai-message-time { font-size: 0.68rem; color: #475569; margin-top: 6px; }
.ai-section { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-left: 3px solid; border-radius: 0 10px 10px 0; padding: 12px 14px; margin-bottom: 10px; }
.ai-section-title { font-size: 0.82rem; font-weight: 700; margin-bottom: 8px; }
.ai-section-body { font-size: 0.81rem; color: #94a3b8; white-space: pre-wrap; line-height: 1.6; }
.ai-loading { display: flex; align-items: center; padding: 12px 0; }
.ai-loading span:not(:last-child) { width: 7px; height: 7px; border-radius: 50%; background: #6366f1; margin-right: 5px; animation: ai-bounce 1.2s infinite; }
.ai-loading span:nth-child(2) { animation-delay: 0.2s; }
.ai-loading span:nth-child(3) { animation-delay: 0.4s; }
@keyframes ai-bounce { 0%,80%,100% { transform: scale(0.6); opacity: 0.5; } 40% { transform: scale(1); opacity: 1; } }
.ai-input-area { padding: 14px 24px; background: rgba(255,255,255,0.02); border-top: 1px solid rgba(255,255,255,0.07); flex-shrink: 0; }
.ai-input-box { display: flex; gap: 10px; margin-bottom: 6px; }
.ai-input-box input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 12px 16px; color: #e2e8f0; font-size: 0.85rem; outline: none; transition: border-color 0.2s; }
.ai-input-box input:focus { border-color: rgba(99,102,241,0.5); }
.ai-input-box input::placeholder { color: #475569; }
.ai-send-btn { width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; flex-shrink: 0; }
.ai-send-btn:hover:not(:disabled) { opacity: 0.85; transform: scale(1.05); }
.ai-send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.ai-disclaimer { font-size: 0.68rem; color: #475569; text-align: center; margin: 0; }
`;
