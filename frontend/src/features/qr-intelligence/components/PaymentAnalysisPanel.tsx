import React from 'react';

interface PaymentAnalysisPanelProps {
    payment: Record<string, any>;
}

const PaymentAnalysisPanel: React.FC<PaymentAnalysisPanelProps> = ({ payment }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full flex flex-col mt-6">
            <div className="bg-teal-50 px-4 py-3 border-b border-teal-100 flex justify-between items-center">
                <h2 className="text-teal-900 font-semibold flex items-center gap-2">
                    Payment Infrastructure Analysis
                </h2>
                <span className="bg-teal-600 text-white text-xs font-bold px-3 py-1 rounded">
                    {payment.payment_network}
                </span>
            </div>
            
            <div className="p-6 flex-1">
                <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-1">
                        <span className="block text-xs font-bold text-gray-500 uppercase tracking-wider">Merchant / Payee ID</span>
                        <span className="block text-lg font-mono text-gray-800 break-all">{payment.merchant_id || 'N/A'}</span>
                    </div>
                    
                    <div className="space-y-1">
                        <span className="block text-xs font-bold text-gray-500 uppercase tracking-wider">Transaction Amount</span>
                        {payment.transaction_amount ? (
                             <span className="block text-lg font-semibold text-gray-800">
                                 {payment.transaction_amount.toFixed(2)} {payment.currency}
                             </span>
                        ) : (
                             <span className="block text-lg font-medium text-gray-400 italic">Unspecified (User Entry)</span>
                        )}
                    </div>
                    
                    <div className="space-y-1">
                        <span className="block text-xs font-bold text-gray-500 uppercase tracking-wider">Payload Mutability</span>
                        {payment.is_dynamic ? (
                            <span className="inline-flex items-center gap-1 bg-yellow-100 text-yellow-800 text-xs font-bold px-2 py-1 rounded">
                                DYNAMIC (Fixed Amount)
                            </span>
                        ) : (
                            <span className="inline-flex items-center gap-1 bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded">
                                STATIC (Open Amount)
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PaymentAnalysisPanel;
