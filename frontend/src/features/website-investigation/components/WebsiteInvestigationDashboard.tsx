import React, { useState } from 'react';
import { investigateWebsite, type WebsiteInvestigationResult } from '../api/websiteAPI';
import WebsiteAIFindings from './WebsiteAIFindings';
import VisualInvestigationPanel from './VisualInvestigationPanel';
import SecurityDashboard from './SecurityDashboard';
import CodeExplorer from './CodeExplorer';
import DataViewer from './DataViewer';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const WebsiteInvestigationDashboard: React.FC = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<WebsiteInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async () => {
        if (!url) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateWebsite(url);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to investigate website.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <h1 className="text-3xl font-bold mb-2 text-gray-900">Advanced Website Investigation Platform</h1>
            <p className="text-gray-500 mb-6">Deep content analysis of HTML, DOM, JavaScript, Forms, and Visual UI.</p>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                <div className="flex gap-4">
                    <input 
                        type="url" 
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="Enter URL to perform deep content scan (e.g., https://example.com)" 
                        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        onKeyDown={(e) => e.key === 'Enter' && handleInvestigate()}
                    />
                    <button 
                        onClick={handleInvestigate}
                        disabled={loading}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[140px]"
                    >
                        {loading ? 'Scanning...' : 'Deep Scan'}
                    </button>
                </div>
                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Top Row */}
                    <div className="lg:col-span-1 space-y-6">
                        <RiskDashboard score={result.risk_score} />
                    </div>
                    <div className="lg:col-span-2">
                        <WebsiteAIFindings summary={result.ai_summary} />
                    </div>
                    
                    {/* Visual & Security */}
                    <div className="lg:col-span-2 space-y-6">
                        <VisualInvestigationPanel visual={result.visual_analysis} />
                    </div>
                    <div className="lg:col-span-1 space-y-6">
                        <SecurityDashboard security={result.security_headers} />
                    </div>
                    
                    {/* Code & Data */}
                    <div className="lg:col-span-2">
                        <CodeExplorer html={result.html_analysis} js={result.javascript_analysis} />
                    </div>
                    <div className="lg:col-span-1">
                        <DataViewer forms={result.form_analysis} cookies={result.cookie_analysis} />
                    </div>
                </div>
            )}
        </div>
    );
};

export default WebsiteInvestigationDashboard;
