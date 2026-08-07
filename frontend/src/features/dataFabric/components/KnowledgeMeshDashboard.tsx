import React from 'react';

const KnowledgeMeshDashboard: React.FC = () => {
  return (
    <div className="p-6 h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4">Unified Cyber Knowledge Mesh</h2>
      <div className="bg-white rounded-lg shadow border border-gray-200 flex-1 p-6 overflow-auto">
        <h3 className="text-sm font-semibold text-gray-700 mb-4 uppercase tracking-wider">Discovered Semantic Relationships</h3>
        <div className="space-y-4">
          {[
            { source: 'admin_user', type: 'AUTHENTICATED_FROM', target: 'ip_192.168.1.50', risk: 'LOW' },
            { source: 'ip_192.168.1.50', type: 'COMMUNICATED_WITH', target: 'malicious_domain.com', risk: 'CRITICAL' },
            { source: 'process_powershell', type: 'SPAWNED_BY', target: 'winword.exe', risk: 'HIGH' },
            { source: 'aws_role_dev', type: 'HAS_PERMISSION', target: 's3_bucket_prod', risk: 'MEDIUM' }
          ].map((rel, idx) => (
            <div key={idx} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg border border-gray-100">
              <div className="flex-1 font-medium text-blue-600 text-right">{rel.source}</div>
              <div className="px-3 py-1 bg-gray-200 text-xs font-bold text-gray-700 rounded-full">{rel.type}</div>
              <div className="flex-1 font-medium text-purple-600">{rel.target}</div>
              <div className={`px-2 py-1 text-xs font-bold rounded ${
                rel.risk === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                rel.risk === 'HIGH' ? 'bg-orange-100 text-orange-800' :
                rel.risk === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
              }`}>{rel.risk}</div>
            </div>
          ))}
        </div>
        <div className="mt-8 text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
            <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <p className="mt-2 text-sm text-gray-500">Connecting semantic relationships across Security and Business Domains.</p>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeMeshDashboard;
