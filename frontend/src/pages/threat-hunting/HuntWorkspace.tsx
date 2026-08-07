import React, { useState } from 'react';
import apiClient from '@/api/client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { BrainCircuit, Search, Database, Network, Crosshair, ChevronRight } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';

export default function HuntWorkspace() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [hypotheses, setHypotheses] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  
  // Mock Session ID for demo
  const sessionId = "12345678-1234-1234-1234-123456789012";

  const handleSearch = async () => {
      if (!query) return;
      setIsSearching(true);
      try {
          // In a real app we'd create a session first if it doesn't exist.
          // We mock the API call for execution.
          const res = await apiClient.post(`/threat-hunting/sessions/${sessionId}/query`, { raw_query: query });
          
          // Mocking the returned UI data since the backend only returns the audit record currently
          setResults([
              { id: 1, type: 'PROCESS', artifact: 'powershell.exe -enc JAB...', host: 'DC-01', time: '10 mins ago' },
              { id: 2, type: 'NETWORK', artifact: '10.0.0.5:445 -> 10.0.0.8:445', host: 'DC-01', time: '12 mins ago' },
          ]);
      } catch (err) {
          console.error(err);
      } finally {
          setIsSearching(false);
      }
  };

  const generateHypothesis = async () => {
      try {
          const res = await apiClient.post(`/threat-hunting/sessions/${sessionId}/hypothesize`);
          setHypotheses(res.data);
      } catch (err) {
          console.error(err);
      }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      
      {/* Main Workspace */}
      <div className="flex-1 flex flex-col p-6 space-y-4 border-r border-slate-800">
          <div className="flex justify-between items-center pb-2 border-b border-slate-800">
              <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                  <Crosshair className="text-red-500" />
                  Operation Night Owl (Active)
              </h1>
          </div>

          {/* Search Bar */}
          <div className="flex gap-2">
              <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 text-slate-500" size={18} />
                  <Input 
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      placeholder="Natural Language Search (e.g., 'Show me anomalous PowerShell on Domain Controllers')" 
                      className="w-full pl-10 bg-slate-900 border-slate-700 focus:border-red-500 h-12 text-md"
                      onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                  />
              </div>
              <Button onClick={handleSearch} disabled={isSearching} className="h-12 px-6 bg-red-600 hover:bg-red-700 text-white">
                  {isSearching ? 'Querying...' : 'Hunt'}
              </Button>
          </div>

          {/* Results Area */}
          <Card className="flex-1 bg-slate-900 border-slate-800 flex flex-col overflow-hidden">
              <CardHeader className="py-3 px-4 border-b border-slate-800 bg-slate-950/50 flex flex-row items-center justify-between">
                  <CardTitle className="text-sm text-slate-300 flex items-center gap-2">
                      <Database size={16} /> Evidence & Correlated Artifacts
                  </CardTitle>
                  <Button variant="ghost" size="sm" className="h-8 text-slate-400 hover:text-slate-200">
                      <Network size={14} className="mr-2" /> View in Knowledge Graph
                  </Button>
              </CardHeader>
              <CardContent className="p-0 flex-1 overflow-auto">
                  {results.length === 0 ? (
                      <div className="flex items-center justify-center h-full text-slate-500 text-sm">
                          Enter a query to start hunting.
                      </div>
                  ) : (
                      <div className="divide-y divide-slate-800/50">
                          {results.map((r, i) => (
                              <div key={i} className="p-4 hover:bg-slate-800/30 transition-colors flex items-center justify-between">
                                  <div className="flex items-center gap-4">
                                      <Badge variant="outline" className="bg-slate-800 text-slate-300 border-slate-700 w-20 justify-center">
                                          {r.type}
                                      </Badge>
                                      <code className="text-sm text-red-400 bg-red-500/10 px-2 py-1 rounded font-mono">
                                          {r.artifact}
                                      </code>
                                  </div>
                                  <div className="flex items-center gap-4 text-sm text-slate-500">
                                      <span>{r.host}</span>
                                      <span>{r.time}</span>
                                      <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-red-400">
                                          <ChevronRight size={16} />
                                      </Button>
                                  </div>
                              </div>
                          ))}
                      </div>
                  )}
              </CardContent>
          </Card>
      </div>

      {/* Right Sidebar - AI Hypotheses */}
      <div className="w-96 bg-slate-950 p-6 flex flex-col space-y-4">
          <Button onClick={generateHypothesis} className="w-full bg-amber-500/20 text-amber-400 hover:bg-amber-500/30 border border-amber-500/30">
              <BrainCircuit size={16} className="mr-2" />
              Generate AI Hypotheses
          </Button>

          <ScrollArea className="flex-1">
              <div className="space-y-4 pr-4">
                  {hypotheses.length === 0 ? (
                      <p className="text-sm text-slate-500 italic text-center mt-10">
                          No hypotheses generated yet. Add evidence to your hunt and click generate.
                      </p>
                  ) : (
                      hypotheses.map((h, i) => (
                          <Card key={i} className="bg-slate-900 border-slate-800 shadow-xl">
                              <CardHeader className="p-4 pb-2">
                                  <div className="flex justify-between items-start mb-2">
                                      <Badge className="bg-amber-500/20 text-amber-400 border-0">
                                          Confidence: {h.confidence_score * 100}%
                                      </Badge>
                                  </div>
                                  <CardDescription className="text-slate-300 text-sm leading-relaxed">
                                      {h.hypothesis_text}
                                  </CardDescription>
                              </CardHeader>
                              <CardContent className="p-4 pt-2">
                                  <div className="mt-2">
                                      <p className="text-xs font-semibold text-slate-500 mb-2">Suggested Follow-up Queries:</p>
                                      <ul className="space-y-2">
                                          {h.suggested_queries.map((sq: string, j: number) => (
                                              <li key={j} className="text-xs bg-slate-950 p-2 rounded border border-slate-800 text-slate-400 cursor-pointer hover:border-red-500/50 hover:text-red-400 transition-colors" onClick={() => setQuery(sq)}>
                                                  <Search size={10} className="inline mr-2" />
                                                  {sq}
                                              </li>
                                          ))}
                                      </ul>
                                  </div>
                              </CardContent>
                          </Card>
                      ))
                  )}
              </div>
          </ScrollArea>
      </div>

    </div>
  );
}
