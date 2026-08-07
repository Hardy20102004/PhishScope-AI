import React, { useState } from 'react';
import { investigateNetwork, type NetworkInvestigationResult } from '../api/networkAPI';
import NetworkAIFindings from './NetworkAIFindings';
import TimelineViewer from './TimelineViewer';
import FlowExplorer from './FlowExplorer';
import DNSExplorer from './DNSExplorer';
import HTTPExplorer from './HTTPExplorer';
import TLSExplorer from './TLSExplorer';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const NetworkInvestigationDashboard: React.FC = () => {
    const [payload, setPayload] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<NetworkInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async () => {
        if (!payload) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateNetwork(payload);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to process network forensic data.');
        } finally {
            setLoading(false);
        }
    };

    const loadMockData = () => {
        setPayload('{ "mock_zeek_json": true }');
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <h1 className="text-3xl font-bold mb-2 text-gray-900">Network Investigation Platform</h1>
            <p className="text-gray-500 mb-6">Forensic analysis of network flows, DNS queries, HTTP, and TLS metadata.</p>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Simulate Network Log Upload (Zeek JSON):</label>
                    <input 
                        type="text"
                        value={payload}
                        onChange={(e) => setPayload(e.target.value)}
                        placeholder="e.g., { 'conn': [...], 'dns': [...] }" 
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                    />
                </div>
                
                <div className="flex justify-between items-center">
                    <button 
                        onClick={loadMockData}
                        className="text-cyan-600 hover:text-cyan-800 text-sm font-medium transition-colors"
                    >
                        Load Mock PCAP/Zeek Profile
                    </button>
                    <button 
                        onClick={handleInvestigate}
                        disabled={loading || !payload}
                        className="bg-cyan-700 hover:bg-cyan-800 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[140px]"
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
                        <FlowExplorer flows={result.flows} />
                    </div>

                    {/* Main Content */}
                    <div className="lg:col-span-3 space-y-6">
                        <NetworkAIFindings summary={result.ai_summary} />
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <DNSExplorer dns={result.dns} />
                            <HTTPExplorer http={result.http} />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <TLSExplorer tls={result.tls} />
                            <TimelineViewer timeline={result.timeline} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default NetworkInvestigationDashboard;
