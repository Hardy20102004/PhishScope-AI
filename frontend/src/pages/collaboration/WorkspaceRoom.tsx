import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Hash, Search, Paperclip, Send, Bot, ShieldAlert } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function WorkspaceRoom() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      
      {/* Left Sidebar - Channels */}
      <div className="w-64 border-r border-slate-800 bg-slate-900 flex flex-col">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center">
              <h2 className="text-sm font-bold text-slate-200">Workspaces</h2>
              <Search size={16} className="text-slate-500" />
          </div>
          <div className="p-2 space-y-1 flex-1 overflow-y-auto">
              <ChannelItem name="inc-2026-084-ransomware" active />
              <ChannelItem name="hunt-apt29-lateral" />
              <ChannelItem name="intel-sharing-global" />
              <ChannelItem name="soc-general" />
          </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
          {/* Header */}
          <div className="h-16 border-b border-slate-800 flex justify-between items-center px-6 bg-slate-900/50">
              <div>
                  <h1 className="text-lg font-bold text-slate-200 flex items-center gap-2">
                      <Hash size={18} className="text-slate-500" />
                      inc-2026-084-ransomware
                  </h1>
                  <p className="text-xs text-slate-500">Incident Collaboration Room • 5 Members</p>
              </div>
              <div className="flex gap-2">
                  <Button variant="outline" className="bg-slate-900 border-indigo-500/50 text-indigo-400 h-8 text-xs hover:bg-indigo-950/30">
                      <Bot size={14} className="mr-2" /> Summarize Thread
                  </Button>
              </div>
          </div>
          
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
              <Message 
                  author="Jane Doe" 
                  time="10:15 AM" 
                  content="I've attached the memory dump from HR-05 to the Evidence Locker. Analyzing with Volatility now." 
              />
              <SystemMessage 
                  time="10:22 AM" 
                  content="SOAR Playbook 'Ransomware Containment' executed action: Isolate Host (HR-05)." 
              />
              <Message 
                  author="Bob Smith" 
                  time="10:25 AM" 
                  content="Nice, we caught it early. Has anyone checked the firewall logs for exfiltration?" 
              />
              
              <div className="relative my-8">
                  <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-800"></div></div>
                  <div className="relative flex justify-center"><span className="bg-slate-950 px-2 text-xs text-slate-500">Unread Messages</span></div>
              </div>

              <Message 
                  author="Jane Doe" 
                  time="10:30 AM" 
                  content="@Bob Yes, I just ran a query in the Hunting Workspace. No anomalous outbound transfers > 10MB to external IPs." 
                  mention
              />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-slate-800 bg-slate-900/50">
              <div className="flex items-center gap-2 bg-slate-950 p-2 rounded-lg border border-slate-700">
                  <Button variant="ghost" size="icon" className="text-slate-400 hover:text-slate-200"><Paperclip size={18} /></Button>
                  <Input 
                      className="flex-1 bg-transparent border-none focus-visible:ring-0 text-slate-200 placeholder:text-slate-600" 
                      placeholder="Message #inc-2026-084-ransomware..."
                  />
                  <Button size="icon" className="bg-purple-600 hover:bg-purple-700 text-white rounded-md"><Send size={16} /></Button>
              </div>
          </div>
      </div>
      
      {/* Right Sidebar - Thread/Context */}
      <div className="w-80 border-l border-slate-800 bg-slate-900 flex flex-col hidden lg:flex">
          <div className="p-4 border-b border-slate-800">
              <h2 className="text-sm font-bold text-slate-200">Incident Context</h2>
          </div>
          <div className="p-4 space-y-6">
              <div>
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Linked Entities</h3>
                  <div className="flex items-center gap-3 p-2 bg-slate-950 rounded border border-slate-800">
                      <ShieldAlert size={16} className="text-rose-500" />
                      <div>
                          <p className="text-xs font-bold text-slate-200">INC-2026-084</p>
                          <p className="text-[10px] text-slate-500">Status: CONTAINMENT</p>
                      </div>
                  </div>
              </div>
              
              <div>
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">AI Thread Summary</h3>
                  <div className="bg-indigo-950/20 p-3 rounded border border-indigo-500/20 text-sm text-slate-300 leading-relaxed">
                      Jane Doe collected memory evidence. SOAR isolated the host. Bob and Jane verified no data exfiltration occurred via firewall logs.
                  </div>
              </div>
          </div>
      </div>
    </div>
  );
}

function ChannelItem({ name, active }: any) {
    return (
        <div className={`flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer transition-colors ${active ? 'bg-purple-500/20 text-purple-400 font-semibold' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'}`}>
            <Hash size={16} />
            <span className="text-sm truncate">{name}</span>
        </div>
    );
}

function Message({ author, time, content, mention }: any) {
    return (
        <div className={`flex gap-4 p-2 rounded-lg transition-colors hover:bg-slate-900 ${mention ? 'bg-purple-500/10 border-l-2 border-purple-500' : ''}`}>
            <div className="w-10 h-10 rounded-lg bg-slate-800 flex-shrink-0 flex items-center justify-center font-bold text-slate-300">
                {author.charAt(0)}
            </div>
            <div>
                <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold text-slate-200 text-sm">{author}</span>
                    <span className="text-xs text-slate-500">{time}</span>
                </div>
                <p className="text-sm text-slate-300 leading-relaxed">
                    {content.split(' ').map((word: string, i: number) => 
                        word.startsWith('@') ? <span key={i} className="text-purple-400 font-semibold bg-purple-500/10 px-1 rounded">{word} </span> : word + ' '
                    )}
                </p>
            </div>
        </div>
    );
}

function SystemMessage({ time, content }: any) {
    return (
        <div className="flex items-center gap-4 px-2 py-1">
            <div className="w-10 flex justify-center text-slate-600"><Bot size={16} /></div>
            <div className="text-xs text-slate-500 italic">
                <span className="font-mono mr-2">{time}</span>
                {content}
            </div>
        </div>
    );
}
