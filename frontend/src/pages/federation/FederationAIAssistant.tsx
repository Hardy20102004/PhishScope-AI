import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function FederationAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the FEDERATION AI Assistant. I can help analyze cross-domain trust relationships, troubleshoot SAML/OIDC misconfigurations, or generate certificate rotation playbooks. How can I assist you?'
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
        content: `I analyzed the federation configuration for "${newMsg.content}". \n\n**Observed Evidence:** The \`Partner B2B Portal\` SAML integration does not enforce encrypted assertions from the external Identity Provider.\n\n**Calculated Metrics:** This exposes 14 sensitive claims (including group memberships and email) to interception during the assertion transmission.\n\n**Analytical Assessment:** This violates the Zero Trust architecture mandate for end-to-end encryption of federation tokens.\n\n**Recommendation:** Enable \`RequiresEncryptedAssertions\` on the Service Provider configuration and coordinate with the B2B partner to update their metadata XML with the new public encryption key.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{FED_AI_STYLES}</style>
      <div className="fedai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="fedai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>FEDERATION AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="fedai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`fedai-msg-row ${msg.role === 'ai' ? 'fedai-msg-ai' : 'fedai-msg-user'}`}>
            <div className="fedai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#38bdf8" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="fedai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="fedai-input-area">
        <div className="fedai-input-wrapper">
          <input 
            type="text" 
            className="fedai-input" 
            placeholder="Ask about SAML risks, SSO application mappings, or trust governance..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="fedai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const FED_AI_STYLES = `
.fedai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.fedai-header-icon { width: 36px; height: 36px; background: rgba(14,165,233,0.15); border: 1px solid rgba(14,165,233,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #38bdf8; }
.fedai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.fedai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.fedai-msg-ai { align-self: flex-start; }
.fedai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.fedai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.fedai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.fedai-msg-user .fedai-bubble { background: rgba(14,165,233,0.1); border-color: rgba(14,165,233,0.2); color: #e2e8f0; }
.fedai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.fedai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.fedai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.fedai-input:focus { border-color: #0ea5e9; }
.fedai-send-btn { background: #0ea5e9; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.fedai-send-btn:hover { background: #0284c7; }
`;
