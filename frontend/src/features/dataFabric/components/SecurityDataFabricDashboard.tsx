import React, { useState, useEffect } from 'react';
import { dataFabricApi } from '../api/dataFabricApi';
import { DataFabricSummary } from '../types';
import MetadataCatalogDashboard from './MetadataCatalogDashboard';
import KnowledgeMeshDashboard from './KnowledgeMeshDashboard';
import DataLineageDashboard from './DataLineageDashboard';
import DataQualityDashboard from './DataQualityDashboard';
import GovernanceDashboard from './GovernanceDashboard';
import AIDataFabricAssistant from './AIDataFabricAssistant';

const SecurityDataFabricDashboard: React.FC = () => {
  const [summary, setSummary] = useState<DataFabricSummary | null>(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        const data = await dataFabricApi.getOverview();
        setSummary(data);
      } catch (error) {
        console.error('Failed to fetch data fabric overview', error);
      }
    };
    fetchOverview();
  }, []);

  const renderTabContent = () => {
    switch (activeTab) {
      case 'metadata':
        return <MetadataCatalogDashboard />;
      case 'knowledge':
        return <KnowledgeMeshDashboard />;
      case 'lineage':
        return <DataLineageDashboard />;
      case 'quality':
        return <DataQualityDashboard />;
      case 'governance':
        return <GovernanceDashboard />;
      default:
        return (
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
              <h3 className="text-sm font-medium text-gray-500 mb-1">Total Metadata Nodes</h3>
              <p className="text-3xl font-bold text-gray-900">{summary?.total_nodes || 0}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
              <h3 className="text-sm font-medium text-gray-500 mb-1">Knowledge Relationships</h3>
              <p className="text-3xl font-bold text-gray-900">{summary?.total_edges || 0}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
              <h3 className="text-sm font-medium text-gray-500 mb-1">Overall Data Quality</h3>
              <p className="text-3xl font-bold text-green-600">{summary?.overall_quality_score || 0}%</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
              <h3 className="text-sm font-medium text-gray-500 mb-1">Critical Issues</h3>
              <p className="text-3xl font-bold text-red-600">{summary?.critical_issues || 0}</p>
            </div>
            
            <div className="col-span-full mt-4">
               <AIDataFabricAssistant summary={summary} />
            </div>
          </div>
        );
    }
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-2xl font-bold text-gray-900">Enterprise Security Data Fabric</h1>
        <p className="text-sm text-gray-500 mt-1">Unified Cyber Knowledge Mesh & Intelligent Data Governance Platform</p>
        
        <div className="mt-6 flex space-x-6 border-b border-gray-200">
          {['overview', 'metadata', 'knowledge', 'lineage', 'quality', 'governance'].map((tab) => (
            <button
              key={tab}
              className={`pb-3 text-sm font-medium capitalize ${
                activeTab === tab
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>
      <div className="flex-1 overflow-auto">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default SecurityDataFabricDashboard;
