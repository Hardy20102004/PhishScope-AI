import React, { useState } from 'react';
import { investigateQR, type QRInvestigationResult } from '../api/qrAPI';
import QRAIFindings from './QRAIFindings';
import QRViewer from './QRViewer';
import PayloadViewer from './PayloadViewer';
import TamperingViewer from './TamperingViewer';
import PaymentAnalysisPanel from './PaymentAnalysisPanel';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const QRInvestigationDashboard: React.FC = () => {
    const [rawPayload, setRawPayload] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<QRInvestigationResult | null>(null);
    const [error, setError] = useState('');

    const handleInvestigate = async () => {
        if (!rawPayload) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateQR(rawPayload);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to investigate QR code.');
        } finally {
            setLoading(false);
        }
    };

    const loadMockUPI = () => {
        setRawPayload("upi://pay?pa=fraudulent_merchant@bank&pn=VenmoSupport&am=500.00&cu=INR&tampered=true");
    };

    const loadMockURL = () => {
        setRawPayload("https://malicious-login-update.com/qr-auth");
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <h1 className="text-3xl font-bold mb-2 text-gray-900">QR Intelligence & Visual Scam Detection Platform</h1>
            <p className="text-gray-500 mb-6">Deep forensic analysis of QR images, payment payloads, and visual tampering indicators.</p>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Simulate QR Image Upload (Paste Decoded String):</label>
                    <input 
                        type="text"
                        value={rawPayload}
                        onChange={(e) => setRawPayload(e.target.value)}
                        placeholder="e.g., https://example.com or upi://pay?pa=..." 
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                    />
                </div>
                <div className="flex justify-between items-center">
                    <div className="flex gap-4">
                        <button 
                            onClick={loadMockUPI}
                            className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
                        >
                            Load Tampered UPI QR
                        </button>
                        <button 
                            onClick={loadMockURL}
                            className="text-orange-600 hover:text-orange-800 text-sm font-medium transition-colors"
                        >
                            Load Malicious URL QR
                        </button>
                    </div>
                    <button 
                        onClick={handleInvestigate}
                        disabled={loading || !rawPayload}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[140px]"
                    >
                        {loading ? 'Analyzing...' : 'Analyze QR'}
                    </button>
                </div>
                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Top Row: AI & Risk */}
                    <div className="lg:col-span-1 space-y-6">
                        <RiskDashboard score={result.risk_score} />
                        <TamperingViewer tampering={result.tampering_analysis} visual={result.visual_analysis} />
                    </div>
                    <div className="lg:col-span-2">
                        <QRAIFindings summary={result.ai_summary} />
                    </div>
                    
                    {/* Details Row */}
                    <div className="lg:col-span-2 space-y-6">
                        <PayloadViewer decoded={result.decoded_payload} />
                        {result.decoded_payload.payload_type === 'payment_upi' && (
                             <PaymentAnalysisPanel payment={result.payment_analysis} />
                        )}
                    </div>
                    
                    {/* Image Meta Row */}
                    <div className="lg:col-span-1 space-y-6">
                        <QRViewer metadata={result.image_metadata} />
                    </div>
                </div>
            )}
        </div>
    );
};

export default QRInvestigationDashboard;
