import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function ITDRAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the ITDR AI Assistant. I can analyze authentication logs, interpret behavioral anomalies, summarize identity timelines, and provide response recommendations. How can I assist you today?'
    }
  ]);

  const handleSend = () => {
    if (!query.trim()) return;
    const newMsg = { id: Date.now(), role: 'user', content: query };
    setMessages([...messages, newMsg]);
    setQuery('');

    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'ai',
        content: `I analyzed the identity timeline for "${newMsg.content}". \n\n**Observed Evidence:** The user \`alice.security\` authenticated successfully from Seattle, WA, and 30 minutes later failed authentication from Moscow, RU.\n\n**Calculated Metrics:** Travel velocity exceeds physical limits (Impossible Travel).\n\n**Analytical Assessment:** High probability of credential compromise. The second authentication attempt was likely a malicious actor using stolen credentials.\n\n**Recommendation:** Isolate the account immediately, revoke all active sessions, and force a password reset.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{ITDR_AI_STYLES}</style>
      <div className="iai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="iai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>ITDR AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="iai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`iai-msg-row ${msg.role === 'ai' ? 'iai-msg-ai' : 'iai-msg-user'}`}>
            <div className="iai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#ef4444" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="iai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="iai-input-area">
        <div className="iai-input-wrapper">
          <input 
            type="text" 
            className="iai-input" 
            placeholder="Ask about identity threats, impossible travel, or credential attacks..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="iai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const ITDR_AI_STYLES = `
.iai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.iai-header-icon { width: 36px; height: 36px; background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #ef4444; }
.iai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.iai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.iai-msg-ai { align-self: flex-start; }
.iai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.iai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.iai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.iai-msg-user .iai-bubble { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.2); color: #e2e8f0; }
.iai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.iai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.iai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.iai-input:focus { border-color: #ef4444; }
.iai-send-btn { background: #ef4444; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.iai-send-btn:hover { background: #dc2626; }
`;
