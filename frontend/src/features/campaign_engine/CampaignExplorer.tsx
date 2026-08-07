import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

export const CampaignExplorer: React.FC = () => {
  const { campaignId } = useParams<{ campaignId: string }>();
  const [campaign, setCampaign] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Mock data fetching
  useEffect(() => {
    if (campaignId) {
      setTimeout(() => {
        setCampaign({
          id: campaignId,
          name: 'Operation Ghost Hunt',
          description: 'A prolonged credential harvesting campaign targeting European defense contractors using overlapping VPS infrastructure.',
          status: 'Active',
          severity: 'Critical',
          confidence: 0.92,
          infrastructure_count: 45,
          victim_count: 12,
          created_at: '2023-11-01T10:00:00Z'
        });
        setLoading(false);
      }, 500);
    } else {
        setLoading(false);
    }
  }, [campaignId]);

  if (loading) return <div className="p-8 text-gray-400">Loading Campaign Profile...</div>;
  if (!campaign) return <div className="p-8 text-gray-400 text-center">Select a campaign to explore.</div>;

  return (
    <div className="bg-gray-900 min-h-screen p-6">
      <div className="flex justify-between items-start mb-6">
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <h2 className="text-3xl font-bold text-white">{campaign.name}</h2>
            <span className="px-2.5 py-0.5 rounded text-xs font-medium uppercase tracking-wider bg-red-500/10 text-red-400 border border-red-500/20">
              {campaign.status}
            </span>
            <span className="px-2.5 py-0.5 rounded text-xs font-medium uppercase tracking-wider bg-orange-500/10 text-orange-400 border border-orange-500/20">
              {campaign.severity} Severity
            </span>
          </div>
          <p className="text-gray-400 text-sm">Discovered via Auto-Clustering Engine on {new Date(campaign.created_at).toLocaleDateString()}</p>
        </div>
        <div className="bg-gray-800 px-4 py-2 rounded-lg border border-gray-700 flex flex-col items-end shadow">
          <span className="text-xs text-gray-400 uppercase tracking-wider">Cluster Confidence</span>
          <span className="text-2xl font-bold text-emerald-400">{(campaign.confidence * 100).toFixed(0)}%</span>
        </div>
      </div>

      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-6">
        <h3 className="text-lg font-semibold text-white mb-3">Intelligence Summary</h3>
        <p className="text-gray-300 leading-relaxed text-sm">{campaign.description}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
           <h3 className="text-lg font-semibold text-white mb-4 border-b border-gray-700 pb-2 flex justify-between">
             <span>Correlated Infrastructure</span>
             <span className="bg-blue-500/10 text-blue-400 text-xs px-2 py-1 rounded">{campaign.infrastructure_count} Indicators</span>
           </h3>
           <div className="space-y-3 text-sm">
             <div className="flex justify-between items-center bg-gray-900 p-2 rounded">
               <span className="text-gray-300">Domains (C2)</span>
               <span className="text-white font-medium">14</span>
             </div>
             <div className="flex justify-between items-center bg-gray-900 p-2 rounded">
               <span className="text-gray-300">IP Addresses (Hosting)</span>
               <span className="text-white font-medium">6</span>
             </div>
             <div className="flex justify-between items-center bg-gray-900 p-2 rounded">
               <span className="text-gray-300">Payload Hashes</span>
               <span className="text-white font-medium">25</span>
             </div>
           </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
           <h3 className="text-lg font-semibold text-white mb-4 border-b border-gray-700 pb-2 flex justify-between">
             <span>Victimology</span>
             <span className="bg-yellow-500/10 text-yellow-400 text-xs px-2 py-1 rounded">{campaign.victim_count} Targets</span>
           </h3>
           <div className="space-y-3 text-sm">
             <div className="flex justify-between items-center bg-gray-900 p-2 rounded border-l-2 border-yellow-500">
               <span className="text-gray-300">European Defense Org A</span>
               <span className="text-gray-500 text-xs">Nov 12</span>
             </div>
             <div className="flex justify-between items-center bg-gray-900 p-2 rounded border-l-2 border-yellow-500">
               <span className="text-gray-300">Aerospace Contractor B</span>
               <span className="text-gray-500 text-xs">Nov 15</span>
             </div>
             <div className="text-center pt-2">
               <button className="text-xs text-blue-400 hover:text-blue-300">View All 12 Victims...</button>
             </div>
           </div>
        </div>
      </div>
    </div>
  );
};
