import axios from 'axios';

const API_BASE_URL = '/api/v1/network-investigation'; 

export interface NetworkInvestigationResult {
    flows: any[];
    dns: any[];
    http: any[];
    tls: any[];
    timeline: any[];
    iocs: any[];
    risk_score: Record<string, any>;
    ai_summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

export const investigateNetwork = async (export_payload: string): Promise<NetworkInvestigationResult> => {
    const response = await axios.post(`${API_BASE_URL}/investigate`, { export_payload });
    return response.data;
};
