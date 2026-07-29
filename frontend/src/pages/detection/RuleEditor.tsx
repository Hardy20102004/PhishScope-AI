import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BrainCircuit, Check, GitCommit, FileCode, Play } from 'lucide-react';
import { Textarea } from '@/components/ui/textarea';

export default function RuleEditor() {
  const navigate = useNavigate();
  const [rule, setRule] = useState({
    name: '', description: '', rule_type: 'SIGMA', severity: 'MEDIUM', payload: ''
  });
  const [aiSuggestions, setAiSuggestions] = useState<any>(null);

  const handleSave = async () => {
    try {
      const res = await apiClient.post('/detection', rule);
      navigate('/detection/rules');
    } catch (err) {
      console.error(err);
      alert('Failed to save rule. Syntax might be invalid.');
    }
  };

  const handleAiSuggest = async () => {
    try {
      const res = await apiClient.post('/detection/ai/suggest', { payload: rule.payload });
      setAiSuggestions(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-8 flex flex-col lg:flex-row gap-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
      {/* Editor Main */}
      <div className="flex-1 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <FileCode className="text-emerald-500" />
            Detection Rule Editor
          </h1>
          <div className="flex gap-2">
             <Button variant="outline" className="border-slate-700 hover:bg-slate-800 text-slate-300">Cancel</Button>
             <Button onClick={handleSave} className="bg-emerald-600 hover:bg-emerald-700 text-white">Save Draft</Button>
          </div>
        </div>

        <Card className="bg-slate-900 border-slate-800 shadow-xl">
           <CardContent className="p-6 space-y-4">
             <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-slate-400 mb-1 block">Rule Name</label>
                  <Input className="bg-slate-950 border-slate-800" value={rule.name} onChange={e => setRule({...rule, name: e.target.value})} placeholder="e.g. Suspicious PowerShell Download" />
                </div>
                <div>
                  <label className="text-sm text-slate-400 mb-1 block">Severity</label>
                  <select className="w-full bg-slate-950 border border-slate-800 rounded-md p-2 text-sm focus:border-emerald-500" value={rule.severity} onChange={e => setRule({...rule, severity: e.target.value})}>
                    <option value="LOW">Low</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="HIGH">High</option>
                    <option value="CRITICAL">Critical</option>
                  </select>
                </div>
             </div>
             <div>
                <label className="text-sm text-slate-400 mb-1 block">Description</label>
                <Input className="bg-slate-950 border-slate-800" value={rule.description} onChange={e => setRule({...rule, description: e.target.value})} placeholder="Detects..." />
             </div>
           </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800 shadow-xl flex-1 flex flex-col">
          <Tabs defaultValue="code" className="w-full h-full flex flex-col">
            <CardHeader className="pb-0 border-b border-slate-800 flex flex-row items-center justify-between">
              <TabsList className="bg-slate-950 border border-slate-800">
                <TabsTrigger value="code">Raw Editor</TabsTrigger>
                <TabsTrigger value="visual">Visual Builder</TabsTrigger>
              </TabsList>
              <Button onClick={handleAiSuggest} variant="ghost" className="text-indigo-400 hover:bg-indigo-950">
                <BrainCircuit size={16} className="mr-2" />
                Ask AI Assistant
              </Button>
            </CardHeader>
            <CardContent className="p-0 flex-1 relative min-h-[400px]">
              <TabsContent value="code" className="h-full m-0">
                <Textarea 
                  className="w-full h-full min-h-[400px] bg-[#0d1117] text-[#c9d1d9] font-mono p-4 border-0 rounded-none focus-visible:ring-0 resize-none"
                  value={rule.payload}
                  onChange={e => setRule({...rule, payload: e.target.value})}
                  placeholder="Paste YAML or YARA logic here..."
                />
              </TabsContent>
              <TabsContent value="visual" className="h-full m-0 p-6 flex items-center justify-center text-slate-500">
                Visual node builder not available for this rule type.
              </TabsContent>
            </CardContent>
          </Tabs>
        </Card>
      </div>

      {/* Right Sidebar - Context & Actions */}
      <div className="w-full lg:w-80 space-y-6">
        <Card className="bg-indigo-950/20 border-indigo-500/20 shadow-xl">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2 text-indigo-400">
              <BrainCircuit size={16} />
              AI Context Assistant
            </CardTitle>
          </CardHeader>
          <CardContent>
            {aiSuggestions ? (
              <div className="space-y-4">
                <p className="text-xs text-slate-300">{aiSuggestions.explanation}</p>
                <div>
                  <span className="text-xs font-semibold text-slate-400">Suggested Techniques:</span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {aiSuggestions.suggested_techniques.map((t: string) => (
                      <span key={t} className="px-2 py-1 bg-indigo-500/20 text-indigo-300 rounded text-xs border border-indigo-500/30">{t}</span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">Click 'Ask AI Assistant' to generate mapping suggestions and rule explanations.</p>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm text-slate-300">Rule Lifecycle</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
             <Button className="w-full justify-start bg-slate-800 hover:bg-slate-700 text-slate-300">
               <Play size={14} className="mr-2 text-cyan-400" />
               Run Regression Tests
             </Button>
             <Button className="w-full justify-start bg-slate-800 hover:bg-slate-700 text-slate-300">
               <GitCommit size={14} className="mr-2 text-emerald-400" />
               Submit for Approval
             </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
