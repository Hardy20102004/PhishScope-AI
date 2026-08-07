import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { BrainCircuit, Send, Paperclip, Mic, User } from 'lucide-react';
import ContextPanel from './ContextPanel';
import SuggestedPrompts from './SuggestedPrompts';

export default function CopilotWorkspace() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative border-r border-slate-800">
          {/* Header */}
          <div className="h-16 border-b border-slate-800 flex justify-between items-center px-6 bg-slate-900/50">
              <div className="flex items-center gap-3">
                  <BrainCircuit size={24} className="text-cyan-500" />
                  <div>
                      <h1 className="text-lg font-bold text-slate-200">PHOENIX X Copilot</h1>
                      <p className="text-xs text-slate-500">Enterprise AI Security Assistant</p>
                  </div>
              </div>
              <Button variant="outline" className="bg-slate-900 border-slate-700 h-8 text-xs hover:bg-slate-800">
                  New Session
              </Button>
          </div>
          
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-8 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-opacity-5">
              
              <div className="flex flex-col items-center justify-center h-48 space-y-4 opacity-50">
                  <BrainCircuit size={64} className="text-cyan-500" />
                  <p className="text-sm font-medium text-slate-400">How can I assist your investigation today?</p>
              </div>

              <UserMessage content="Can you summarize the recent lateral movement alerts originating from HR-05?" />
              <AIMessage content="Certainly. I analyzed the alerts from HR-05 over the last 24 hours. The host engaged in anomalous SMB enumeration across the Finance subnet, triggering 4 High-Severity detections. Based on the MITRE ATT&CK knowledge graph, this activity strongly correlates with APT29 lateral movement techniques." />
              
              <div className="mx-12">
                  <SuggestedPrompts />
              </div>
          </div>

          {/* Input Area */}
          <div className="p-6 bg-gradient-to-t from-slate-950 to-transparent">
              <div className="flex items-center gap-2 bg-slate-900 p-3 rounded-xl border border-slate-700 shadow-2xl shadow-cyan-500/5">
                  <Button variant="ghost" size="icon" className="text-slate-400 hover:text-slate-200"><Paperclip size={20} /></Button>
                  <Input 
                      className="flex-1 bg-transparent border-none focus-visible:ring-0 text-slate-200 placeholder:text-slate-500 text-base" 
                      placeholder="Ask Copilot to analyze alerts, generate reports, or hunt threats..."
                  />
                  <Button variant="ghost" size="icon" className="text-slate-400 hover:text-slate-200"><Mic size={20} /></Button>
                  <Button size="icon" className="bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg"><Send size={18} /></Button>
              </div>
          </div>
      </div>
      
      {/* Right Sidebar - Context & Evidence */}
      <ContextPanel />
    </div>
  );
}

function UserMessage({ content }: { content: string }) {
    return (
        <div className="flex gap-4 p-4 rounded-xl bg-slate-900 border border-slate-800 ml-12">
            <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex-shrink-0 flex items-center justify-center text-slate-400">
                <User size={18} />
            </div>
            <div className="pt-2 text-slate-200 leading-relaxed text-sm">
                {content}
            </div>
        </div>
    );
}

function AIMessage({ content }: { content: string }) {
    return (
        <div className="flex gap-4 p-4 mr-12">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex-shrink-0 flex items-center justify-center text-white shadow-lg shadow-cyan-500/20">
                <BrainCircuit size={20} />
            </div>
            <div className="pt-2 text-slate-300 leading-relaxed text-sm space-y-4">
                <p>{content}</p>
                <div className="flex gap-2">
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-slate-900 border border-slate-800 text-[10px] text-slate-400 font-mono">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500"></div> Evidence Linked
                    </span>
                </div>
            </div>
        </div>
    );
}
