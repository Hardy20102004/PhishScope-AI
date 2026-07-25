import React, { useState } from 'react';
import { investigateEmail, type EmailInvestigationResult } from '../api/emailAPI';
import EmailAIFindings from './EmailAIFindings';
import HeaderExplorer from './HeaderExplorer';
import AuthenticationDashboard from './AuthenticationDashboard';
import RoutingTimeline from './RoutingTimeline';
import ConversationViewer from './ConversationViewer';
import AttachmentExplorer from './AttachmentExplorer';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const EmailInvestigationDashboard: React.FC = () => {
    const [rawEml, setRawEml] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<EmailInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async () => {
        if (!rawEml) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateEmail(rawEml);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to investigate email.');
        } finally {
            setLoading(false);
        }
    };

    const loadMockEmail = () => {
        const mockEml = `Date: Mon, 25 Jul 2026 10:00:00 +0000\r\nFrom: "CEO Urgent" <ceo@example.com>\r\nTo: finance@example.com\r\nSubject: URGENT: Wire Transfer Required\r\nMessage-ID: <12345@example.com>\r\nAuthentication-Results: mx.google.com; spf=fail (google.com: domain of ceo@example.com does not designate 1.2.3.4 as permitted sender) smtp.mailfrom=ceo@example.com; dmarc=fail (p=REJECT sp=NONE dis=NONE) header.from=example.com\r\nReceived: from unknown (1.2.3.4) by mx.google.com\r\nContent-Type: multipart/mixed; boundary="boundary123"\r\n\r\n--boundary123\r\nContent-Type: text/plain\r\n\r\nPlease process this invoice immediately. Urgent action required.\r\nhttp://malicious-login-portal.com\r\n\r\n--boundary123\r\nContent-Type: application/pdf\r\nContent-Disposition: attachment; filename="invoice_overdue.pdf"\r\n\r\n%PDF-1.4...mock_binary_data...\r\n--boundary123--`;
        setRawEml(mockEml);
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <h1 className="text-3xl font-bold mb-2 text-gray-900">Enterprise Email Intelligence Platform</h1>
            <p className="text-gray-500 mb-6">Deep forensic analysis of EML files, Headers, Authentication, Routing, and Attachments.</p>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Paste Raw RFC 5322 EML Content:</label>
                    <textarea 
                        value={rawEml}
                        onChange={(e) => setRawEml(e.target.value)}
                        placeholder="Paste email headers and body here..." 
                        className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                    />
                </div>
                <div className="flex justify-between items-center">
                    <button 
                        onClick={loadMockEmail}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
                    >
                        Load Mock Phishing Email
                    </button>
                    <button 
                        onClick={handleInvestigate}
                        disabled={loading || !rawEml}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[140px]"
                    >
                        {loading ? 'Analyzing...' : 'Analyze Email'}
                    </button>
                </div>
                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Top Row: AI & Risk */}
                    <div className="lg:col-span-1 space-y-6">
                        <RiskDashboard score={result.risk_score} />
                        <AuthenticationDashboard auth={result.auth_results} />
                    </div>
                    <div className="lg:col-span-2">
                        <EmailAIFindings summary={result.ai_summary} campaign={result.campaign_correlation} />
                    </div>
                    
                    {/* Content Row */}
                    <div className="lg:col-span-2 space-y-6">
                        <HeaderExplorer headers={result.header_data} />
                        <ConversationViewer conversation={result.conversation_analysis} />
                    </div>
                    
                    {/* Sidebar Row */}
                    <div className="lg:col-span-1 space-y-6">
                        <RoutingTimeline routing={result.routing_hops} />
                        <AttachmentExplorer attachments={result.attachments} />
                    </div>
                </div>
            )}
        </div>
    );
};

export default EmailInvestigationDashboard;
