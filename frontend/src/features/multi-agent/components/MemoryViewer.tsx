import React, { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';
import { Database, Search, DatabaseZap, Clock } from 'lucide-react';


export const MemoryViewer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Placeholder data for demonstration since memory API isn't fully scaffolded in this phase
  const memoryItems = [
    { id: '1', tier: 'WORKING', key: 'investigation:INV-482:entities', size: '2.4KB', lastAccessed: '2 mins ago', expires: '24h' },
    { id: '2', tier: 'EVIDENCE', key: 'case:CAS-901:pcap_hashes', size: '14.1MB', lastAccessed: '1 hour ago', expires: 'Never' },
    { id: '3', tier: 'CONVERSATION', key: 'session:msg_thread_99', size: '4.8KB', lastAccessed: 'Just now', expires: '7d' },
    { id: '4', tier: 'ORGANIZATION', key: 'tenant:patterns:phishing', size: '1.2MB', lastAccessed: '5 hours ago', expires: 'Never' }
  ];

  const getTierColor = (tier: string) => {
    switch(tier) {
      case 'WORKING': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'EVIDENCE': return 'text-red-400 bg-red-400/10 border-red-400/20';
      case 'CONVERSATION': return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
      case 'ORGANIZATION': return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      default: return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Database className="w-6 h-6 text-emerald-400" />
            Shared Memory & Context
          </h2>
          <p className="text-gray-400 text-sm mt-1">Explore the distributed context layer used by the agent workforce.</p>
        </div>
      </div>

      <Card className="bg-gray-800 border-gray-700">
        <CardHeader className="border-b border-gray-700 pb-4">
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="w-5 h-5 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input 
                type="text" 
                placeholder="Search memory keys or content..." 
                className="w-full bg-gray-900 border border-gray-700 rounded-md pl-10 pr-4 py-2 text-white focus:outline-none focus:border-emerald-500 transition-colors"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <button className="px-4 py-2 bg-gray-900 border border-gray-700 hover:bg-gray-700 text-white rounded-md transition-colors flex items-center gap-2">
              <DatabaseZap className="w-4 h-4 text-orange-400" /> Garbage Collect
            </button>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-gray-700 bg-gray-900/50">
                <th className="px-6 py-4 text-sm font-semibold text-gray-300">Key</th>
                <th className="px-6 py-4 text-sm font-semibold text-gray-300">Tier</th>
                <th className="px-6 py-4 text-sm font-semibold text-gray-300">Size</th>
                <th className="px-6 py-4 text-sm font-semibold text-gray-300">Last Accessed</th>
                <th className="px-6 py-4 text-sm font-semibold text-gray-300">TTL</th>
                <th className="px-6 py-4 text-sm font-semibold text-gray-300 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700/50">
              {memoryItems.filter(item => item.key.includes(searchTerm)).map((item) => (
                <tr key={item.id} className="hover:bg-gray-700/20 transition-colors">
                  <td className="px-6 py-4">
                    <span className="font-mono text-sm text-gray-200">{item.key}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getTierColor(item.tier)}`}>
                      {item.tier}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-400">{item.size}</td>
                  <td className="px-6 py-4 text-sm text-gray-400 flex items-center gap-1">
                    <Clock className="w-3 h-3" /> {item.lastAccessed}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-400">{item.expires}</td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-sm text-emerald-400 hover:text-emerald-300 mr-3">View</button>
                    <button className="text-sm text-red-400 hover:text-red-300">Evict</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
};
