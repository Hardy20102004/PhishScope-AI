import React from 'react';

const KnowledgeMeshDashboard: React.FC = () => {
  return (
    <div className="p-6 h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4">Unified Cyber Knowledge Mesh</h2>
      <div className="bg-white rounded-lg shadow border border-gray-200 flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
            <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 className="mt-2 text-sm font-medium text-gray-900">Graph Visualization Active</h3>
          <p className="mt-1 text-sm text-gray-500">Connecting semantic relationships across Security and Business Domains.</p>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeMeshDashboard;
