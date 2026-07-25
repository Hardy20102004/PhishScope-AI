import React from 'react';

interface DeviceOverviewProps {
    metadata: Record<string, any>;
}

const DeviceOverview: React.FC<DeviceOverviewProps> = ({ metadata }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full">
            <div className="bg-gray-800 px-4 py-3 border-b border-gray-700 flex justify-between items-center">
                <h2 className="text-gray-100 font-semibold truncate">Device Profile</h2>
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
            </div>
            
            <div className="p-6">
                <div className="space-y-4">
                    <div className="border-b border-gray-100 pb-3">
                        <span className="block text-xs text-gray-500 uppercase tracking-wider mb-1">Manufacturer / Model</span>
                        <span className="font-semibold text-gray-900 text-lg">{metadata.manufacturer || 'Unknown'} {metadata.model || 'Device'}</span>
                    </div>
                    
                    <div className="border-b border-gray-100 pb-3">
                        <span className="block text-xs text-gray-500 uppercase tracking-wider mb-1">Operating System</span>
                        <span className="font-medium text-gray-800">{metadata.os_name} {metadata.os_version}</span>
                    </div>
                    
                    <div className="pb-1">
                        <span className="block text-xs text-gray-500 uppercase tracking-wider mb-1">Timezone / Locale</span>
                        <span className="font-mono text-sm text-gray-700 bg-gray-50 px-2 py-1 rounded border border-gray-200">{metadata.timezone || 'UTC'}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DeviceOverview;
