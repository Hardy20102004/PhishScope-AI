import React from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Database, Search, Activity, FileText, UploadCloud, BookOpen } from 'lucide-react';
import { Link } from 'react-router-dom';

export const KnowledgeDashboard: React.FC = () => {
  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-blue-500" />
            Enterprise Knowledge Base
          </h1>
          <p className="text-gray-400 mt-2 max-w-3xl">
            RAG Platform overview: document ingestion, embedding status, and hybrid search performance.
          </p>
        </div>
        <div className="flex gap-3">
          <Link 
            to="/rag/search"
            className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors border border-gray-700"
          >
            <Search className="w-5 h-5" />
            Search Knowledge
          </Link>
          <Link 
            to="/rag/library"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors"
          >
            <UploadCloud className="w-5 h-5" />
            Manage Documents
          </Link>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-4 mb-10">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <FileText className="w-5 h-5 text-blue-400" />
              <p className="text-sm font-medium text-gray-400">Total Assets</p>
            </div>
            <h3 className="text-3xl font-bold text-white">1,248</h3>
            <p className="text-xs text-gray-500 mt-1">Active documents indexed</p>
          </CardContent>
        </Card>
        
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Database className="w-5 h-5 text-purple-400" />
              <p className="text-sm font-medium text-gray-400">Vector Chunks</p>
            </div>
            <h3 className="text-3xl font-bold text-white">14.2k</h3>
            <p className="text-xs text-gray-500 mt-1">Embeddings generated</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Search className="w-5 h-5 text-emerald-400" />
              <p className="text-sm font-medium text-gray-400">Cache Hit Rate</p>
            </div>
            <h3 className="text-3xl font-bold text-white">84.5%</h3>
            <p className="text-xs text-emerald-500 mt-1">Queries served from cache</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-5 h-5 text-orange-400" />
              <p className="text-sm font-medium text-gray-400">Search Latency</p>
            </div>
            <h3 className="text-3xl font-bold text-white">120ms</h3>
            <p className="text-xs text-orange-500 mt-1">P95 Hybrid Retrieval</p>
          </CardContent>
        </Card>
      </div>
      
      <div className="mt-8">
        <h2 className="text-xl font-bold text-white mb-4">Ingestion Queue</h2>
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center justify-center h-32 text-gray-500">
              No documents currently processing.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
