import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckSquare, Plus, Clock } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function TaskBoard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="flex justify-between items-end border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <CheckSquare className="text-blue-500" />
                Response Action Plan
            </h1>
            <p className="text-slate-400 mt-1">Track containment and forensics tasks for INC-2026-084.</p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              <Plus size={16} className="mr-2" /> Add Task
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Column title="TODO" count={2}>
                <TaskCard title="Review firewall logs for exfiltration" assignee="Bob Smith" type="INVESTIGATION" />
                <TaskCard title="Draft external communication memo" assignee="Legal Team" type="DOCUMENTATION" />
            </Column>
            
            <Column title="IN PROGRESS" count={1}>
                <TaskCard title="Analyze memory dump from HR-05" assignee="Jane Doe" type="FORENSICS" active />
            </Column>
            
            <Column title="DONE" count={1}>
                <TaskCard title="Isolate affected HR endpoints" assignee="System Auto" type="CONTAINMENT" done />
            </Column>
        </div>
    </div>
  );
}

function Column({ title, count, children }: any) {
    return (
        <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800 flex flex-col h-[600px]">
            <div className="flex justify-between items-center mb-4 px-2">
                <h3 className="text-sm font-bold text-slate-300">{title}</h3>
                <Badge variant="secondary" className="bg-slate-800 text-slate-400">{count}</Badge>
            </div>
            <div className="space-y-4 overflow-y-auto">
                {children}
            </div>
        </div>
    );
}

function TaskCard({ title, assignee, type, active, done }: any) {
    return (
        <Card className={`bg-slate-900 border ${active ? 'border-blue-500/50 shadow-[0_0_10px_rgba(59,130,246,0.1)]' : 'border-slate-700'} hover:border-slate-500 transition-colors cursor-grab`}>
            <CardContent className="p-4 flex flex-col gap-3">
                <div className="flex justify-between items-start">
                    <Badge variant="outline" className="text-[10px] font-semibold bg-slate-950 border-slate-700 text-slate-400">
                        {type}
                    </Badge>
                </div>
                <p className={`text-sm font-medium ${done ? 'text-slate-500 line-through' : 'text-slate-200'}`}>
                    {title}
                </p>
                <div className="flex justify-between items-center mt-2 border-t border-slate-800 pt-3">
                    <span className="text-xs text-slate-500 flex items-center gap-1">
                        <Clock size={12} /> Due Today
                    </span>
                    <div className="w-6 h-6 rounded-full bg-slate-700 flex items-center justify-center text-[10px] font-bold text-slate-300" title={assignee}>
                        {assignee.charAt(0)}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
