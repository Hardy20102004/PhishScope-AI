import React from 'react';

interface ApplicationExplorerProps {
    applications: any[];
}

const ApplicationExplorer: React.FC<ApplicationExplorerProps> = ({ applications }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Installed Applications</h2>
            
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                        <tr>
                            <th className="px-4 py-3">App Name</th>
                            <th className="px-4 py-3">Package</th>
                            <th className="px-4 py-3">Permissions</th>
                            <th className="px-4 py-3">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {applications.map((app, idx) => (
                            <tr key={idx} className="bg-white border-b hover:bg-gray-50">
                                <td className="px-4 py-3 font-medium text-gray-900">{app.app_name}</td>
                                <td className="px-4 py-3 font-mono text-xs">{app.package_name}</td>
                                <td className="px-4 py-3">
                                    <div className="flex flex-wrap gap-1">
                                        {app.permissions.map((perm: string, pIdx: number) => (
                                            <span key={pIdx} className="bg-gray-100 border border-gray-200 text-gray-600 text-[10px] px-1.5 py-0.5 rounded">
                                                {perm}
                                            </span>
                                        ))}
                                    </div>
                                </td>
                                <td className="px-4 py-3">
                                    {app.is_suspicious ? (
                                        <span className="bg-red-100 text-red-800 text-xs font-bold px-2 py-1 rounded">SUSPICIOUS</span>
                                    ) : (
                                        <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded">CLEAN</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ApplicationExplorer;
