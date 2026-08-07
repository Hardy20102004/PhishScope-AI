import { useState, useEffect, useRef } from 'react';
import { BrainCircuit, Send, Bot, Sparkles, Network } from 'lucide-react';

export function AIKnowledgeEvolutionAssistant() {
  const [messages, setMessages] = useState([
    {
      id: '1',
      sender: 'ai',
      text: 'I am the AI Knowledge Evolution Assistant. I monitor the knowledge graph, discover new semantic relationships, and recommend schema updates. How can I help you evolve the graph today?',
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

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');

    // Simulate AI response
    setTimeout(() => {
      let aiResponseText = "I've analyzed the graph and identified potential improvements. I recommend merging the 'Malicious IP' and 'Attacker IP' entities.";
      if (input.toLowerCase().includes('quality')) {
        aiResponseText = "The knowledge quality is currently at 92%. Coverage is slightly low (88%) due to missing cloud metadata on legacy assets.";
      } else if (input.toLowerCase().includes('relationship')) {
        aiResponseText = "I've discovered 2 new highly-confident relationships linking recent login anomalies to the Lazarus malware family.";
      }
      
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: aiResponseText,
        type: 'analysis'
      };
      
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-full bg-card">
      <div className="p-4 border-b flex items-center space-x-3 bg-card sticky top-0 z-10">
        <div className="bg-primary/20 p-2 rounded-lg">
          <BrainCircuit className="h-5 w-5 text-primary" />
        </div>
        <div>
          <h2 className="font-semibold text-foreground text-sm">Knowledge AI</h2>
          <p className="text-xs text-emerald-500 flex items-center">
            <span className="w-2 h-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
            Evolution Engine Active
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
                    ME
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
                    <span className="text-xs font-semibold uppercase tracking-wider">Analysis</span>
                  </div>
                )}
                
                <p className="leading-relaxed">{msg.text}</p>
                
                {msg.type === 'analysis' && (
                  <div className="mt-3 pt-3 border-t border-border/50">
                    <button className="flex items-center text-xs font-medium text-primary hover:underline">
                      <Network className="mr-1.5 h-3.5 w-3.5" />
                      View Graph Updates
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
            placeholder="Ask about graph evolution..."
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
