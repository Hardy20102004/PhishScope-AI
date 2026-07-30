import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function IdentityCCAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the Apex Command Center AI Assistant. I have cross-platform visibility into your ISPM, ZTA, PAM, ITDR, IGA, NHI, Passwordless, and Federation modules. How can I assist you in securing the enterprise today?'
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
        content: `I analyzed the enterprise-wide posture regarding "${newMsg.content}". \n\n**Observed Evidence:** Across 12,450 identities, we have 142 federated trusts. 3 AWS Admin accounts currently have standing privileges without JIT policies attached (PAM Module).\n\n**Calculated Metrics:** The global Identity Trust Score is 88, but the Privileged Access Health score is suffering (72/100) due to these standing privileges.\n\n**Analytical Assessment:** The lack of JIT on these 3 accounts violates the core Zero Trust mandate and creates a critical threat vector for ITDR.\n\n**Strategic Recommendation:** Deploy the unified JIT elevation workflow for these 3 AWS Admin accounts. I have drafted the policy in the Governance module for your human approval.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{CCAI_STYLES}</style>
      <div className="ccai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="ccai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Command Center AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="ccai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`ccai-msg-row ${msg.role === 'ai' ? 'ccai-msg-ai' : 'ccai-msg-user'}`}>
            <div className="ccai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#c084fc" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="ccai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="ccai-input-area">
        <div className="ccai-input-wrapper">
          <input 
            type="text" 
            className="ccai-input" 
            placeholder="Ask for an executive summary, cross-module risk analysis, or ZTA roadmaps..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="ccai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const CCAI_STYLES = `
.ccai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.ccai-header-icon { width: 36px; height: 36px; background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #c084fc; }
.ccai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.ccai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.ccai-msg-ai { align-self: flex-start; }
.ccai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.ccai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ccai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.ccai-msg-user .ccai-bubble { background: rgba(168,85,247,0.1); border-color: rgba(168,85,247,0.2); color: #e2e8f0; }
.ccai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.ccai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.ccai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.ccai-input:focus { border-color: #a855f7; }
.ccai-send-btn { background: #a855f7; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.ccai-send-btn:hover { background: #9333ea; }
`;
