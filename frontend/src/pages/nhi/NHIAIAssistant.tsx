import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function NHIAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the NHI AI Assistant. I can help investigate over-permissioned service accounts, analyze trust relationships, or explain workload identity risks. How can I assist you today?'
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
        content: `I analyzed the risk for "${newMsg.content}". \n\n**Observed Evidence:** The service account \`dev-ci-pipeline\` has the \`AdministratorAccess\` policy attached in AWS.\n\n**Calculated Metrics:** This identity has not used 94% of its granted permissions in the last 90 days.\n\n**Analytical Assessment:** This violates Least Privilege. If the CI/CD pipeline is compromised, the attacker gains full administrative control over the GCP Development environment.\n\n**Recommendation:** Downgrade the permissions to match observed usage. I have generated a scoped IAM policy tailored to the exact actions this pipeline performs.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{NHI_AI_STYLES}</style>
      <div className="nhiai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="nhiai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>NHI AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="nhiai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`nhiai-msg-row ${msg.role === 'ai' ? 'nhiai-msg-ai' : 'nhiai-msg-user'}`}>
            <div className="nhiai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#3b82f6" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="nhiai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="nhiai-input-area">
        <div className="nhiai-input-wrapper">
          <input 
            type="text" 
            className="nhiai-input" 
            placeholder="Ask about service accounts, API keys, or trust chains..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="nhiai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const NHI_AI_STYLES = `
.nhiai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.nhiai-header-icon { width: 36px; height: 36px; background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #3b82f6; }
.nhiai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.nhiai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.nhiai-msg-ai { align-self: flex-start; }
.nhiai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.nhiai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.nhiai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.nhiai-msg-user .nhiai-bubble { background: rgba(59,130,246,0.1); border-color: rgba(59,130,246,0.2); color: #e2e8f0; }
.nhiai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.nhiai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.nhiai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.nhiai-input:focus { border-color: #3b82f6; }
.nhiai-send-btn { background: #3b82f6; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.nhiai-send-btn:hover { background: #2563eb; }
`;
