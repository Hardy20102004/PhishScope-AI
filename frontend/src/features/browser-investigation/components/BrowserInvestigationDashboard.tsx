import React, { useState } from 'react';
import { investigateBrowser, type BrowserInvestigationResult } from '../api/browserAPI';
import BrowserAIFindings from './BrowserAIFindings';
import TimelineViewer from './TimelineViewer';
import HistoryExplorer from './HistoryExplorer';
import ExtensionExplorer from './ExtensionExplorer';
import CookieExplorer from './CookieExplorer';
import DownloadExplorer from './DownloadExplorer';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const BrowserInvestigationDashboard: React.FC = () => {
    const [payload, setPayload] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<BrowserInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async () => {
        if (!payload) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateBrowser(payload);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to process browser forensic data.');
        } finally {
            setLoading(false);
        }
    };

    const loadMockData = () => {
        setPayload('{ "mock_browser_export": true }');
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <h1 className="text-3xl font-bold mb-2 text-gray-900">Browser Investigation Platform</h1>
            <p className="text-gray-500 mb-6">Forensic analysis of browser history, cookies, extensions, and downloads.</p>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Simulate Browser Profile Export Upload (JSON/SQLite):</label>
                    <input 
                        type="text"
                        value={payload}
                        onChange={(e) => setPayload(e.target.value)}
                        placeholder="e.g., { 'history': [...] }" 
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                    />
                </div>
                
                <div className="flex justify-between items-center">
                    <button 
                        onClick={loadMockData}
                        className="text-purple-600 hover:text-purple-800 text-sm font-medium transition-colors"
                    >
                        Load Mock Chrome Profile
                    </button>
                    <button 
                        onClick={handleInvestigate}
                        disabled={loading || !payload}
                        className="bg-purple-700 hover:bg-purple-800 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[140px]"
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
                        <ExtensionExplorer extensions={result.extensions} />
                    </div>

                    {/* Main Content */}
                    <div className="lg:col-span-3 space-y-6">
                        <BrowserAIFindings summary={result.ai_summary} />
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <HistoryExplorer history={result.history} />
                            <DownloadExplorer downloads={result.downloads} />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <CookieExplorer cookies={result.cookies} />
                            <TimelineViewer timeline={result.timeline} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BrowserInvestigationDashboard;
