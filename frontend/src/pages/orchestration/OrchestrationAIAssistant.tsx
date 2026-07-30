import React, { useState } from 'react';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';

export default function OrchestrationAIAssistant() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I am the Orchestration AI Copilot. I can draft workflows, analyze pending decisions, and execute approved playbooks across the PHOENIX platform. How can I assist you?'
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
        content: `I analyzed the orchestration state regarding "${newMsg.content}". \n\n**Observed Evidence:** There are currently 3 active tasks assigned to the AI Agent (Brain), and 1 pending human approval for AWS Network Isolation.\n\n**Calculated Metrics:** The average automated task completion time is currently 1.2 seconds, down 15% from last week.\n\n**Analytical Assessment:** The orchestration engine is running optimally, but the pending human approval is blocking incident containment.\n\n**Strategic Recommendation:** I recommend opening the Decision Intelligence dashboard to review and approve the AWS Network Isolation playbook execution to prevent lateral movement.`
      }]);
    }, 1000);
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', height: '100vh', display: 'flex', flexDirection: 'column', color: '#e2e8f0' }}>
      <style>{OAI_STYLES}</style>
      <div className="oai-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div className="oai-header-icon"><Bot size={20} /></div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Orchestration AI Copilot</h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Powered by Enterprise AI Security Brain</p>
          </div>
        </div>
      </div>

      <div className="oai-chat-area">
        {messages.map(msg => (
          <div key={msg.id} className={`oai-msg-row ${msg.role === 'ai' ? 'oai-msg-ai' : 'oai-msg-user'}`}>
            <div className="oai-avatar">
              {msg.role === 'ai' ? <Sparkles size={16} color="#ec4899" /> : <UserIcon size={16} color="#94a3b8" />}
            </div>
            <div className="oai-bubble">
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem', lineHeight: 1.5 }}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="oai-input-area">
        <div className="oai-input-wrapper">
          <input 
            type="text" 
            className="oai-input" 
            placeholder="Ask to build a new playbook, review pending approvals, or summarize tasks..." 
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button className="oai-send-btn" onClick={handleSend}><Send size={18} /></button>
        </div>
      </div>
    </div>
  );
}

const OAI_STYLES = `
.oai-header { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.oai-header-icon { width: 36px; height: 36px; background: rgba(236,72,153,0.15); border: 1px solid rgba(236,72,153,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #f472b6; }
.oai-chat-area { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
.oai-msg-row { display: flex; gap: 16px; max-width: 80%; }
.oai-msg-ai { align-self: flex-start; }
.oai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.oai-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.oai-bubble { padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; }
.oai-msg-user .oai-bubble { background: rgba(236,72,153,0.1); border-color: rgba(236,72,153,0.2); color: #e2e8f0; }
.oai-input-area { padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
.oai-input-wrapper { display: flex; gap: 12px; max-width: 900px; margin: 0 auto; }
.oai-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: white; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
.oai-input:focus { border-color: #ec4899; }
.oai-send-btn { background: #ec4899; color: white; border: none; border-radius: 8px; width: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: background 0.2s; }
.oai-send-btn:hover { background: #db2777; }
`;
