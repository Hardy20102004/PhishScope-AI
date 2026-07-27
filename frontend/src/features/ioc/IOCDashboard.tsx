import React, { useState, useEffect } from 'react';

interface AnalyticsData {
  total_indicators: number;
  total_relationships: number;
  average_confidence: number;
  top_ioc_types: Record<string, number>;
}

export const IOCDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // In a real app, this would use a proper API client
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/v1/ioc/analytics/summary');
        if (response.ok) {
          const data = await response.json();
          setAnalytics(data);
        }
      } catch (error) {
        console.error('Failed to fetch analytics', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="flex h-full items-center justify-center text-gray-400">Loading IOC Engine Data...</div>;
  }

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
          Enterprise IOC Correlation Engine
        </h1>
        <p className="text-gray-400 mt-2 text-sm">
          Real-time threat intelligence discovery and relationship mapping.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Metric Cards */}
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg relative overflow-hidden group">
          <div className="absolute inset-0 bg-blue-500 opacity-0 group-hover:opacity-5 transition-opacity duration-300"></div>
          <h3 className="text-gray-400 text-sm font-medium">Total Indicators</h3>
          <p className="text-4xl font-bold text-white mt-2">{analytics?.total_indicators ?? 0}</p>
        </div>

        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg relative overflow-hidden group">
          <div className="absolute inset-0 bg-purple-500 opacity-0 group-hover:opacity-5 transition-opacity duration-300"></div>
          <h3 className="text-gray-400 text-sm font-medium">Discovered Relationships</h3>
          <p className="text-4xl font-bold text-white mt-2">{analytics?.total_relationships ?? 0}</p>
        </div>

        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg relative overflow-hidden group">
          <div className="absolute inset-0 bg-green-500 opacity-0 group-hover:opacity-5 transition-opacity duration-300"></div>
          <h3 className="text-gray-400 text-sm font-medium">Average Confidence</h3>
          <p className="text-4xl font-bold text-white mt-2">
            {((analytics?.average_confidence ?? 0) * 100).toFixed(1)}%
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
          <h3 className="text-lg font-semibold text-white mb-4">Top IOC Types</h3>
          <div className="space-y-4">
            {Object.entries(analytics?.top_ioc_types || {}).map(([type, count]) => (
              <div key={type} className="flex items-center">
                <div className="w-32 text-sm text-gray-400 truncate">{type}</div>
                <div className="flex-1 ml-4">
                  <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-500 to-indigo-500"
                      style={{ width: `${Math.min(100, (count as number / 200) * 100)}%` }}
                    ></div>
                  </div>
                </div>
                <div className="ml-4 text-sm font-mono text-gray-300">{count as React.ReactNode}</div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 bg-indigo-500/20 text-indigo-400 rounded-full flex items-center justify-center border border-indigo-500/50">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-200">Correlation Engine Active</h3>
              <p className="text-sm text-gray-400 mt-2 max-w-xs">
                Real-time correlation and similarity analysis is continuously processing new indicators across the enterprise.
              </p>
            </div>
        </div>
      </div>
    </div>
  );
};
