import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function DigitalTwinAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the Cyber Digital Twin AI Assistant. I can simulate architectural changes, forecast risk trends, and map hypothetical attack paths. What enterprise scenario would you like to model today?'
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
        content: `I analyzed the digital twin representation regarding "${newMsg.content}". \n\n**Simulated Results:** Implementing strict Zero Trust segmentation on the core AWS VPCs eliminates 14 distinct attack paths originating from the guest wireless subnet.\n\n**Calculated Metrics:** This architectural change would increase the Enterprise Resilience Score from 88% to 94%.\n\n**Analytical Assessment:** The primary risk surface is currently legacy inter-VPC peering. Enforcing granular micro-segmentation successfully breaks the simulated kill chains.\n\n**Recommendations:** 1. Deploy the tested AWS security group configurations. 2. Verify identity-based conditional access before fully deprecating the legacy VPN.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{DTAI_STYLES}</style>
      <div className="dtai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="dtai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Digital Twin AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="dtai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`dtai-msg-row ${msg.role === 'ai' ? 'dtai-msg-ai' : 'dtai-msg-user'}`}>
            <div className="dtai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#0ea5e9" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="dtai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="dtai-input-area">
        <div className="dtai-input-wrapper">
          <input 
            type="text" 
            className="dtai-input" 
            placeholder="Ask to run a simulation, find an attack path, or assess resilience..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="dtai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const DTAI_STYLES = `
.dtai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.dtai-header-icon { width: 36px; height: 36px; background: rgba(14,165,233,0.15); border: 1px solid rgba(14,165,233,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #38bdf8; }
.dtai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.dtai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.dtai-msg-ai { align-self: flex-start; }
.dtai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.dtai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.dtai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.dtai-msg-user .dtai-bubble { background: rgba(14,165,233,0.1); border-color: rgba(14,165,233,0.2); color: #e2e8f0; }
.dtai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.dtai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.dtai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.dtai-input:focus { border-color: #0ea5e9; }
.dtai-send-btn { background: #0ea5e9; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.dtai-send-btn:hover { background: #0284c7; }
`;
