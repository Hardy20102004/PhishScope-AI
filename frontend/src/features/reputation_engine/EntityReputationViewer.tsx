import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

export const EntityReputationViewer: React.FC = () => {
  const { entityId } = useParams<{ entityId: string }>();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (entityId) {
      // Mocking fetch for a specific entity
      setTimeout(() => {
        setProfile({
          entity_id: entityId,
          entity_type: 'Domain',
          risk_score: 85,
          trust_score: 12,
          confidence: 0.9,
          trend: 'Declining',
          first_observed: '2023-01-15T08:00:00Z',
          last_updated: '2023-11-20T14:30:00Z',
          evidence: [
            { id: 1, source: 'CrowdStrike Feed', description: 'Domain flagged as hosting malware payload.', risk_delta: +40, trust_delta: -20, date: '2023-11-20' },
            { id: 2, source: 'Knowledge Graph Influence', description: 'Resolved to IP address with Risk Score 95.', risk_delta: +20, trust_delta: -10, date: '2023-11-18' }
          ]
        });
        setLoading(false);
      }, 500);
    } else {
      setLoading(false);
    }
  }, [entityId]);

  if (loading) return <div className="p-8 text-gray-400">Loading Reputation Profile...</div>;
  if (!profile) return <div className="p-8 text-center text-gray-400">Select an entity to view its reputation profile.</div>;

  return (
    <div className="bg-gray-900 min-h-screen p-6">
      <div className="flex justify-between items-start mb-8">
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <h2 className="text-3xl font-bold text-white">{profile.entity_id}</h2>
            <span className="px-2.5 py-0.5 rounded text-xs font-medium uppercase tracking-wider bg-gray-700 text-gray-300">
              {profile.entity_type}
            </span>
            <span className={`px-2.5 py-0.5 rounded text-xs font-medium uppercase tracking-wider 
              ${profile.trend === 'Declining' ? 'bg-orange-500/10 text-orange-400 border border-orange-500/20' : 'bg-green-500/10 text-green-400 border border-green-500/20'}`}>
              Trend: {profile.trend}
            </span>
          </div>
          <p className="text-gray-400 text-sm">Profile active since {new Date(profile.first_observed).toLocaleDateString()}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow flex flex-col items-center justify-center">
          <span className="text-gray-400 text-sm uppercase tracking-wider mb-2">Risk Score</span>
          <div className="relative w-32 h-32 flex items-center justify-center rounded-full border-8 border-gray-700">
             <div className="absolute inset-0 rounded-full border-8 border-red-500" style={{ clipPath: `polygon(0 0, 100% 0, 100% ${profile.risk_score}%, 0 ${profile.risk_score}%)` }}></div>
             <span className="text-4xl font-bold text-white z-10">{profile.risk_score}</span>
          </div>
        </div>
        
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow flex flex-col items-center justify-center">
          <span className="text-gray-400 text-sm uppercase tracking-wider mb-2">Trust Score</span>
          <div className="relative w-32 h-32 flex items-center justify-center rounded-full border-8 border-gray-700">
             <div className="absolute inset-0 rounded-full border-8 border-green-500" style={{ clipPath: `polygon(0 0, 100% 0, 100% ${profile.trust_score}%, 0 ${profile.trust_score}%)` }}></div>
             <span className="text-4xl font-bold text-white z-10">{profile.trust_score}</span>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow flex flex-col justify-center space-y-4">
           <div>
             <span className="text-xs text-gray-400 uppercase">Scoring Confidence</span>
             <div className="flex items-center mt-1">
               <div className="w-full bg-gray-700 rounded-full h-2 mr-3">
                 <div className="bg-cyan-500 h-2 rounded-full" style={{ width: `${profile.confidence * 100}%` }}></div>
               </div>
               <span className="text-sm font-bold text-cyan-400">{(profile.confidence * 100).toFixed(0)}%</span>
             </div>
           </div>
           <div>
             <span className="text-xs text-gray-400 uppercase">Last Updated</span>
             <p className="text-sm text-gray-200 mt-1">{new Date(profile.last_updated).toLocaleString()}</p>
           </div>
        </div>
      </div>

      <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white mb-4 border-b border-gray-700 pb-2 flex items-center">
          <svg className="w-5 h-5 mr-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Evidence Ledger
        </h3>
        <div className="space-y-4">
          {profile.evidence.map((ev: any) => (
            <div key={ev.id} className="bg-gray-900 p-4 rounded border border-gray-700">
              <div className="flex justify-between items-start mb-2">
                <span className="text-sm font-semibold text-cyan-400">{ev.source}</span>
                <span className="text-xs text-gray-500">{ev.date}</span>
              </div>
              <p className="text-sm text-gray-300 mb-3">{ev.description}</p>
              <div className="flex space-x-4">
                 <span className={`text-xs px-2 py-1 rounded font-medium ${ev.risk_delta > 0 ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-gray-800 text-gray-400'}`}>
                   Risk {ev.risk_delta > 0 ? '+' : ''}{ev.risk_delta}
                 </span>
                 <span className={`text-xs px-2 py-1 rounded font-medium ${ev.trust_delta < 0 ? 'bg-orange-500/10 text-orange-400 border border-orange-500/20' : 'bg-green-500/10 text-green-400 border border-green-500/20'}`}>
                   Trust {ev.trust_delta > 0 ? '+' : ''}{ev.trust_delta}
                 </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
