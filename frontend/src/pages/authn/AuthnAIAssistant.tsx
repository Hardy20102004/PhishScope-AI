import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function AuthnAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the AUTHN AI Assistant. I can help analyze legacy authentication usage, recommend passkey migration paths, or assess your organization\\'s overall Authentication Assurance Level (AAL). How can I assist you?'
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
        content: `I analyzed the authentication posture for "${newMsg.content}". \n\n**Observed Evidence:** The \`Contractors Group\` is currently enforcing an AAL1 policy, relying solely on passwords and SMS OTP.\n\n**Calculated Metrics:** 94% of users in this group have compatible mobile devices capable of supporting platform authenticators (Passkeys).\n\n**Analytical Assessment:** Using SMS OTP exposes the organization to SIM swapping attacks, and passwords remain highly susceptible to phishing.\n\n**Recommendation:** Upgrade the policy to require AAL2. I have generated a staged rollout plan to prompt contractors to register a device-bound passkey during their next login session.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{AUTHN_AI_STYLES}</style>
      <div className="authnai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="authnai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>AUTHN AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="authnai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`authnai-msg-row ${msg.role === 'ai' ? 'authnai-msg-ai' : 'authnai-msg-user'}`}>
            <div className="authnai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#8b5cf6" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="authnai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="authnai-input-area">
        <div className="authnai-input-wrapper">
          <input 
            type="text" 
            className="authnai-input" 
            placeholder="Ask about passkey adoption, legacy auth deprecation, or AAL compliance..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="authnai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const AUTHN_AI_STYLES = `
.authnai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.authnai-header-icon { width: 36px; height: 36px; background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #8b5cf6; }
.authnai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.authnai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.authnai-msg-ai { align-self: flex-start; }
.authnai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.authnai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.authnai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.authnai-msg-user .authnai-bubble { background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.2); color: #e2e8f0; }
.authnai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.authnai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.authnai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.authnai-input:focus { border-color: #8b5cf6; }
.authnai-send-btn { background: #8b5cf6; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.authnai-send-btn:hover { background: #7c3aed; }
`;
