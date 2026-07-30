import React from 'react';
import type {  DataFabricSummary  } from "../types";

interface Props {
  summary: DataFabricSummary | null;
}

const AIDataFabricAssistant: React.FC<Props> = ({ summary }) => {
  return (
    <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
      <div className="flex items-center space-x-3 mb-4">
        <div className="bg-blue-600 p-2 rounded-lg">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-blue-900">AI Data Fabric Assistant</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-blue-800 uppercase tracking-wider mb-1">Analytical Assessment</h4>
          <p className="text-sm text-blue-900">{summary?.summary_text || 'Waiting for AI analysis...'}</p>
        </div>
        
        {summary?.recommendations && summary.recommendations.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-blue-800 uppercase tracking-wider mb-1">Recommendations</h4>
            <ul className="list-disc list-inside text-sm text-blue-900 space-y-1">
              {summary.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIDataFabricAssistant;
