import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function ResilienceAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the Cyber Resilience AI Copilot. I can assess Disaster Recovery readiness, generate Business Continuity summaries, or help design a tabletop exercise. How can I assist you today?'
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
        content: `I analyzed the resilience metrics regarding "${newMsg.content}". \n\n**Observed Evidence:** The "Global Identity Auth" service currently meets its RTO of 15m (Actual: 12m), but recent DR tests show failures in cross-region failover.\n\n**Readiness Assessment:** Overall enterprise recovery readiness is at 88%, but Cloud Resilience has dropped to 74% due to untested Azure backups.\n\n**Recommendation:** I recommend scheduling a Tabletop Exercise focused on Azure tenant compromise to validate our updated BCP procedures. Would you like me to draft the scenario and invite the necessary stakeholders?`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{PAI_STYLES}</style>
      <div className="pai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="pai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Resilience AI Copilot</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="pai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`pai-msg-row ${msg.role === 'ai' ? 'pai-msg-ai' : 'pai-msg-user'}`}>
            <div className="pai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#10b981" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="pai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="pai-input-area">
        <div className="pai-input-wrapper">
          <input 
            type="text" 
            className="pai-input" 
            placeholder="Ask to summarize DR readiness, assess BCP gaps, or design a crisis simulation..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="pai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const PAI_STYLES = `
.pai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.pai-header-icon { width: 36px; height: 36px; background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #34d399; }
.pai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.pai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.pai-msg-ai { align-self: flex-start; }
.pai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.pai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.pai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.pai-msg-user .pai-bubble { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.2); color: #e2e8f0; }
.pai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.pai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.pai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.pai-input:focus { border-color: #10b981; }
.pai-send-btn { background: #10b981; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.pai-send-btn:hover { background: #059669; }
`;
