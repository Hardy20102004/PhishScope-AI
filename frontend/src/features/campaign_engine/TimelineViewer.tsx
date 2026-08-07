import React, { useEffect, useState } from 'react';

export const TimelineViewer: React.FC<{ campaignId: string }> = ({ campaignId }) => {
  const [events, setEvents] = useState<any[]>([]);
  
  useEffect(() => {
    // Mocking timeline fetch
    setTimeout(() => {
      setEvents([
        { id: '1', date: '2023-10-15', type: 'Infrastructure', desc: 'VPS purchased via anonymized crypto wallet.' },
        { id: '2', date: '2023-10-18', type: 'Infrastructure', desc: 'Primary C2 domain registered.' },
        { id: '3', date: '2023-11-01', type: 'Execution', desc: 'First phishing wave sent to Aerospace targets.' },
        { id: '4', date: '2023-11-03', type: 'Payload', desc: 'New variant of Stealer malware compiled.' },
        { id: '5', date: '2023-11-12', type: 'Victimology', desc: 'Compromise of Defense Org A.' },
      ]);
    }, 500);
  }, [campaignId]);

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-semibold text-white mb-6 flex items-center border-b border-gray-700 pb-4">
        <svg className="w-5 h-5 mr-2 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        Campaign Timeline
      </h3>
      
      <div className="relative border-l-2 border-gray-700 ml-4 space-y-8 pb-4 mt-4">
        {events.map((event) => (
          <div key={event.id} className="relative pl-6 group">
            <div className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full border-2 border-gray-900 
              ${event.type === 'Infrastructure' ? 'bg-blue-500' : 
                event.type === 'Victimology' ? 'bg-yellow-500' : 
                event.type === 'Payload' ? 'bg-purple-500' : 'bg-red-500'}`}>
            </div>
            
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700 shadow-sm transition-transform duration-200 group-hover:translate-x-1 hover:border-gray-500 cursor-default">
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-mono text-gray-400 bg-gray-900 px-2 py-1 rounded border border-gray-750">
                  {event.date}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded font-medium 
                  ${event.type === 'Infrastructure' ? 'text-blue-400 bg-blue-400/10' : 
                    event.type === 'Victimology' ? 'text-yellow-400 bg-yellow-400/10' : 
                    event.type === 'Payload' ? 'text-purple-400 bg-purple-400/10' : 'text-red-400 bg-red-400/10'}`}>
                  {event.type}
                </span>
              </div>
              <p className="text-sm text-gray-300 mt-2">{event.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
