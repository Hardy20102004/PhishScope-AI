import React, { useState } from 'react';
import { Smartphone, Sparkles, RefreshCw, X, AlertTriangle, ShieldCheck, Zap } from 'lucide-react';
import { investigateMobile, type MobileInvestigationResult } from '../api/mobileAPI';
import MobileAIFindings from './MobileAIFindings';
import DeviceOverview from './DeviceOverview';
import TimelineViewer from './TimelineViewer';
import ApplicationExplorer from './ApplicationExplorer';
import CommunicationExplorer from './CommunicationExplorer';
import LocationMap from './LocationMap';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const MobileInvestigationDashboard: React.FC = () => {
    const [payload, setPayload] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<MobileInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async (targetPayload?: string) => {
        const queryPayload = targetPayload || payload;
        if (!queryPayload) return;
        if (targetPayload) setPayload(queryPayload);

        setLoading(true);
        setError('');
        try {
            const data = await investigateMobile(queryPayload);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to process mobile forensic data.');
        } finally {
            setLoading(false);
        }
    };

    const loadUPIPreset = () => {
        const text = 'upi://pay?am=200.00&cu=INR&mc=0000&pa=7906731016%40mbkns&pn=Narshiesh&tid=P20863357512549703680000&tn=P20863357512549703680000';
        setPayload(text);
        handleInvestigate(text);
    };

    const loadRelaxoPreset = () => {
        const text = 'Dear Sir/Madam Thanks for shopping at Relaxo. As part of our green initiative, your digital bill awaits: http://truna.me/RELA';
        setPayload(text);
        handleInvestigate(text);
    };

    const getPayloadBadge = (text: string) => {
        const lower = text.toLowerCase();
        if (lower.includes('upi://pay') || lower.includes('pa=')) {
            const isScam = lower.includes('refund') || lower.includes('lotto') || lower.includes('blocked') || lower.includes('kyc') || lower.includes('mpin') || lower.includes('http');
            if (isScam) {
                return { label: 'Deceptive UPI Fraud / Collect Scam', color: 'bg-red-100 text-red-800 border-red-300' };
            }
            return { label: 'Standard UPI Payment Deep-Link (Valid VPA)', color: 'bg-emerald-100 text-emerald-800 border-emerald-300' };
        }
        if (lower.includes('sbi') || lower.includes('bank') || lower.includes('kyc')) {
            return { label: 'Banking Phishing SMS / Credential Harvesting', color: 'bg-red-100 text-red-800 border-red-300' };
        }
        if (lower.includes('.apk') || lower.includes('trojan') || lower.includes('patch')) {
            return { label: 'Trojan APK Dropper Link', color: 'bg-amber-100 text-amber-800 border-amber-300' };
        }
        if (text.trim().startsWith('{')) {
            return { label: 'Structured JSON Forensic Dump', color: 'bg-blue-100 text-blue-800 border-blue-300' };
        }

        return { label: 'Mobile Forensic Artifact', color: 'bg-gray-100 text-gray-800 border-gray-300' };
    };

    const badge = payload ? getPayloadBadge(payload) : null;

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <div className="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                        <Smartphone className="w-8 h-8 text-indigo-600" />
                        Mobile Device Investigation Platform
                    </h1>
                    <p className="text-gray-500 mt-1">Forensic analysis of lawfully acquired mobile artifacts, timelines, and communications.</p>
                </div>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8 space-y-4">
                <div>
                    <div className="flex items-center justify-between mb-2">
                        <label className="block text-sm font-semibold text-gray-800">
                            Simulate Forensic Export Upload (Paste UPI string, raw SMS, message log, or JSON export):
                        </label>
                        {badge && (
                            <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${badge.color}`}>
                                {badge.label}
                            </span>
                        )}
                    </div>

                    <div className="relative">
                        <textarea 
                            rows={3}
                            value={payload}
                            onChange={(e) => setPayload(e.target.value)}
                            placeholder="Paste raw SMS, UPI payment link (e.g. upi://pay?am=200.00&pa=7906731016@mbkns...), call log, or JSON export..." 
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono text-sm pr-10 resize-y"
                        />
                        {payload && (
                            <button
                                type="button"
                                onClick={() => setPayload('')}
                                className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        )}
                    </div>
                </div>

                <div className="flex flex-wrap items-center gap-2 text-xs text-gray-500">
                    <span className="font-semibold text-gray-700 flex items-center gap-1">
                        <Zap className="w-3.5 h-3.5 text-indigo-600" />
                        Quick Test Cases:
                    </span>
                    <button 
                        type="button"
                        onClick={loadUPIPreset}
                        className="px-2.5 py-1 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded border border-purple-200 font-medium transition-colors flex items-center gap-1"
                    >
                        <Sparkles className="w-3 h-3" />
                        UPI Payment Scam (7906731016@mbkns)
                    </button>
                    <button 
                        type="button"
                        onClick={loadRelaxoPreset}
                        className="px-2.5 py-1 bg-gray-100 hover:bg-indigo-50 hover:text-indigo-700 rounded border border-gray-200 font-mono transition-colors"
                    >
                        Relaxo Phishing Bill (truna.me)
                    </button>
                    <button 
                        type="button"
                        onClick={() => handleInvestigate('SBI Alert: Your NetBanking account will be blocked today. Update KYC immediately at: http://onlinesbi.phishing-portal.co.in')}
                        className="px-2.5 py-1 bg-gray-100 hover:bg-indigo-50 hover:text-indigo-700 rounded border border-gray-200 font-mono transition-colors"
                    >
                        SBI KYC Phishing (phishing-portal.co.in)
                    </button>
                    <button 
                        type="button"
                        onClick={() => handleInvestigate('Urgent Security Update: Download Android Patch APK to protect against malware: http://evil-login-update.com/apk')}
                        className="px-2.5 py-1 bg-gray-100 hover:bg-indigo-50 hover:text-indigo-700 rounded border border-gray-200 font-mono transition-colors"
                    >
                        Trojan APK Scam (evil-login-update.com)
                    </button>
                </div>
                
                <div className="flex justify-between items-center pt-2 border-t border-gray-100">
                    <button 
                        type="button"
                        onClick={loadUPIPreset}
                        className="text-indigo-600 hover:text-indigo-800 text-xs font-semibold hover:underline transition-colors flex items-center gap-1"
                    >
                        <Sparkles className="w-3.5 h-3.5" />
                        Load UPI Fraud Sample Export
                    </button>
                    <button 
                        onClick={() => handleInvestigate()}
                        disabled={loading || !payload}
                        className="bg-indigo-700 hover:bg-indigo-800 text-white px-8 py-3 rounded-lg font-semibold transition-all shadow-sm disabled:opacity-50 flex items-center justify-center min-w-[160px] gap-2"
                    >
                        {loading ? (
                            <>
                                <RefreshCw className="w-4 h-4 animate-spin" />
                                Processing...
                            </>
                        ) : (
                            <>
                                <Smartphone className="w-4 h-4" />
                                Process Artifacts
                            </>
                        )}
                    </button>
                </div>
                {error && <p className="text-red-500 text-sm font-medium mt-2">{error}</p>}
            </div>

            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    {/* Sidebar */}
                    <div className="lg:col-span-1 space-y-6">
                        <DeviceOverview metadata={result.device_metadata} />
                        <RiskDashboard score={result.risk_score} />
                    </div>

                    {/* Main Content */}
                    <div className="lg:col-span-3 space-y-6">
                        <MobileAIFindings summary={result.ai_summary} />
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <ApplicationExplorer applications={result.applications} />
                            <LocationMap locations={result.locations} />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <CommunicationExplorer communications={result.communications} iocs={result.iocs} />
                            <TimelineViewer timeline={result.timeline} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MobileInvestigationDashboard;

