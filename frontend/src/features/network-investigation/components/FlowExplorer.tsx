import React from 'react';

interface FlowExplorerProps {
    flows: any[];
}

const FlowExplorer: React.FC<FlowExplorerProps> = ({ flows }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Network Connections</h2>
            
            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                {flows.map((flow, idx) => (
                    <div key={idx} className="p-4 rounded-lg border bg-gray-50 border-gray-200">
                        <div className="flex justify-between items-start mb-2">
                            <span className="font-semibold text-gray-900 font-mono text-sm">
                                {flow.source_ip}:{flow.source_port} → {flow.destination_ip}:{flow.destination_port}
                            </span>
                            <span className="bg-gray-200 text-gray-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase">
                                {flow.protocol}
                            </span>
                        </div>
                        <div className="text-xs text-gray-500 mb-2">
                            {new Date(flow.timestamp).toLocaleString()}
                        </div>
                        <div className="flex justify-between text-xs font-mono text-gray-600 border-t border-gray-200 pt-2 mt-2">
                            <span>TX: {flow.bytes_sent} B</span>
                            <span>RX: {flow.bytes_received} B</span>
                            <span>Dur: {flow.duration}s</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FlowExplorer;
