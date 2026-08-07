import React from 'react';

interface TamperingViewerProps {
    tampering: Record<string, any>;
    visual: Record<string, any>;
}

const TamperingViewer: React.FC<TamperingViewerProps> = ({ tampering, visual }) => {
    const isTampered = tampering.has_overlay_sticker || tampering.has_logo_anomaly;

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Visual Tampering Analysis</h2>
            
            <div className="space-y-4">
                <div className="flex justify-between items-center border-b pb-3">
                    <div>
                        <span className="block font-semibold text-gray-700">Overlay Sticker Detected</span>
                        <span className="text-xs text-gray-500">Physical manipulation check</span>
                    </div>
                    {tampering.has_overlay_sticker ? (
                        <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full font-bold text-xs animate-pulse">DETECTED</span>
                    ) : (
                        <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full font-bold text-xs">CLEAR</span>
                    )}
                </div>
                
                <div className="flex justify-between items-center border-b pb-3">
                    <div>
                        <span className="block font-semibold text-gray-700">Logo / Error Block Anomaly</span>
                        <span className="text-xs text-gray-500">Digital manipulation check</span>
                    </div>
                    {tampering.has_logo_anomaly ? (
                        <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full font-bold text-xs">DETECTED</span>
                    ) : (
                        <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full font-bold text-xs">CLEAR</span>
                    )}
                </div>
                
                <div className="flex justify-between items-center pb-2">
                    <div>
                        <span className="block font-semibold text-gray-700">Detected Brand / Logo</span>
                    </div>
                    <span className="text-gray-800 font-medium">
                        {visual.detected_brand || 'None'}
                    </span>
                </div>
            </div>

            {isTampered && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm font-medium">
                    <p className="flex items-center gap-2">
                        <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
                        High probability of visual manipulation. Confidence: {(tampering.tampering_confidence * 100).toFixed(0)}%
                    </p>
                </div>
            )}
        </div>
    );
};

export default TamperingViewer;
