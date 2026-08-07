import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

interface ActorProfile {
  id: string;
  name: string;
  description: string;
  motivations: string[];
  target_sectors: string[];
  target_regions: string[];
  status: string;
  confidence: number;
  aliases: any[];
}

export const ActorExplorer: React.FC = () => {
  const { actorId } = useParams<{ actorId: string }>();
  const [profile, setProfile] = useState<ActorProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // For demonstration, mock a profile if no ID is passed or fetch fails
  useEffect(() => {
    if (actorId) {
      // In real implementation: fetch(`/api/v1/threat-actor/${actorId}`)
      setTimeout(() => {
        setProfile({
          id: actorId,
          name: 'APT29',
          description: 'A threat group that has been attributed to the Russian government...',
          motivations: ['Espionage', 'Information Theft'],
          target_sectors: ['Government', 'Defense', 'Technology'],
          target_regions: ['North America', 'Europe'],
          status: 'Active',
          confidence: 0.95,
          aliases: [{ id: '1', alias_name: 'Cozy Bear', source: 'CrowdStrike' }]
        });
        setLoading(false);
      }, 500);
    } else {
        setLoading(false);
    }
  }, [actorId]);

  if (loading) return <div className="p-8 text-gray-400">Loading Profile...</div>;
  
  if (!profile) return (
    <div className="p-8 text-center text-gray-400 bg-gray-900 h-full flex flex-col items-center justify-center">
      <svg className="w-16 h-16 mb-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      Select a Threat Actor from the directory to view their profile.
    </div>
  );

  return (
    <div className="bg-gray-900 min-h-screen p-6 overflow-y-auto">
      <div className="flex justify-between items-start mb-6">
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <h2 className="text-3xl font-bold text-white">{profile.name}</h2>
            <span className={`px-2.5 py-0.5 rounded text-xs font-medium uppercase tracking-wider
              ${profile.status === 'Active' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-gray-700 text-gray-300'}`}>
              {profile.status}
            </span>
          </div>
          <div className="flex space-x-2 text-sm text-gray-400">
            <span>Aliases: </span>
            {profile.aliases.map(a => (
              <span key={a.id} className="bg-gray-800 px-2 rounded border border-gray-700">{a.alias_name}</span>
            ))}
          </div>
        </div>
        <div className="bg-gray-800 px-4 py-2 rounded-lg border border-gray-700 flex flex-col items-end">
          <span className="text-xs text-gray-400 uppercase">Profile Confidence</span>
          <span className="text-xl font-bold text-blue-400">{(profile.confidence * 100).toFixed(0)}%</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-3">Description</h3>
            <p className="text-gray-300 leading-relaxed text-sm">{profile.description}</p>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
              <h3 className="text-md font-semibold text-gray-300 mb-3">Target Sectors</h3>
              <div className="flex flex-wrap gap-2">
                {profile.target_sectors.map(sector => (
                  <span key={sector} className="text-xs bg-gray-900 text-gray-300 px-2.5 py-1 rounded border border-gray-700">{sector}</span>
                ))}
              </div>
            </div>
            <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
              <h3 className="text-md font-semibold text-gray-300 mb-3">Target Regions</h3>
              <div className="flex flex-wrap gap-2">
                {profile.target_regions.map(region => (
                  <span key={region} className="text-xs bg-gray-900 text-gray-300 px-2.5 py-1 rounded border border-gray-700">{region}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
             <h3 className="text-lg font-semibold text-white mb-4 border-b border-gray-700 pb-2">Intelligence Links</h3>
             <ul className="space-y-3 text-sm">
               <li className="flex justify-between items-center text-gray-300 hover:text-white cursor-pointer p-2 rounded hover:bg-gray-700">
                 <div className="flex items-center">
                   <svg className="w-4 h-4 mr-2 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                   </svg>
                   Campaigns
                 </div>
                 <span className="bg-gray-900 px-2 py-0.5 rounded text-xs">12</span>
               </li>
               <li className="flex justify-between items-center text-gray-300 hover:text-white cursor-pointer p-2 rounded hover:bg-gray-700">
                 <div className="flex items-center">
                   <svg className="w-4 h-4 mr-2 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                   </svg>
                   Known Infrastructure
                 </div>
                 <span className="bg-gray-900 px-2 py-0.5 rounded text-xs">342</span>
               </li>
               <li className="flex justify-between items-center text-gray-300 hover:text-white cursor-pointer p-2 rounded hover:bg-gray-700">
                 <div className="flex items-center">
                   <svg className="w-4 h-4 mr-2 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                   </svg>
                   Malware Families
                 </div>
                 <span className="bg-gray-900 px-2 py-0.5 rounded text-xs">5</span>
               </li>
             </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
