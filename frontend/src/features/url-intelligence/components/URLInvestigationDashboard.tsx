import React, { useState } from 'react';
import { investigateURL, type URLInvestigationResult } from '../api/urlAPI';
import AIFindingsPanel from './AIFindingsPanel';
import RiskDashboard from './RiskDashboard';
import EvidenceTimeline from './EvidenceTimeline';
import InfrastructureMap from './InfrastructureMap';
import RelationshipGraph from './RelationshipGraph';

const URLInvestigationDashboard: React.FC = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<URLInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async () => {
        if (!url) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateURL(url);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to investigate URL.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <h1 className="text-3xl font-bold mb-6 text-gray-900">Advanced URL Intelligence Platform</h1>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                <div className="flex gap-4">
                    <input 
                        type="url" 
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="Enter URL to investigate (e.g., https://example.com)" 
                        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        onKeyDown={(e) => e.key === 'Enter' && handleInvestigate()}
                    />
                    <button 
                        onClick={handleInvestigate}
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[140px]"
                    >
                        {loading ? 'Analyzing...' : 'Investigate'}
                    </button>
                </div>
                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Top Section */}
                    <div className="lg:col-span-1 space-y-6">
                        <RiskDashboard score={result.risk_score} />
                        <AIFindingsPanel summary={result.ai_summary} />
                    </div>
                    
                    <div className="lg:col-span-2 space-y-6">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <h2 className="text-xl font-semibold mb-4">Evidence Timeline (Redirects)</h2>
                            <EvidenceTimeline chain={result.redirect_chain} />
                        </div>
                        
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <h2 className="text-xl font-semibold mb-4">Infrastructure Correlated Data</h2>
                            <InfrastructureMap infrastructure={result.infrastructure} brand={result.brand} />
                        </div>
                    </div>
                    
                    <div className="lg:col-span-3">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <h2 className="text-xl font-semibold mb-4">Relationship Graph</h2>
                            <RelationshipGraph data={result} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default URLInvestigationDashboard;
