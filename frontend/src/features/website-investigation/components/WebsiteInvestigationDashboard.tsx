import React, { useState } from 'react';
import { investigateWebsite, type WebsiteInvestigationResult } from '../api/websiteAPI';
import WebsiteAIFindings from './WebsiteAIFindings';
import VisualInvestigationPanel from './VisualInvestigationPanel';
import SecurityDashboard from './SecurityDashboard';
import CodeExplorer from './CodeExplorer';
import DataViewer from './DataViewer';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';
import { FileSearch, Camera, Code2, FormInput, ShieldCheck, Sparkles } from 'lucide-react';

const WebsiteInvestigationDashboard: React.FC = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<WebsiteInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async (targetUrl?: string) => {
        const queryUrl = targetUrl || url;
        if (!queryUrl) return;
        if (targetUrl) setUrl(queryUrl);

        setLoading(true);
        setError('');
        try {
            const data = await investigateWebsite(queryUrl);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to investigate website.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800 font-sans">
            
            {/* Header Title with Content & Visual Layer Badge */}
            <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200 pb-4">
                <div>
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-purple-600 text-white rounded-lg shadow-sm">
                            <FileSearch size={24} />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                                Website Impersonation Scanner
                                <span className="text-xs bg-purple-100 text-purple-800 border border-purple-200 px-2.5 py-1 rounded-full font-bold uppercase tracking-wider">
                                    Content & Visual Layer
                                </span>
                            </h1>
                            <p className="text-gray-500 mt-1 text-sm">
                                Deep inspection of HTML DOM structure, JavaScript payload obfuscation, fake login forms, brand logo spoofing, and security headers.
                            </p>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2 text-xs font-mono bg-purple-50 text-purple-900 px-3 py-1.5 rounded-lg border border-purple-200">
                    <Sparkles size={14} className="text-purple-600" />
                    <span>Visual Impersonation AI Active</span>
                </div>
            </div>
            
            {/* Input Box & Quick Examples */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8 space-y-4">
                <div className="flex flex-col sm:flex-row gap-4">
                    <div className="relative flex-1">
                        <input 
                            type="url" 
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="Enter website URL to scan HTML, DOM, forms & visual UI (e.g., https://fake-login.paypal-security.net)" 
                            className="w-full pl-4 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                            onKeyDown={(e) => e.key === 'Enter' && handleInvestigate()}
                        />
                    </div>
                    <button 
                        onClick={() => handleInvestigate()}
                        disabled={loading}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2 min-w-[150px] text-sm"
                    >
                        {loading ? 'Scanning DOM...' : 'Deep Visual Scan'}
                    </button>
                </div>

                {/* Quick Sample Action Buttons */}
                <div className="flex flex-wrap items-center gap-2 pt-2 text-xs text-gray-500">
                    <span className="font-semibold text-gray-700">Quick Test Samples:</span>
                    <button 
                        type="button"
                        onClick={() => handleInvestigate('https://fake-login.paypal-security-update.net')}
                        className="px-2.5 py-1 bg-gray-100 hover:bg-purple-50 hover:text-purple-700 rounded border border-gray-200 font-mono transition-colors"
                    >
                        https://fake-login.paypal-security-update.net
                    </button>
                    <button 
                        type="button"
                        onClick={() => handleInvestigate('https://onlinesbi.phishing-portal.co.in')}
                        className="px-2.5 py-1 bg-gray-100 hover:bg-purple-50 hover:text-purple-700 rounded border border-gray-200 font-mono transition-colors"
                    >
                        https://onlinesbi.phishing-portal.co.in
                    </button>
                </div>

                {error && <p className="text-red-500 text-sm mt-2 font-medium">{error}</p>}
            </div>

            {/* Feature Highlights (Visible before scanning) */}
            {!result && !loading && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-purple-50 text-purple-600 rounded-lg w-fit">
                            <Camera size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">Visual UI & Logo Similarity</h3>
                        <p className="text-xs text-gray-500">Compares rendered screenshots against legitimate brand logos (SBI, PayPal, Google, HDFC).</p>
                    </div>

                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-rose-50 text-rose-600 rounded-lg w-fit">
                            <FormInput size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">Form & Credential Harvesters</h3>
                        <p className="text-xs text-gray-500">Detects hidden input forms, password inputs, OTP capture scripts, and POST action destinations.</p>
                    </div>

                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg w-fit">
                            <Code2 size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">HTML & JS Deobfuscation</h3>
                        <p className="text-xs text-gray-500">Parses script tags, inline JavaScript, eval() calls, and base64 encoded phishing payloads.</p>
                    </div>

                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg w-fit">
                            <ShieldCheck size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">Security Header Compliance</h3>
                        <p className="text-xs text-gray-500">Evaluates Content Security Policy (CSP), HSTS enforcement, X-Frame-Options, and CORS controls.</p>
                    </div>
                </div>
            )}

            {/* Results Display */}
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
