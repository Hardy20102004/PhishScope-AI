import React from 'react';

interface InfrastructureMapProps {
    infrastructure: Record<string, any>;
    brand: Record<string, any>;
}

const InfrastructureMap: React.FC<InfrastructureMapProps> = ({ infrastructure }) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* DNS Records */}
            <div className="border border-gray-100 rounded-lg overflow-hidden">
                <div className="bg-gray-50 px-4 py-2 border-b border-gray-100 font-semibold text-sm text-gray-700">
                    DNS Resolution
                </div>
                <div className="p-4 space-y-3">
                    <div>
                        <span className="text-xs text-gray-500 uppercase font-semibold">IP Addresses (A)</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                            {infrastructure.ips?.length > 0 ? infrastructure.ips.map((ip: string, i: number) => (
                                <span key={i} className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-sm font-mono">{ip}</span>
                            )) : <span className="text-gray-400 text-sm">No records found</span>}
                        </div>
                    </div>
                    
                    <div>
                        <span className="text-xs text-gray-500 uppercase font-semibold">Nameservers (NS)</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                            {infrastructure.nameservers?.length > 0 ? infrastructure.nameservers.map((ns: string, i: number) => (
                                <span key={i} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm font-mono">{ns}</span>
                            )) : <span className="text-gray-400 text-sm">No records found</span>}
                        </div>
                    </div>
                    
                    <div>
                        <span className="text-xs text-gray-500 uppercase font-semibold">Mail Exchangers (MX)</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                            {infrastructure.mx_records?.length > 0 ? infrastructure.mx_records.map((mx: string, i: number) => (
                                <span key={i} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm font-mono">{mx}</span>
                            )) : <span className="text-gray-400 text-sm">No MX records</span>}
                        </div>
                    </div>
                </div>
            </div>
            
            {/* Certificate Analysis */}
            <div className="border border-gray-100 rounded-lg overflow-hidden">
                <div className="bg-gray-50 px-4 py-2 border-b border-gray-100 font-semibold text-sm text-gray-700">
                    Certificate Transparency
                </div>
                <div className="p-4">
                    {infrastructure.certificates?.length > 0 ? (
                        infrastructure.certificates.map((cert: any, i: number) => (
                            <div key={i} className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <span className="text-sm font-semibold">Subject</span>
                                    <span className={`text-xs px-2 py-1 rounded-full font-bold ${cert.is_valid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                        {cert.is_valid ? 'VALID' : 'INVALID'}
                                    </span>
                                </div>
                                <div className="text-sm font-mono bg-gray-50 p-2 rounded truncate" title={cert.subject}>{cert.subject}</div>
                                
                                <span className="text-sm font-semibold block mt-3">Issuer</span>
                                <div className="text-sm font-mono bg-gray-50 p-2 rounded truncate" title={cert.issuer}>{cert.issuer}</div>
                                
                                <div className="grid grid-cols-2 gap-2 mt-3">
                                    <div>
                                        <span className="text-xs text-gray-500 uppercase">Valid From</span>
                                        <div className="text-sm">{cert.valid_from ? new Date(cert.valid_from).toLocaleDateString() : 'N/A'}</div>
                                    </div>
                                    <div>
                                        <span className="text-xs text-gray-500 uppercase">Valid To</span>
                                        <div className="text-sm">{cert.valid_to ? new Date(cert.valid_to).toLocaleDateString() : 'N/A'}</div>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-500 text-sm italic">No certificates found.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default InfrastructureMap;
