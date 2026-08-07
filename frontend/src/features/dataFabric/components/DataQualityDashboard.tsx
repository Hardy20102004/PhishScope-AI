import React from 'react';

const DataQualityDashboard: React.FC = () => {
  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Intelligent Data Quality</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
          <h3 className="text-lg font-medium mb-4">Quality Metrics</h3>
          <ul className="space-y-3">
             <li className="flex justify-between"><span className="text-gray-600">Completeness</span><span className="font-semibold text-green-600">98%</span></li>
             <li className="flex justify-between"><span className="text-gray-600">Consistency</span><span className="font-semibold text-green-600">95%</span></li>
             <li className="flex justify-between"><span className="text-gray-600">Freshness</span><span className="font-semibold text-yellow-600">88%</span></li>
             <li className="flex justify-between"><span className="text-gray-600">Accuracy Indicators</span><span className="font-semibold text-green-600">92%</span></li>
          </ul>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
          <h3 className="text-lg font-medium mb-4">AI Quality Assessment</h3>
          <p className="text-sm text-gray-600">Overall data quality is <span className="font-bold text-green-600">EXCELLENT</span>. Missing values detected in Threat Intelligence feeds from source B. Recommend automated backfill workflow.</p>
        </div>
      </div>
    </div>
  );
};

export default DataQualityDashboard;
