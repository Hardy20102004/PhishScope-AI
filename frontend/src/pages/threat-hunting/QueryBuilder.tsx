import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Filter, Plus } from 'lucide-react';

export default function QueryBuilder() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
              <Filter className="text-blue-500" />
              Structured Query Builder
          </h1>
          <p className="text-slate-400 mt-1">Build advanced Boolean queries across specific indices.</p>
        </div>

        <Card className="bg-slate-900 border-slate-800">
            <CardHeader>
                <CardTitle className="text-slate-300 text-sm">Query Parameters</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex gap-4 items-center">
                    <select className="bg-slate-950 border border-slate-800 rounded p-2 text-sm text-slate-300 w-48">
                        <option>Index: EDR Events</option>
                        <option>Index: Network Flow</option>
                        <option>Index: Cloud Trail</option>
                    </select>
                    <span className="text-slate-500 text-sm">WHERE</span>
                    <select className="bg-slate-950 border border-slate-800 rounded p-2 text-sm text-slate-300 w-48">
                        <option>Process.Name</option>
                        <option>Process.CommandLine</option>
                        <option>Network.DestinationIP</option>
                    </select>
                    <select className="bg-slate-950 border border-slate-800 rounded p-2 text-sm text-slate-300 w-32">
                        <option>EQUALS</option>
                        <option>CONTAINS</option>
                        <option>MATCHES_REGEX</option>
                    </select>
                    <Input className="bg-slate-950 border-slate-800 flex-1" placeholder="e.g. powershell.exe" />
                </div>
                
                <div className="flex gap-2">
                    <Button variant="outline" className="bg-slate-900 border-slate-700 text-slate-300 text-xs">
                        <Plus size={12} className="mr-1" /> Add AND Condition
                    </Button>
                    <Button variant="outline" className="bg-slate-900 border-slate-700 text-slate-300 text-xs">
                        <Plus size={12} className="mr-1" /> Add OR Condition
                    </Button>
                </div>
            </CardContent>
        </Card>

        <div className="flex justify-end">
             <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8">
                 <Search size={16} className="mr-2" />
                 Execute Structured Query
             </Button>
        </div>
    </div>
  );
}
