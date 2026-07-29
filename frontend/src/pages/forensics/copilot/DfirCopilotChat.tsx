import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Bot, User, Send, Paperclip, ShieldAlert } from 'lucide-react';
import ExplanationBadge from './ExplanationBadge';
import SuggestedQuestions from './SuggestedQuestions';

export default function DfirCopilotChat() {
  const [query, setQuery] = useState('');

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col border-r border-slate-800">
        
        {/* Header */}
        <div className="p-4 border-b border-slate-800 bg-slate-950 flex items-center gap-3">
            <Bot className="text-violet-400" size={24} />
            <div>
                <h1 className="text-lg font-bold text-slate-200">AI DFIR Copilot</h1>
                <p className="text-xs text-slate-400">Context: Unified Investigation INV-8891</p>
            </div>
        </div>

        {/* Message Log */}
        <div className="flex-1 overflow-y-auto p-6 space-y-8">
            <UserMessage content="Summarize the events leading up to the execution of invoice.exe." />
            
            <CopilotMessage>
                <div className="space-y-4">
                    <div className="flex gap-4">
                        <ExplanationBadge type="OBSERVATION" />
                        <p className="text-sm text-slate-300">At 14:00 UTC, an email with subject 'Invoice Update' was delivered to ceo@company.com.</p>
                    </div>
                    <div className="flex gap-4">
                        <ExplanationBadge type="OBSERVATION" />
                        <p className="text-sm text-slate-300">Five minutes later, invoice.exe was written to Disk and executed.</p>
                    </div>
                    <div className="flex gap-4">
                        <ExplanationBadge type="ASSESSMENT" />
                        <p className="text-sm text-slate-300">This sequence strongly suggests the user was the victim of a targeted spear-phishing campaign that resulted in immediate payload detonation.</p>
                    </div>
                    <div className="flex gap-4 p-3 bg-violet-950/20 border border-violet-500/20 rounded">
                        <ExplanationBadge type="RECOMMENDATION" />
                        <p className="text-sm text-violet-300">You should immediately isolate the affected endpoint and reset the user's IAM credentials.</p>
                    </div>
                </div>
                
                <div className="mt-6 border-t border-slate-800 pt-4">
                    <SuggestedQuestions questions={[
                        "What happened next?", 
                        "Explain the registry modifications.", 
                        "Is there a related network beacon?"
                    ]} />
                </div>
            </CopilotMessage>
        </div>

        {/* Input Area */}
        <div className="p-4 bg-slate-900 border-t border-slate-800">
            <div className="flex items-center gap-2 bg-slate-950 border border-slate-800 rounded-lg p-2 focus-within:border-violet-500 focus-within:ring-1 focus-within:ring-violet-500/50 transition-all">
                <Button variant="ghost" size="icon" className="text-slate-500 hover:text-slate-300 shrink-0">
                    <Paperclip size={18} />
                </Button>
                <input 
                    type="text" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask about the timeline, explain an artifact, or generate a summary..." 
                    className="flex-1 bg-transparent border-none focus:outline-none text-sm px-2 text-slate-200 placeholder:text-slate-600"
                />
                <Button size="icon" className="bg-violet-600 hover:bg-violet-700 text-white shrink-0">
                    <Send size={16} />
                </Button>
            </div>
            <p className="text-[10px] text-center text-slate-600 mt-2">
                AI assessments may be inaccurate. Always verify findings against original evidentiary artifacts.
            </p>
        </div>
      </div>

      {/* Context Panel */}
      <div className="w-96 bg-slate-900 p-6 flex flex-col gap-6">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-2">Active Context</h2>
        
        <Card className="bg-slate-950 border-slate-800">
            <CardContent className="p-4">
                <h3 className="text-xs font-bold text-slate-400 mb-2">Referenced Evidence (2)</h3>
                <div className="space-y-2">
                    <div className="text-xs bg-slate-900 p-2 rounded border border-slate-800 flex justify-between">
                        <span className="text-slate-300 truncate">EV-982 (EMAIL)</span>
                        <a href="#" className="text-violet-400 hover:underline">View</a>
                    </div>
                    <div className="text-xs bg-slate-900 p-2 rounded border border-slate-800 flex justify-between">
                        <span className="text-slate-300 truncate">EV-983 (DISK)</span>
                        <a href="#" className="text-violet-400 hover:underline">View</a>
                    </div>
                </div>
            </CardContent>
        </Card>
      </div>
    </div>
  );
}

function UserMessage({ content }: any) {
    return (
        <div className="flex gap-4 flex-row-reverse">
            <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center shrink-0">
                <User size={16} className="text-slate-400" />
            </div>
            <div className="bg-slate-800 text-slate-200 p-3 rounded-lg rounded-tr-none text-sm max-w-[80%]">
                {content}
            </div>
        </div>
    );
}

function CopilotMessage({ children }: any) {
    return (
        <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-violet-600 flex items-center justify-center shrink-0 shadow-lg shadow-violet-500/20 mt-1">
                <Bot size={16} className="text-white" />
            </div>
            <div className="flex-1">
                {children}
            </div>
        </div>
    );
}
