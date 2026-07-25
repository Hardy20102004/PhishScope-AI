import React from 'react';

interface DataViewerProps {
    forms: any[];
    cookies: Record<string, any>;
}

const DataViewer: React.FC<DataViewerProps> = ({ forms, cookies }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 h-full flex flex-col">
            <div className="p-6 border-b border-gray-100 flex-1">
                <h2 className="text-xl font-semibold mb-4">Form & Data Targets</h2>
                
                {forms.length === 0 ? (
                    <p className="text-gray-500 italic text-sm mb-6">No forms detected.</p>
                ) : (
                    <div className="space-y-4 mb-6">
                        {forms.map((form, idx) => (
                            <div key={idx} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                                <div className="flex justify-between items-start mb-2">
                                    <span className="text-sm font-semibold text-gray-700 truncate max-w-[70%]" title={form.action_url}>
                                        Target: {form.action_url || '<self>'}
                                    </span>
                                    {form.is_login && <span className="bg-red-100 text-red-700 text-xs px-2 py-1 rounded font-bold">LOGIN</span>}
                                </div>
                                <div className="flex flex-wrap gap-2 text-xs">
                                    {form.has_password_field && <span className="bg-gray-200 text-gray-700 px-2 py-1 rounded">Password Field</span>}
                                    {form.has_credit_card_field && <span className="bg-red-100 text-red-700 px-2 py-1 rounded">Credit Card Field</span>}
                                    {form.requests_personal_info && <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded">PII Requested</span>}
                                    {form.is_hidden && <span className="bg-gray-800 text-white px-2 py-1 rounded">Hidden Elements</span>}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
            
            <div className="p-6 bg-blue-50 flex-1 rounded-b-xl border-t border-blue-100">
                <h2 className="text-xl font-semibold mb-4 text-blue-900">Cookies & Storage</h2>
                
                <div className="flex justify-between items-center mb-4 bg-white p-3 rounded shadow-sm">
                    <span className="font-semibold text-gray-700">Insecure Cookies</span>
                    <span className={`text-xl font-bold ${cookies.insecure_count > 0 ? 'text-red-600' : 'text-green-600'}`}>
                        {cookies.insecure_count || 0}
                    </span>
                </div>
                
                {cookies.cookies && cookies.cookies.length > 0 && (
                    <div className="text-xs text-gray-600 space-y-1">
                        <p className="font-medium">Detected Cookies ({cookies.cookies.length}):</p>
                        <div className="flex flex-wrap gap-1">
                            {cookies.cookies.slice(0, 10).map((c: any, i: number) => (
                                <span key={i} className="bg-white border border-gray-200 px-2 py-1 rounded">
                                    {c.name}
                                </span>
                            ))}
                            {cookies.cookies.length > 10 && <span>...</span>}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DataViewer;
