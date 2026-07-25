import React from 'react';

interface LocationMapProps {
    locations: any[];
}

const LocationMap: React.FC<LocationMapProps> = ({ locations }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full flex flex-col">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Location Map</h2>
            
            <div className="bg-gray-100 flex-1 min-h-[200px] rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center relative overflow-hidden mb-4">
                <span className="text-gray-400 text-sm font-medium flex flex-col items-center">
                    <svg className="w-8 h-8 mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.242-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    Mock Map Component
                </span>
                
                {/* Mock Pin */}
                {locations.length > 0 && (
                    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                        <svg className="w-6 h-6 text-red-500 animate-bounce" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" /></svg>
                    </div>
                )}
            </div>

            <div className="space-y-2">
                {locations.map((loc, idx) => (
                    <div key={idx} className="flex justify-between items-center text-sm border-b border-gray-100 pb-2">
                        <div>
                            <span className="font-semibold text-gray-800 block">{loc.label || 'Unknown'}</span>
                            <span className="font-mono text-gray-500 text-xs">{loc.latitude}, {loc.longitude}</span>
                        </div>
                        <span className="text-gray-400 text-xs">{new Date(loc.timestamp).toLocaleString()}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LocationMap;
