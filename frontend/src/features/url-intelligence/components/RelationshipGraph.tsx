import React from 'react';

interface RelationshipGraphProps {
    data: any;
}

const RelationshipGraph: React.FC<RelationshipGraphProps> = ({ data }) => {
    // In a production app, this would use a library like react-force-graph or cytoscape
    // Here we create a simple tree representation
    
    return (
        <div className="bg-gray-50 rounded-lg p-6 border border-gray-100 flex flex-col items-center overflow-x-auto">
            
            <div className="bg-blue-600 text-white px-6 py-3 rounded-lg shadow-md font-bold mb-8 relative">
                {data.parsed?.root_domain || 'Target Domain'}
                <div className="absolute w-[2px] h-8 bg-gray-300 left-1/2 -bottom-8"></div>
            </div>
            
            <div className="w-full max-w-3xl border-t-2 border-gray-300 relative mb-8">
                 <div className="absolute w-[2px] h-8 bg-gray-300 left-[20%] top-0"></div>
                 <div className="absolute w-[2px] h-8 bg-gray-300 left-[50%] top-0"></div>
                 <div className="absolute w-[2px] h-8 bg-gray-300 left-[80%] top-0"></div>
            </div>
            
            <div className="w-full max-w-3xl flex justify-between">
                <div className="bg-white border-2 border-blue-200 px-4 py-2 rounded-lg text-center w-1/4 shadow-sm">
                    <span className="block text-xs text-gray-500 font-bold uppercase mb-1">IP Infrastructure</span>
                    <span className="font-mono text-sm text-gray-800">
                        {data.infrastructure?.ips?.length > 0 ? `${data.infrastructure.ips.length} Node(s)` : 'Unknown'}
                    </span>
                </div>
                
                <div className="bg-white border-2 border-green-200 px-4 py-2 rounded-lg text-center w-1/4 shadow-sm">
                    <span className="block text-xs text-gray-500 font-bold uppercase mb-1">Certificates</span>
                    <span className="font-mono text-sm text-gray-800">
                        {data.infrastructure?.certificates?.length > 0 ? `${data.infrastructure.certificates.length} Cert(s)` : 'None'}
                    </span>
                </div>
                
                <div className="bg-white border-2 border-purple-200 px-4 py-2 rounded-lg text-center w-1/4 shadow-sm">
                    <span className="block text-xs text-gray-500 font-bold uppercase mb-1">Brand Mapping</span>
                    <span className="text-sm font-semibold text-gray-800">
                        {data.brand?.targeted_brand || 'Generic'}
                    </span>
                </div>
            </div>
            
            {data.redirect_chain && data.redirect_chain.length > 0 && (
                <>
                    <div className="w-[2px] h-8 bg-gray-300 my-2"></div>
                    <div className="bg-white border-2 border-orange-200 px-4 py-2 rounded-lg text-center shadow-sm">
                        <span className="block text-xs text-gray-500 font-bold uppercase mb-1">Redirect Chain</span>
                        <span className="text-sm text-gray-800">{data.redirect_chain.length} Hop(s)</span>
                    </div>
                </>
            )}
            
        </div>
    );
};

export default RelationshipGraph;
