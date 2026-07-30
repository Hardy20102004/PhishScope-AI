import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function IGAAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the IGA AI Assistant. I can help evaluate Segregation of Duties conflicts, summarize access certification progress, or explain governance risks. How can I assist you today?'
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
        content: `I analyzed the Segregation of Duties violation for "${newMsg.content}". \n\n**Observed Evidence:** The user \`alice.smith\` currently holds both the "AP Clerk" and "AP Manager" roles.\n\n**Calculated Metrics:** This violates SoD Rule #12 (Accounts Payable Separation).\n\n**Analytical Assessment:** This combination allows a single user to both create and approve vendor payments, presenting a high risk of financial fraud.\n\n**Recommendation:** Revoke the "AP Clerk" role from \`alice.smith\` immediately. Ensure an access certification campaign is triggered for the Finance department.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{IGA_AI_STYLES}</style>
      <div className="iaia-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="iaia-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>IGA AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="iaia-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`iaia-msg-row ${msg.role === 'ai' ? 'iaia-msg-ai' : 'iaia-msg-user'}`}>
            <div className="iaia-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#14b8a6" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="iaia-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="iaia-input-area">
        <div className="iaia-input-wrapper">
          <input 
            type="text" 
            className="iaia-input" 
            placeholder="Ask about SoD conflicts, access requests, or UAR progress..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="iaia-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const IGA_AI_STYLES = `
.iaia-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.iaia-header-icon { width: 36px; height: 36px; background: rgba(20,184,166,0.15); border: 1px solid rgba(20,184,166,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #14b8a6; }
.iaia-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.iaia-msg-row { display: flex; gap: 16px; max-width: 80%; }
.iaia-msg-ai { align-self: flex-start; }
.iaia-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.iaia-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.iaia-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.iaia-msg-user .iaia-bubble { background: rgba(20,184,166,0.1); border-color: rgba(20,184,166,0.2); color: #e2e8f0; }
.iaia-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.iaia-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.iaia-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.iaia-input:focus { border-color: #14b8a6; }
.iaia-send-btn { background: #14b8a6; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.iaia-send-btn:hover { background: #0d9488; }
`;
