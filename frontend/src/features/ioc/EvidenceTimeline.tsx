import React from 'react';

interface EvidenceItem {
  id: string;
  type: string;
  description: string;
  source: string;
  timestamp: string;
  confidence: number;
}

interface EvidenceTimelineProps {
  relationshipId: string;
}

export const EvidenceTimeline: React.FC<EvidenceTimelineProps> = ({ relationshipId: _relationshipId }) => {
  // Mock data - in a real app, fetch based on relationshipId
  const evidence: EvidenceItem[] = [
    {
      id: 'e1',
      type: 'Infrastructure Analysis',
      description: 'Domain resolves to IP 192.168.1.100.',
      source: 'Internal Knowledge Graph',
      timestamp: '2023-10-27T10:15:30Z',
      confidence: 1.0
    },
    {
      id: 'e2',
      type: 'Heuristic Analysis',
      description: 'Malicious payload downloaded from IP.',
      source: 'CrowdStrike Intelligence',
      timestamp: '2023-10-27T11:00:00Z',
      confidence: 0.95
    },
    {
      id: 'e3',
      type: 'Historical Correlation',
      description: 'Attacker email previously registered similar typosquatting domains.',
      source: 'Historical Investigation Case #4021',
      timestamp: '2023-10-26T14:20:00Z',
      confidence: 0.8
    }
  ];

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-6 h-full">
      <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        Evidence Timeline
      </h3>
      
      <div className="relative border-l-2 border-gray-700 ml-3 space-y-8 pb-4">
        {evidence.map((item) => (
          <div key={item.id} className="relative pl-6 group">
            {/* Timeline Dot */}
            <div className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full border-2 border-gray-900 
              ${item.confidence > 0.9 ? 'bg-green-500' : item.confidence > 0.7 ? 'bg-yellow-500' : 'bg-red-500'}`}>
            </div>
            
            {/* Content Card */}
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700 shadow-sm transition-transform duration-200 group-hover:translate-x-1 group-hover:border-gray-500">
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-mono text-gray-400 bg-gray-900 px-2 py-1 rounded">
                  {new Date(item.timestamp).toLocaleString()}
                </span>
                <span className={`text-xs px-2 py-1 rounded font-medium 
                  ${item.confidence > 0.9 ? 'text-green-400 bg-green-400/10' : 
                    item.confidence > 0.7 ? 'text-yellow-400 bg-yellow-400/10' : 
                    'text-red-400 bg-red-400/10'}`}>
                  {(item.confidence * 100).toFixed(0)}% Conf.
                </span>
              </div>
              
              <h4 className="text-md font-medium text-white mb-1">{item.type}</h4>
              <p className="text-sm text-gray-300 mb-3">{item.description}</p>
              
              <div className="flex items-center text-xs text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Source: <span className="ml-1 text-gray-400 font-medium">{item.source}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {evidence.length === 0 && (
        <div className="text-center text-gray-500 mt-10">
          No evidence found for this relationship.
        </div>
      )}
    </div>
  );
};
