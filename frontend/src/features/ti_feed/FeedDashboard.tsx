import React, { useState, useEffect } from 'react';

interface FeedAnalytics {
  total_feeds: number;
  active_feeds: number;
  total_indicators_ingested: number;
  sync_success_rate: number;
  recent_errors: number;
  feeds_by_format: Record<string, number>;
}

export const FeedDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<FeedAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/v1/ti-feed/analytics/summary');
        if (response.ok) {
          const data = await response.json();
          setAnalytics(data);
        }
      } catch (error) {
        console.error('Failed to fetch feed analytics', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-gray-400">Loading Intelligence Platform...</div>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white flex items-center">
          <svg className="w-8 h-8 mr-3 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          Threat Intelligence Feed Platform
        </h1>
        <p className="text-gray-400 mt-2">Enterprise-grade CTI ingestion, enrichment, and distribution.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {/* Metric Cards */}
        <div className="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm">Active Feeds</span>
          <span className="text-3xl font-bold text-white mt-2">{analytics?.active_feeds} / {analytics?.total_feeds}</span>
        </div>
        <div className="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm">Indicators Ingested</span>
          <span className="text-3xl font-bold text-blue-400 mt-2">{(analytics?.total_indicators_ingested || 0).toLocaleString()}</span>
        </div>
        <div className="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm">Sync Success Rate</span>
          <span className="text-3xl font-bold text-green-400 mt-2">{analytics?.sync_success_rate}%</span>
        </div>
        <div className="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm">Recent Errors</span>
          <span className={`text-3xl font-bold mt-2 ${(analytics?.recent_errors || 0) > 0 ? 'text-red-400' : 'text-gray-300'}`}>
            {analytics?.recent_errors}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
           <h3 className="text-lg font-semibold mb-4 text-white">Feeds by Format</h3>
           <div className="space-y-3">
             {Object.entries(analytics?.feeds_by_format || {}).map(([format, count]) => (
                <div key={format} className="flex justify-between items-center bg-gray-900 p-3 rounded border border-gray-750">
                  <span className="font-mono text-sm text-blue-300">{format}</span>
                  <span className="text-white font-medium">{count as React.ReactNode} Feeds</span>
                </div>
             ))}
           </div>
        </div>

        <div className="bg-gradient-to-br from-blue-900/50 to-indigo-900/50 p-6 rounded-xl border border-blue-800/50 flex flex-col justify-center items-center text-center">
            <svg className="w-16 h-16 text-blue-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <h3 className="text-xl font-bold text-white">AI Enrichment Active</h3>
            <p className="text-blue-200/70 mt-2 text-sm max-w-sm">
              All ingested indicators are automatically validated, normalized, and enriched via the IOC Correlation Engine and Enterprise Knowledge Graph.
            </p>
        </div>
      </div>
    </div>
  );
};
