import { useState } from 'react';
import { Bot, Sparkles, Send, BrainCircuit, Shield } from 'lucide-react';

interface Props {
  currentContext: string;
}

export function UnifiedAIPanel({ currentContext }: Props) {
  const [input, setInput] = useState('');

  return (
    <div className="flex flex-col h-full bg-card">
      <div className="p-4 border-b flex items-center space-x-3 sticky top-0 z-10 bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/75">
        <div className="bg-primary/20 p-2 rounded-lg relative overflow-hidden">
          <div className="absolute inset-0 bg-primary/20 animate-pulse"></div>
          <BrainCircuit className="h-5 w-5 text-primary relative z-10" />
        </div>
        <div>
          <h2 className="font-bold tracking-tight text-foreground text-sm uppercase">Unified AI Brain</h2>
          <p className="text-[10px] uppercase font-bold text-emerald-500 tracking-wider flex items-center mt-0.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
            Context: {currentContext.replace('-', ' ')}
          </p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Initial Greeting Contextualized */}
        <div className="flex justify-start">
          <div className="flex space-x-2 max-w-[85%]">
            <div className="shrink-0 mt-1">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30">
                <Bot className="h-4 w-4 text-primary" />
              </div>
            </div>
            <div className="rounded-xl p-3 text-sm shadow-sm bg-secondary text-foreground border border-border/50">
              <div className="flex items-center space-x-1.5 mb-2 text-primary">
                <Sparkles className="h-3.5 w-3.5" />
                <span className="text-[10px] font-bold uppercase tracking-wider">System Analysis</span>
              </div>
              <p className="leading-relaxed">
                I am the Unified AI Security Brain. I am currently monitoring all 22 active CyberOS modules.
              </p>
              <div className="mt-3 bg-background/50 rounded p-2 text-xs border">
                <strong>Current Posture:</strong> 99.9% Nominal<br/>
                <strong>Recommendations:</strong> No immediate action required across the enterprise fleet.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 border-t bg-card">
        <div className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Query the enterprise graph..."
            className="w-full bg-secondary border border-border rounded-lg pl-4 pr-12 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-primary focus:bg-background transition-all shadow-inner"
          />
          <button
            disabled={!input.trim()}
            className="absolute right-1.5 p-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <div className="mt-2 text-center">
           <span className="text-[10px] text-muted-foreground uppercase font-semibold tracking-wider">Protected by Enterprise Human Governance</span>
        </div>
      </div>
    </div>
  );
}
