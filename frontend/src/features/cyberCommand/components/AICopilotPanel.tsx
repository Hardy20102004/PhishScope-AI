import { useState, useEffect, useRef } from 'react';
import { Send, Bot, Sparkles, Globe, Map } from 'lucide-react';
import axios from 'axios';

export function AICopilotPanel() {
  const [messages, setMessages] = useState([
    {
      id: '1',
      sender: 'ai',
      text: 'I am the Apex AI Executive Copilot. I have synthesized intelligence from the SOC, Cloud Security, Threat Intelligence, and Governance platforms. The enterprise posture is currently stable at 92.5%.',
      type: 'greeting'
    }
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const { data } = await axios.post('/api/v1/ai-brain/orchestrate', {
        input_text: userMessage.text,
        intent: "GENERAL_QUERY",
        capability: "SOC Copilot",
        session_id: "apex-ui-session"
      });
      
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: data.response_text,
        type: 'analysis'
      };
      
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('AI Copilot error:', error);
      const errResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: "I encountered a communication error with the AI Brain backend.",
        type: 'error'
      };
      setMessages(prev => [...prev, errResponse]);
    }
  };

  return (
    <div className="flex flex-col h-full bg-card border-l">
      <div className="p-4 border-b flex items-center space-x-3 bg-card sticky top-0 z-10">
        <div className="bg-primary/20 p-2 rounded-lg">
          <Globe className="h-5 w-5 text-primary" />
        </div>
        <div>
          <h2 className="font-semibold text-foreground text-sm">Apex Copilot</h2>
          <p className="text-xs text-emerald-500 flex items-center">
            <span className="w-2 h-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
            Cross-Domain Analysis Active
          </p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex space-x-2 max-w-[85%] ${msg.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              <div className="shrink-0 mt-1">
                {msg.sender === 'ai' ? (
                  <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-primary" />
                  </div>
                ) : (
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-xs font-medium">
                    CMD
                  </div>
                )}
              </div>
              
              <div className={`rounded-xl p-3 text-sm shadow-sm ${
                msg.sender === 'user' 
                  ? 'bg-primary text-primary-foreground' 
                  : 'bg-secondary text-foreground'
              }`}>
                {msg.type === 'analysis' && (
                  <div className="flex items-center space-x-1.5 mb-2 text-primary">
                    <Sparkles className="h-3.5 w-3.5" />
                    <span className="text-xs font-semibold uppercase tracking-wider">Apex Insight</span>
                  </div>
                )}
                
                <p className="leading-relaxed">{msg.text}</p>
                
                {msg.type === 'analysis' && (
                  <div className="mt-3 pt-3 border-t border-border/50">
                    <button className="flex items-center text-xs font-medium text-primary hover:underline">
                      <Map className="mr-1.5 h-3.5 w-3.5" />
                      View Strategic Timeline
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t bg-card">
        <div className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about enterprise posture..."
            className="w-full bg-secondary/50 border border-border rounded-full pl-4 pr-12 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-primary focus:bg-secondary transition-all"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim()}
            className="absolute right-1.5 p-2 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
