import React, { useState } from 'react';
import { investigateCloud, type CloudInvestigationResult } from '../api/cloudAPI';
import CloudAIFindings from './CloudAIFindings';
import TimelineViewer from './TimelineViewer';
import AssetExplorer from './AssetExplorer';
import IdentityExplorer from './IdentityExplorer';
import ConfigurationViewer from './ConfigurationViewer';
import AuditLogViewer from './AuditLogViewer';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const CloudInvestigationDashboard: React.FC = () => {
    const [payload, setPayload] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<CloudInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async () => {
        if (!payload) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateCloud(payload);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to process cloud forensic data.');
        } finally {
            setLoading(false);
        }
    };

    const loadMockData = () => {
        setPayload('{ "mock_cloud_json": true }');
    };

    return (
        <div className="p-6 bg-slate-50 min-h-screen text-slate-800">
            <h1 className="text-3xl font-bold mb-2 text-slate-900">Cloud Investigation Platform</h1>
            <p className="text-slate-500 mb-6">Forensic analysis of cloud assets, identities, configurations, and audit logs.</p>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-8">
                <div className="mb-4">
                    <label className="block text-sm font-medium text-slate-700 mb-2">Simulate Cloud Export Upload (JSON):</label>
                    <input 
                        type="text"
                        value={payload}
                        onChange={(e) => setPayload(e.target.value)}
                        placeholder="e.g., { 'assets': [...], 'audit_logs': [...] }" 
                        className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono text-sm"
                    />
                </div>
                
                <div className="flex justify-between items-center">
                    <button 
                        onClick={loadMockData}
                        className="text-indigo-600 hover:text-indigo-800 text-sm font-medium transition-colors"
                    >
                        Load Mock AWS/GCP Profile
                    </button>
                    <button 
                        onClick={handleInvestigate}
                        disabled={loading || !payload}
                        className="bg-indigo-700 hover:bg-indigo-800 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[140px]"
                    >
                        {loading ? 'Processing...' : 'Process Artifacts'}
                    </button>
                </div>
                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    {/* Sidebar */}
                    <div className="lg:col-span-1 space-y-6">
                        <RiskDashboard score={result.risk_score} />
                        <AssetExplorer assets={result.assets} />
                    </div>

                    {/* Main Content */}
                    <div className="lg:col-span-3 space-y-6">
                        <CloudAIFindings summary={result.ai_summary} />
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <IdentityExplorer identities={result.identities} />
                            <ConfigurationViewer configs={result.configurations} />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <AuditLogViewer audits={result.audit_logs} />
                            <TimelineViewer timeline={result.timeline} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CloudInvestigationDashboard;
