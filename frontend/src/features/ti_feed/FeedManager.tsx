import React, { useState, useEffect } from 'react';

interface Feed {
  id: string;
  name: string;
  format: string;
  source_uri: string;
  status: string;
  last_sync_at: string | null;
  sync_interval_minutes: number;
}

export const FeedManager: React.FC = () => {
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFeeds = async () => {
    try {
      const response = await fetch('/api/v1/ti-feed/registry');
      if (response.ok) {
        const data = await response.json();
        setFeeds(data);
      }
    } catch (error) {
      console.error('Error fetching feeds', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeeds();
  }, []);

  const handleSync = async (feedId: string) => {
    try {
      await fetch(`/api/v1/ti-feed/${feedId}/sync`, { method: 'POST' });
      alert('Sync triggered successfully! Check Sync Monitor.');
      fetchFeeds();
    } catch (error) {
      console.error('Error triggering sync', error);
      alert('Failed to trigger sync.');
    }
  };

  if (loading) return <div className="p-4 text-gray-400">Loading Feeds...</div>;

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg overflow-hidden">
      <div className="p-6 border-b border-gray-700 flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-white">Feed Registry</h2>
          <p className="text-sm text-gray-400 mt-1">Manage threat intelligence sources and connectors.</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          + Add New Feed
        </button>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-gray-300">
          <thead className="bg-gray-800 text-gray-400 uppercase font-medium">
            <tr>
              <th className="px-6 py-4">Name</th>
              <th className="px-6 py-4">Format</th>
              <th className="px-6 py-4">Source</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Last Sync</th>
              <th className="px-6 py-4">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700/50">
            {feeds.map((feed) => (
              <tr key={feed.id} className="hover:bg-gray-800/50 transition-colors">
                <td className="px-6 py-4 font-medium text-white">{feed.name}</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 bg-gray-700 text-xs rounded font-mono">{feed.format}</span>
                </td>
                <td className="px-6 py-4 truncate max-w-xs" title={feed.source_uri}>
                  {feed.source_uri}
                </td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 text-xs rounded-full flex inline-flex items-center
                    ${feed.status === 'Active' ? 'bg-green-500/10 text-green-400' : 
                      feed.status === 'Error' ? 'bg-red-500/10 text-red-400' : 
                      'bg-gray-500/10 text-gray-400'}`}>
                    <span className={`w-1.5 h-1.5 rounded-full mr-1.5 
                      ${feed.status === 'Active' ? 'bg-green-400' : 
                        feed.status === 'Error' ? 'bg-red-400' : 'bg-gray-400'}`}></span>
                    {feed.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-gray-400">
                  {feed.last_sync_at ? new Date(feed.last_sync_at).toLocaleString() : 'Never'}
                </td>
                <td className="px-6 py-4">
                  <div className="flex space-x-3">
                    <button 
                      onClick={() => handleSync(feed.id)}
                      className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
                    >
                      Sync Now
                    </button>
                    <button className="text-gray-400 hover:text-white transition-colors">
                      Edit
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            
            {feeds.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                  No feeds registered. Click "Add New Feed" to connect to a CTI source.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
