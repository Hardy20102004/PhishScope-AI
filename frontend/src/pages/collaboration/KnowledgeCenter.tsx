import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { BookOpen, Search, Pin, FileText } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function KnowledgeCenter() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="flex justify-between items-end border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3 text-slate-200">
                <BookOpen className="text-blue-500" />
                Knowledge Center
            </h1>
            <p className="text-slate-400 mt-1">Shared analyst notes, playbooks, and pinned investigation templates.</p>
          </div>
          <div className="w-72">
              <div className="relative">
                  <Search size={16} className="absolute left-3 top-2.5 text-slate-500" />
                  <Input className="pl-9 bg-slate-900 border-slate-700 text-slate-200" placeholder="Search knowledge base..." />
              </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <NoteCard 
                title="SOP: Handling Suspected Data Exfiltration"
                author="Jane Doe"
                date="2 days ago"
                tags={["SOP", "Exfiltration", "Network"]}
                pinned
            />
            <NoteCard 
                title="Hunt Notes: APT29 Lateral Movement Patterns"
                author="Alice Wang"
                date="5 days ago"
                tags={["Hunt", "APT29", "Windows Event Logs"]}
            />
            <NoteCard 
                title="Cheatsheet: Velociraptor VQL Queries"
                author="Bob Smith"
                date="1 week ago"
                tags={["DFIR", "Velociraptor", "Cheatsheet"]}
            />
            <NoteCard 
                title="Incident Summary: INC-2026-084"
                author="AI Assistant"
                date="Today"
                tags={["Summary", "Ransomware"]}
            />
        </div>
    </div>
  );
}

function NoteCard({ title, author, date, tags, pinned = false }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-slate-600 transition-colors cursor-pointer flex flex-col h-48">
            <CardHeader className="pb-2 flex-row justify-between items-start space-y-0">
                <CardTitle className="text-md text-slate-200 leading-tight">{title}</CardTitle>
                {pinned && <Pin size={16} className="text-blue-400 flex-shrink-0" />}
            </CardHeader>
            <CardContent className="flex-1 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-xs text-slate-500 mb-4">
                    <FileText size={12} />
                    <span>Created by {author} • {date}</span>
                </div>
                <div className="flex flex-wrap gap-2">
                    {tags.map((tag: string) => (
                        <Badge key={tag} variant="secondary" className="bg-slate-950 text-slate-400 border-slate-800 text-[10px]">
                            {tag}
                        </Badge>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
