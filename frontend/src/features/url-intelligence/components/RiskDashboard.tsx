import React from 'react';

interface RiskDashboardProps {
    score: Record<string, any>;
}

const RiskDashboard: React.FC<RiskDashboardProps> = ({ score }) => {
    const riskLevel = score.threat_severity;
    const isCritical = riskLevel === 'CRITICAL';
    const isHigh = riskLevel === 'HIGH';
    const isMedium = riskLevel === 'MEDIUM';
    
    let colorClass = 'bg-green-100 text-green-800 border-green-200';
    if (isCritical) colorClass = 'bg-red-100 text-red-800 border-red-200';
    else if (isHigh) colorClass = 'bg-orange-100 text-orange-800 border-orange-200';
    else if (isMedium) colorClass = 'bg-yellow-100 text-yellow-800 border-yellow-200';

    return (
        <div className={`p-6 rounded-xl border ${colorClass}`}>
            <h2 className="text-lg font-semibold mb-2">Overall Risk Score</h2>
            <div className="flex items-end gap-2 mb-4">
                <span className="text-5xl font-bold">{score.overall_risk_score}</span>
                <span className="text-lg mb-1 opacity-75">/ 100</span>
            </div>
            
            <div className="space-y-3 mt-6">
                <div className="flex justify-between items-center border-b border-black/10 pb-2">
                    <span className="opacity-80">Threat Severity</span>
                    <span className="font-semibold">{score.threat_severity}</span>
                </div>
                <div className="flex justify-between items-center border-b border-black/10 pb-2">
                    <span className="opacity-80">Confidence</span>
                    <span className="font-semibold">{score.confidence}%</span>
                </div>
                <div className="flex justify-between items-center border-b border-black/10 pb-2">
                    <span className="opacity-80">Infrastructure Risk</span>
                    <span className="font-semibold">{score.infrastructure_risk}</span>
                </div>
                <div className="flex justify-between items-center pb-2">
                    <span className="opacity-80">Brand Risk</span>
                    <span className="font-semibold">{score.brand_risk}</span>
                </div>
            </div>
        </div>
    );
};

export default RiskDashboard;
