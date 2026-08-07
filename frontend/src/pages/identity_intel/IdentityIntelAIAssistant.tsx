import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function IdentityIntelAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the IDENTITY INTEL AI Assistant. I can help analyze cross-platform identity telemetry, explain Adaptive Trust Scores, and generate strategic risk mitigation plans. How can I assist you?'
    }
  ]);

  const handleSend = () => {
    if (!query.trim()) return;
    const newMsg = { id: Date.now(), role: 'user', content: query };
    setMessages([...messages, newMsg]);
    setQuery('');

    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'ai',
        content: `I analyzed the identity intelligence telemetry for "${newMsg.content}". \n\n**Observed Evidence:** The identity \`david.smith (Admin)\` triggered an anomaly in the PAM module (accessing AWS Prod) simultaneously with a geo-velocity anomaly in the AUTHN module (login from unfamiliar region).\n\n**Calculated Metrics:** The Adaptive Trust Score for this identity has dropped from 92.0 to 45.2, falling below the threshold for privileged access.\n\n**Analytical Assessment:** This cross-platform correlation strongly indicates a compromised session or credential theft.\n\n**Recommendation:** Automatically revoke active AWS sessions via the Zero Trust broker and trigger an ITDR incident for SOC investigation.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{INTEL_AI_STYLES}</style>
      <div className="intelai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="intelai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>IDENTITY INTEL AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="intelai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`intelai-msg-row ${msg.role === 'ai' ? 'intelai-msg-ai' : 'intelai-msg-user'}`}>
            <div className="intelai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#2563eb" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="intelai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="intelai-input-area">
        <div className="intelai-input-wrapper">
          <input 
            type="text" 
            className="intelai-input" 
            placeholder="Ask about behavior anomalies, trust scores, or identity risks..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="intelai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const INTEL_AI_STYLES = `
.intelai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.intelai-header-icon { width: 36px; height: 36px; background: rgba(37,99,235,0.15); border: 1px solid rgba(37,99,235,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #60a5fa; }
.intelai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.intelai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.intelai-msg-ai { align-self: flex-start; }
.intelai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.intelai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.intelai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.intelai-msg-user .intelai-bubble { background: rgba(37,99,235,0.1); border-color: rgba(37,99,235,0.2); color: #e2e8f0; }
.intelai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.intelai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.intelai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.intelai-input:focus { border-color: #2563eb; }
.intelai-send-btn { background: #2563eb; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.intelai-send-btn:hover { background: #1d4ed8; }
`;
