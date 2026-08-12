import React, { useState, useRef } from 'react';
import jsQR from 'jsqr';
import { Upload, QrCode, FileImage, CheckCircle2, AlertCircle, X, Sparkles, RefreshCw } from 'lucide-react';
import { investigateQR, scanQRImage, type QRInvestigationResult } from '../api/qrAPI';
import QRAIFindings from './QRAIFindings';
import QRViewer from './QRViewer';
import PayloadViewer from './PayloadViewer';
import TamperingViewer from './TamperingViewer';
import PaymentAnalysisPanel from './PaymentAnalysisPanel';
import RiskDashboard from '../../url-intelligence/components/RiskDashboard';

const QRInvestigationDashboard: React.FC = () => {
    const [rawPayload, setRawPayload] = useState('');
    const [loading, setLoading] = useState(false);
    const [scanningImage, setScanningImage] = useState(false);
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [scanMessage, setScanMessage] = useState<{ text: string; type: 'success' | 'error' | 'info' } | null>(null);
    const [result, setResult] = useState<QRInvestigationResult | null>(null);
    const [error, setError] = useState('');
    
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleInvestigate = async (payloadToAnalyze?: string) => {
        const targetPayload = payloadToAnalyze || rawPayload;
        if (!targetPayload) return;
        setLoading(true);
        setError('');
        try {
            const data = await investigateQR(targetPayload);
            // If we have custom image metadata from an uploaded file, merge it
            if (uploadedFile && imagePreview) {
                const img = new Image();
                img.src = imagePreview;
                data.image_metadata = {
                    ...data.image_metadata,
                    filename: uploadedFile.name,
                    file_size_bytes: uploadedFile.size,
                    format: uploadedFile.type.split('/')[1] || 'png',
                };
            }
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to investigate QR code.');
        } finally {
            setLoading(false);
        }
    };

    const processQRImage = async (file: File) => {
        setUploadedFile(file);
        setScanningImage(true);
        setScanMessage(null);
        setError('');

        const previewUrl = URL.createObjectURL(file);
        setImagePreview(previewUrl);

        // Step 1: Client-side JS decoding using jsQR
        try {
            const img = new Image();
            img.onload = async () => {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                let extractedText: string | null = null;

                if (ctx) {
                    ctx.drawImage(img, 0, 0);
                    const imageData = ctx.getImageData(0, 0, img.width, img.height);
                    const code = jsQR(imageData.data, imageData.width, imageData.height);
                    if (code && code.data) {
                        extractedText = code.data;
                    }
                }

                // Step 2: Fallback to server-side scanning via OpenCV endpoint if jsQR didn't catch it
                if (!extractedText) {
                    try {
                        const backendScan = await scanQRImage(file);
                        if (backendScan.success && backendScan.raw_payload) {
                            extractedText = backendScan.raw_payload;
                        }
                    } catch (e) {
                        console.warn('Backend QR scan fallback error:', e);
                    }
                }

                setScanningImage(false);

                if (extractedText) {
                    setRawPayload(extractedText);
                    setScanMessage({
                        text: `QR Code successfully extracted! Data payload string found.`,
                        type: 'success'
                    });
                } else {
                    setScanMessage({
                        text: 'No clear QR code pattern detected in the uploaded photo. You can manually edit or paste payload below.',
                        type: 'error'
                    });
                }
            };
            img.onerror = () => {
                setScanningImage(false);
                setScanMessage({
                    text: 'Unable to read image file format. Please upload a valid PNG, JPG, or WEBP photo.',
                    type: 'error'
                });
            };
            img.src = previewUrl;
        } catch (err: any) {
            setScanningImage(false);
            setScanMessage({
                text: 'Error processing image: ' + (err.message || 'Unknown error'),
                type: 'error'
            });
        }
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            processQRImage(e.target.files[0]);
        }
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            processQRImage(e.dataTransfer.files[0]);
        }
    };

    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const clearUploadedImage = () => {
        setUploadedFile(null);
        setImagePreview(null);
        setScanMessage(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const loadMockUPI = () => {
        clearUploadedImage();
        setRawPayload("upi://pay?pa=fraudulent_merchant@bank&pn=VenmoSupport&am=500.00&cu=INR&tampered=true");
    };

    const loadMockURL = () => {
        clearUploadedImage();
        setRawPayload("https://malicious-login-update.com/qr-auth");
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen text-gray-800">
            <div className="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                        <QrCode className="w-8 h-8 text-indigo-600" />
                        QR Intelligence & Visual Scam Detection Platform
                    </h1>
                    <p className="text-gray-500 mt-1">Deep forensic analysis of QR images, payment payloads, and visual tampering indicators.</p>
                </div>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8 space-y-6">
                
                {/* File Upload Zone */}
                <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2 flex items-center justify-between">
                        <span className="flex items-center gap-2">
                            <Upload className="w-4 h-4 text-indigo-600" />
                            Option 1: Upload QR Photo / Image
                        </span>
                        <span className="text-xs font-normal text-gray-500">Supports PNG, JPG, JPEG, WEBP</span>
                    </label>

                    <input 
                        type="file" 
                        ref={fileInputRef} 
                        onChange={handleFileSelect} 
                        accept="image/*" 
                        className="hidden" 
                        id="qr-image-upload"
                    />

                    {!imagePreview ? (
                        <div 
                            onDrop={handleDrop}
                            onDragOver={handleDragOver}
                            onClick={() => fileInputRef.current?.click()}
                            className="border-2 border-dashed border-indigo-200 hover:border-indigo-500 bg-indigo-50/30 hover:bg-indigo-50/60 transition-all rounded-xl p-6 text-center cursor-pointer flex flex-col items-center justify-center group"
                        >
                            <div className="w-12 h-12 rounded-full bg-indigo-100 group-hover:bg-indigo-200 text-indigo-600 flex items-center justify-center mb-3 transition-colors">
                                <FileImage className="w-6 h-6" />
                            </div>
                            <p className="text-sm font-semibold text-gray-700">Click to upload or drag & drop QR photo here</p>
                            <p className="text-xs text-gray-400 mt-1">Automatic optical scan & data payload extraction</p>
                        </div>
                    ) : (
                        <div className="border border-gray-200 rounded-xl p-4 bg-gray-50 flex flex-col md:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-4">
                                <div className="w-20 h-20 bg-gray-900 rounded-lg overflow-hidden border border-gray-300 relative flex-shrink-0 flex items-center justify-center">
                                    <img src={imagePreview} alt="QR Preview" className="max-h-full max-w-full object-contain" />
                                </div>
                                <div>
                                    <h4 className="text-sm font-bold text-gray-800">{uploadedFile?.name}</h4>
                                    <p className="text-xs text-gray-500 mt-0.5">
                                        {(uploadedFile?.size ? (uploadedFile.size / 1024).toFixed(1) : '0')} KB &bull; Image Loaded
                                    </p>
                                    {scanningImage && (
                                        <div className="flex items-center gap-2 mt-2 text-xs font-semibold text-indigo-600">
                                            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                                            Scanning QR image & extracting data...
                                        </div>
                                    )}
                                </div>
                            </div>
                            <button
                                type="button"
                                onClick={clearUploadedImage}
                                className="text-xs text-gray-500 hover:text-red-600 flex items-center gap-1 bg-white border border-gray-200 px-3 py-1.5 rounded-lg shadow-sm hover:bg-red-50 transition-colors"
                            >
                                <X className="w-3.5 h-3.5" />
                                Remove Image
                            </button>
                        </div>
                    )}
                </div>

                {/* Scan Feedback Banner */}
                {scanMessage && (
                    <div className={`p-4 rounded-xl border flex items-start gap-3 text-sm ${
                        scanMessage.type === 'success' 
                            ? 'bg-emerald-50 border-emerald-200 text-emerald-800' 
                            : 'bg-amber-50 border-amber-200 text-amber-800'
                    }`}>
                        {scanMessage.type === 'success' ? (
                            <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                        ) : (
                            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                        )}
                        <div className="flex-1">
                            <p className="font-semibold">{scanMessage.text}</p>
                            {scanMessage.type === 'success' && rawPayload && (
                                <p className="mt-1 font-mono text-xs bg-white/70 p-2 rounded border border-emerald-200 text-emerald-900 break-all">
                                    {rawPayload}
                                </p>
                            )}
                        </div>
                    </div>
                )}

                {/* Manual Input / Extracted Payload Display */}
                <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">
                        Option 2: Extracted / Raw QR Payload String:
                    </label>
                    <div className="relative">
                        <input 
                            type="text"
                            value={rawPayload}
                            onChange={(e) => setRawPayload(e.target.value)}
                            placeholder="Extracted data string will appear here, or paste custom e.g., upi://pay?pa=... or https://..." 
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono text-sm pr-28 bg-white"
                        />
                        {rawPayload && (
                            <button
                                type="button"
                                onClick={() => setRawPayload('')}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        )}
                    </div>
                </div>

                {/* Action Bar */}
                <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-2 border-t border-gray-100">
                    <div className="flex gap-4">
                        <button 
                            onClick={loadMockUPI}
                            className="text-indigo-600 hover:text-indigo-800 text-xs font-semibold hover:underline transition-colors flex items-center gap-1"
                        >
                            <Sparkles className="w-3.5 h-3.5" />
                            Load Sample UPI QR
                        </button>
                        <button 
                            onClick={loadMockURL}
                            className="text-orange-600 hover:text-orange-800 text-xs font-semibold hover:underline transition-colors flex items-center gap-1"
                        >
                            <Sparkles className="w-3.5 h-3.5" />
                            Load Sample URL QR
                        </button>
                    </div>
                    
                    <button 
                        onClick={() => handleInvestigate()}
                        disabled={loading || !rawPayload || scanningImage}
                        className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-lg font-semibold transition-all shadow-sm hover:shadow disabled:opacity-50 flex items-center justify-center min-w-[160px] gap-2"
                    >
                        {loading ? (
                            <>
                                <RefreshCw className="w-4 h-4 animate-spin" />
                                Analyzing QR...
                            </>
                        ) : (
                            <>
                                <QrCode className="w-4 h-4" />
                                Analyze QR Payload
                            </>
                        )}
                    </button>
                </div>
                
                {error && <p className="text-red-500 text-sm font-medium mt-2">{error}</p>}
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
                        <QRViewer metadata={result.image_metadata} imageUrl={imagePreview || undefined} />
                    </div>
                </div>
            )}
        </div>
    );
};

export default QRInvestigationDashboard;

