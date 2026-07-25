import React from 'react';

interface CookieExplorerProps {
    cookies: any[];
}

const CookieExplorer: React.FC<CookieExplorerProps> = ({ cookies }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Cookies Analysis</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">Domain</th>
                            <th className="px-4 py-3">Name</th>
                            <th className="px-4 py-3">Flags</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cookies.map((cookie, idx) => (
                            <tr key={idx} className="bg-white border-b hover:bg-gray-50">
                                <td className="px-4 py-3 font-mono text-xs text-blue-600">{cookie.domain}</td>
                                <td className="px-4 py-3 font-medium text-gray-900 truncate max-w-[150px]">{cookie.name}</td>
                                <td className="px-4 py-3">
                                    <div className="flex gap-1">
                                        <span className={`text-[9px] px-1.5 py-0.5 rounded font-bold uppercase ${cookie.is_secure ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                            Secure
                                        </span>
                                        <span className={`text-[9px] px-1.5 py-0.5 rounded font-bold uppercase ${cookie.is_httponly ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                            HttpOnly
                                        </span>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default CookieExplorer;
