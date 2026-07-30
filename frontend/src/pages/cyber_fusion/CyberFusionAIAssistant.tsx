import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function CyberFusionAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the Apex Cyber Fusion AI Assistant. I have ultimate cross-domain visibility across SOC, DFIR, Cloud Security, AppSec, and Identity Security. How can I assist with your enterprise defense strategy today?'
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
        content: `I analyzed the enterprise fusion graph regarding "${newMsg.content}". \n\n**Observed Evidence:** A High-Severity identity anomaly (Impossible Travel via Okta) correlated precisely with a Medium-Severity cloud event (AWS EC2 Image Builder started in a non-standard region), followed by a Critical SOC alert (Outbound C2 traffic on port 4444).\n\n**Calculated Metrics:** The Enterprise Risk Index has spiked from 24 to 89 in the last 15 minutes due to this cross-domain kill chain.\n\n**Analytical Assessment:** This is a confirmed, multi-stage compromise involving credential theft, cloud workload hijacking, and active command-and-control.\n\n**Strategic Recommendation:** I have drafted a unified response playbook: 1. Revoke the compromised Okta session (Identity CC). 2. Quarantine the EC2 instance (Cloud CC). 3. Isolate the impacted network segment (SOC). Please approve this cross-domain response in the Fusion Dashboard.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{CFAI_STYLES}</style>
      <div className="cfai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="cfai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Cyber Fusion AI Assistant</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="cfai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`cfai-msg-row ${msg.role === 'ai' ? 'cfai-msg-ai' : 'cfai-msg-user'}`}>
            <div className="cfai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#34d399" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="cfai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="cfai-input-area">
        <div className="cfai-input-wrapper">
          <input 
            type="text" 
            className="cfai-input" 
            placeholder="Ask for an executive summary, cross-domain threat analysis, or response playbook..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="cfai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const CFAI_STYLES = `
.cfai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.cfai-header-icon { width: 36px; height: 36px; background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #34d399; }
.cfai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.cfai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.cfai-msg-ai { align-self: flex-start; }
.cfai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.cfai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.cfai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.cfai-msg-user .cfai-bubble { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.2); color: #e2e8f0; }
.cfai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.cfai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.cfai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.cfai-input:focus { border-color: #10b981; }
.cfai-send-btn { background: #10b981; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.cfai-send-btn:hover { background: #059669; }
`;
