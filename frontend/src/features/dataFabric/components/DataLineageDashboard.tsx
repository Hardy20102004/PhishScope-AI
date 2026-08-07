import React from 'react';

const DataLineageDashboard: React.FC = () => {
  return (
    <div className="p-6 h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4">Data Lineage & Traceability</h2>
      <div className="bg-white rounded-lg shadow border border-gray-200 flex-1 p-6 overflow-auto">
        <h3 className="text-sm font-semibold text-gray-700 mb-6 uppercase tracking-wider">Lineage Flow</h3>
        
        <div className="flex flex-col space-y-8">
          {/* Example Lineage Flow 1 */}
          <div className="flex items-center space-x-4">
            <div className="bg-blue-50 border border-blue-200 p-4 rounded flex-1">
              <h4 className="font-semibold text-blue-800">Source: AWS CloudTrail</h4>
              <p className="text-xs text-blue-600 mt-1">S3 Bucket / Raw Logs</p>
            </div>
            
            <div className="flex flex-col items-center justify-center text-gray-400 px-4">
              <span className="text-xs font-bold uppercase mb-1">Parsed By</span>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 p-4 rounded flex-1">
              <h4 className="font-semibold text-purple-800">Pipeline: CloudTrail Extractor</h4>
              <p className="text-xs text-purple-600 mt-1">Python ETL Script</p>
            </div>
            
            <div className="flex flex-col items-center justify-center text-gray-400 px-4">
              <span className="text-xs font-bold uppercase mb-1">Written To</span>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
            </div>
            
            <div className="bg-green-50 border border-green-200 p-4 rounded flex-1">
              <h4 className="font-semibold text-green-800">Sink: ElasticSearch</h4>
              <p className="text-xs text-green-600 mt-1">Index: sec-cloudtrail-*</p>
            </div>
          </div>

          {/* Example Lineage Flow 2 */}
          <div className="flex items-center space-x-4">
            <div className="bg-blue-50 border border-blue-200 p-4 rounded flex-1">
              <h4 className="font-semibold text-blue-800">Source: Okta System Log</h4>
              <p className="text-xs text-blue-600 mt-1">REST API</p>
            </div>
            
            <div className="flex flex-col items-center justify-center text-gray-400 px-4">
              <span className="text-xs font-bold uppercase mb-1">Parsed By</span>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 p-4 rounded flex-1">
              <h4 className="font-semibold text-purple-800">Pipeline: FluentD Agent</h4>
              <p className="text-xs text-purple-600 mt-1">Log Forwarder</p>
            </div>
            
            <div className="flex flex-col items-center justify-center text-gray-400 px-4">
              <span className="text-xs font-bold uppercase mb-1">Written To</span>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
            </div>
            
            <div className="bg-green-50 border border-green-200 p-4 rounded flex-1">
              <h4 className="font-semibold text-green-800">Sink: Splunk SIEM</h4>
              <p className="text-xs text-green-600 mt-1">Index: identity_auth</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataLineageDashboard;
