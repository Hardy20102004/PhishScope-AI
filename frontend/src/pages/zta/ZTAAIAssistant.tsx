import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function ZTAAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the Zero Trust AI Assistant. I can explain continuous verification failures, analyze contextual risks, summarize policy gaps, and provide actionable recommendations. How can I assist you today?'
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
        content: `I analyzed the access logs for "${newMsg.content}". \n\n**Observed Evidence:** The device failed MDM compliance check and the location was anomalous.\n\n**Assessment:** High risk of session hijack.\n\n**Recommendation:** Create a Conditional Access policy to explicitly block this subnet and require step-up FIDO2 authentication.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{ZTA_AI_STYLES}</style>
      <div className="zai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="zai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Zero Trust AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="zai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`zai-msg-row ${msg.role === 'ai' ? 'zai-msg-ai' : 'zai-msg-user'}`}>
            <div className="zai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#c084fc" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="zai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="zai-input-area">
        <div className="zai-input-wrapper">
          <input 
            type="text" 
            className="zai-input" 
            placeholder="Ask about verification logs, access decisions, or policy impact..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="zai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const ZTA_AI_STYLES = `
.zai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.zai-header-icon { width: 36px; height: 36px; background: rgba(192,132,252,0.15); border: 1px solid rgba(192,132,252,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #c084fc; }
.zai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.zai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.zai-msg-ai { align-self: flex-start; }
.zai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.zai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.zai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.zai-msg-user .zai-bubble { background: rgba(99,102,241,0.1); border-color: rgba(99,102,241,0.2); color: #e2e8f0; }
.zai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.zai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.zai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.zai-input:focus { border-color: #6366f1; }
.zai-send-btn { background: #6366f1; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.zai-send-btn:hover { background: #4f46e5; }
`;
