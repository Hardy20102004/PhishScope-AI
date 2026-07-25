import React from 'react';

interface SecurityDashboardProps {
    security: Record<string, any>;
}

const SecurityDashboard: React.FC<SecurityDashboardProps> = ({ security }) => {
    
    const renderStatus = (val: string) => {
        if (!val) return <span className="text-red-500 font-medium">Missing</span>;
        return <span className="text-green-600 font-mono text-sm break-all">{val}</span>;
    };
    
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4">Security Headers</h2>
            
            <div className="space-y-4 divide-y divide-gray-100">
                <div className="pt-2">
                    <span className="block text-xs font-bold text-gray-500 uppercase">Content-Security-Policy</span>
                    <div className="mt-1 bg-gray-50 p-2 rounded border border-gray-200">
                        {renderStatus(security.content_security_policy)}
                    </div>
                </div>
                
                <div className="pt-3">
                    <span className="block text-xs font-bold text-gray-500 uppercase">Strict-Transport-Security</span>
                    <div className="mt-1 bg-gray-50 p-2 rounded border border-gray-200">
                        {renderStatus(security.strict_transport_security)}
                    </div>
                </div>
                
                <div className="pt-3">
                    <span className="block text-xs font-bold text-gray-500 uppercase">X-Frame-Options</span>
                    <div className="mt-1 bg-gray-50 p-2 rounded border border-gray-200">
                        {renderStatus(security.x_frame_options)}
                    </div>
                </div>
                
                <div className="pt-3">
                    <span className="block text-xs font-bold text-gray-500 uppercase">X-Content-Type-Options</span>
                    <div className="mt-1 bg-gray-50 p-2 rounded border border-gray-200">
                        {renderStatus(security.x_content_type_options)}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SecurityDashboard;
