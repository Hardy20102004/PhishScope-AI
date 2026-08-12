import React, { useState } from 'react';
import { investigateURL, type URLInvestigationResult } from '../api/urlAPI';
import AIFindingsPanel from './AIFindingsPanel';
import RiskDashboard from './RiskDashboard';
import EvidenceTimeline from './EvidenceTimeline';
import InfrastructureMap from './InfrastructureMap';
import RelationshipGraph from './RelationshipGraph';
import { Globe, Server, ArrowRightLeft, ShieldAlert, Sparkles, Network } from 'lucide-react';

const URLInvestigationDashboard: React.FC = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<URLInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async (targetUrl?: string) => {
        const queryUrl = targetUrl || url;
        if (!queryUrl) return;
        if (targetUrl) setUrl(targetUrl);

        setLoading(true);
        setError('');
        try {
            const data = await investigateURL(queryUrl);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to investigate URL.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800 font-sans">
            
            {/* Header Title with Network Layer Badge */}
            <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200 pb-4">
                <div>
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-600 text-white rounded-lg shadow-sm">
                            <Globe size={24} />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                                URL Intelligence Platform
                                <span className="text-xs bg-blue-100 text-blue-800 border border-blue-200 px-2.5 py-1 rounded-full font-bold uppercase tracking-wider">
                                    Network & Domain Layer
                                </span>
                            </h1>
                            <p className="text-gray-500 mt-1 text-sm">
                                Analyzes domain registration WHOIS, IP Geolocation, DNS records, multi-hop HTTP redirect chains, and threat intelligence correlation.
                            </p>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2 text-xs font-mono bg-blue-50 text-blue-900 px-3 py-1.5 rounded-lg border border-blue-200">
                    <Sparkles size={14} className="text-blue-600" />
                    <span>Gemini AI Engine Active</span>
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
                            placeholder="Enter domain or URL to inspect network & WHOIS info (e.g., https://evil-login-update.com)" 
                            className="w-full pl-4 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                            onKeyDown={(e) => e.key === 'Enter' && handleInvestigate()}
                        />
                    </div>
                    <button 
                        onClick={() => handleInvestigate()}
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2 min-w-[150px] text-sm"
                    >
                        {loading ? 'Analyzing...' : 'Investigate Network'}
                    </button>
                </div>

                {/* Quick Sample Action Buttons */}
                <div className="flex flex-wrap items-center gap-2 pt-2 text-xs text-gray-500">
                    <span className="font-semibold text-gray-700">Quick Test Samples:</span>
                    <button 
                        type="button"
                        onClick={() => handleInvestigate('https://evil-login-update.com')}
                        className="px-2.5 py-1 bg-gray-100 hover:bg-blue-50 hover:text-blue-700 rounded border border-gray-200 font-mono transition-colors"
                    >
                        https://evil-login-update.com
                    </button>
                    <button 
                        type="button"
                        onClick={() => handleInvestigate('http://phishing-bank-login.xyz')}
                        className="px-2.5 py-1 bg-gray-100 hover:bg-blue-50 hover:text-blue-700 rounded border border-gray-200 font-mono transition-colors"
                    >
                        http://phishing-bank-login.xyz
                    </button>
                </div>

                {error && <p className="text-red-500 text-sm mt-2 font-medium">{error}</p>}
            </div>

            {/* Feature Highlights (Visible before scanning) */}
            {!result && !loading && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-blue-50 text-blue-600 rounded-lg w-fit">
                            <Server size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">WHOIS & Registrar Info</h3>
                        <p className="text-xs text-gray-500">Domain creation age, registrar name, registrant anonymity, and WHOIS privacy status.</p>
                    </div>

                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg w-fit">
                            <Network size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">DNS & IP Infrastructure</h3>
                        <p className="text-xs text-gray-500">Resolves A/AAAA, MX, NS records, ASN numbers, hosting provider, and IP geolocation.</p>
                    </div>

                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-purple-50 text-purple-600 rounded-lg w-fit">
                            <ArrowRightLeft size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">HTTP Redirect Chains</h3>
                        <p className="text-xs text-gray-500">Traces multi-hop 301/302 shorteners, cloaked links, and final destination landing URLs.</p>
                    </div>

                    <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs space-y-2">
                        <div className="p-2 bg-amber-50 text-amber-600 rounded-lg w-fit">
                            <ShieldAlert size={20} />
                        </div>
                        <h3 className="font-bold text-gray-900 text-sm">Infrastructure Correlation</h3>
                        <p className="text-xs text-gray-500">Maps malicious IP clusters, ASN threat reputation, and shared phishing infrastructure.</p>
                    </div>
                </div>
            )}

            {/* Results Display */}
            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Top Section */}
                    <div className="lg:col-span-1 space-y-6">
                        <RiskDashboard score={result.risk_score} />
                        <AIFindingsPanel summary={result.ai_summary} />
                    </div>
                    
                    <div className="lg:col-span-2 space-y-6">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                            <h2 className="text-xl font-semibold mb-4 text-gray-900 flex items-center gap-2">
                                <ArrowRightLeft className="text-blue-600" size={20} />
                                Evidence Timeline (Redirects)
                            </h2>
                            <EvidenceTimeline chain={result.redirect_chain} />
                        </div>
                        
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                            <h2 className="text-xl font-semibold mb-4 text-gray-900 flex items-center gap-2">
                                <Server className="text-indigo-600" size={20} />
                                Infrastructure Correlated Data
                            </h2>
                            <InfrastructureMap infrastructure={result.infrastructure} brand={result.brand} />
                        </div>
                    </div>
                    
                    <div className="lg:col-span-3">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                            <h2 className="text-xl font-semibold mb-4 text-gray-900 flex items-center gap-2">
                                <Network className="text-purple-600" size={20} />
                                Relationship Graph
                            </h2>
                            <RelationshipGraph data={result} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default URLInvestigationDashboard;
