import React from 'react';
import { MessageSquare, User, Search, Trash2 } from 'lucide-react';
import { Input } from '@/components/ui/input';

export default function ConversationViewer() {
  return (
    <div className="flex h-[calc(100vh-4rem)] bg-slate-950 text-slate-100 font-sans border-t border-slate-800">
        
        {/* Thread List Pane */}
        <div className="w-1/3 border-r border-slate-800 flex flex-col bg-slate-900/50">
            <div className="p-4 border-b border-slate-800">
                <div className="flex items-center gap-2 bg-slate-900 rounded border border-slate-700 px-3 py-1.5">
                    <Search size={16} className="text-slate-400" />
                    <Input className="border-none h-6 bg-transparent text-sm focus-visible:ring-0 placeholder:text-slate-600" placeholder="Search threads..." />
                </div>
            </div>
            <div className="flex-1 overflow-y-auto">
                <ThreadRow name="John Doe (Suspect)" preview="Yeah, wiped everything and cl..." app="iMessage" active />
                <ThreadRow name="+1 (555) 292-1044" preview="Your 2FA code is 884122" app="SMS" />
                <ThreadRow name="Boss" preview="Did you send the wire transfer?" app="WhatsApp" />
            </div>
        </div>

        {/* Conversation Pane */}
        <div className="w-2/3 flex flex-col bg-slate-950 relative">
            <div className="p-4 border-b border-slate-800 bg-slate-900 flex justify-between items-center z-10">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center">
                        <User size={20} className="text-slate-400" />
                    </div>
                    <div>
                        <h3 className="font-bold text-slate-200">John Doe (Suspect)</h3>
                        <p className="text-xs text-sky-400 font-mono">iMessage • +1 (555) 999-8888</p>
                    </div>
                </div>
            </div>
            
            <div className="flex-1 p-6 overflow-y-auto space-y-6">
                <MessageBubble 
                    text="Did you delete the server logs?" 
                    time="Jul 27, 2026 - 14:00" 
                    isOutgoing={true} 
                />
                <MessageBubble 
                    text="Yeah, wiped everything and cleared the bash history." 
                    time="Jul 27, 2026 - 14:05" 
                    isOutgoing={false} 
                    isDeleted={true}
                />
                
                <div className="text-center">
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
                        End of extracted thread
                    </span>
                </div>
            </div>
        </div>

    </div>
  );
}

function ThreadRow({ name, preview, app, active }: any) {
    return (
        <div className={`p-4 border-b border-slate-800/50 cursor-pointer transition-colors ${active ? 'bg-sky-950/20 border-l-4 border-l-sky-500' : 'hover:bg-slate-800/50 border-l-4 border-l-transparent'}`}>
            <div className="flex justify-between items-start mb-1">
                <h4 className={`font-bold text-sm ${active ? 'text-slate-200' : 'text-slate-300'}`}>{name}</h4>
                <span className="text-[10px] font-bold text-slate-500">{app}</span>
            </div>
            <p className="text-xs text-slate-400 truncate">{preview}</p>
        </div>
    );
}

function MessageBubble({ text, time, isOutgoing, isDeleted }: any) {
    return (
        <div className={`flex flex-col ${isOutgoing ? 'items-end' : 'items-start'}`}>
            <div className={`max-w-[70%] p-3 rounded-2xl ${isOutgoing ? 'bg-sky-600 text-white rounded-br-sm' : 'bg-slate-800 text-slate-200 rounded-bl-sm'} relative group`}>
                {text}
                {isDeleted && (
                    <div className="absolute -top-3 -right-2 bg-rose-950 border border-rose-500/50 text-rose-400 text-[9px] font-bold px-1.5 py-0.5 rounded flex items-center gap-1 shadow-lg">
                        <Trash2 size={10} /> RECOVERED
                    </div>
                )}
            </div>
            <span className="text-[10px] text-slate-500 mt-1 font-mono">{time}</span>
        </div>
    );
}
