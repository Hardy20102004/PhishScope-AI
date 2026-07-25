import React from 'react';

interface AuthenticationDashboardProps {
    auth: Record<string, any>;
}

const AuthenticationDashboard: React.FC<AuthenticationDashboardProps> = ({ auth }) => {
    const renderStatus = (val: string) => {
        if (val === 'pass') return <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-bold uppercase text-xs">PASS</span>;
        if (val === 'fail') return <span className="bg-red-100 text-red-800 px-2 py-1 rounded font-bold uppercase text-xs">FAIL</span>;
        return <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded font-bold uppercase text-xs">{val || 'UNKNOWN'}</span>;
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Sender Authentication</h2>
            
            <div className="space-y-4">
                <div className="flex justify-between items-center border-b pb-2">
                    <span className="font-semibold text-gray-600">SPF</span>
                    {renderStatus(auth.spf_result)}
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                    <span className="font-semibold text-gray-600">DKIM</span>
                    {renderStatus(auth.dkim_result)}
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                    <span className="font-semibold text-gray-600">DMARC</span>
                    {renderStatus(auth.dmarc_result)}
                </div>
            </div>

            {auth.is_spoofed && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm font-medium">
                    Authentication alignment failed. High probability of sender spoofing.
                </div>
            )}
        </div>
    );
};

export default AuthenticationDashboard;
