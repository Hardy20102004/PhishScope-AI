import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Building2, Terminal } from 'lucide-react';

interface NarrativeViewerProps {
  executive: string;
  technical: string;
}

export const NarrativeViewer: React.FC<NarrativeViewerProps> = ({ executive, technical }) => {
  const [activeTab, setActiveTab] = useState<'exec' | 'tech'>('exec');

  return (
    <Card className="bg-gray-900 border-gray-800 h-full">
      <CardContent className="p-0 flex flex-col h-full">
        <div className="flex border-b border-gray-800">
          <button 
            className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-colors ${activeTab === 'exec' ? 'text-yellow-400 border-b-2 border-yellow-500 bg-gray-800/50' : 'text-gray-400 hover:text-gray-300'}`}
            onClick={() => setActiveTab('exec')}
          >
            <Building2 className="w-4 h-4" /> Executive Summary
          </button>
          <button 
            className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-colors ${activeTab === 'tech' ? 'text-cyan-400 border-b-2 border-cyan-500 bg-gray-800/50' : 'text-gray-400 hover:text-gray-300'}`}
            onClick={() => setActiveTab('tech')}
          >
            <Terminal className="w-4 h-4" /> Technical Deep Dive
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto flex-1">
          {activeTab === 'exec' ? (
            <div className="prose prose-invert max-w-none">
              {executive.split('\n').map((line: string, i: number) => (
                <p key={i} className="text-gray-300 leading-relaxed mb-2">{line}</p>
              ))}
            </div>
          ) : (
            <div className="prose prose-invert max-w-none font-mono text-sm bg-black/50 p-4 rounded-lg border border-gray-800">
              {technical.split('\n').map((line: string, i: number) => (
                <p key={i} className={`${line.startsWith('-') ? 'ml-4 text-cyan-300' : 'text-gray-300'} mb-1`}>{line}</p>
              ))}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
