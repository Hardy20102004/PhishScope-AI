import axios from 'axios';

const API_BASE_URL = '/api/v1/cloud-investigation'; 

export interface CloudInvestigationResult {
    assets: any[];
    identities: any[];
    configurations: any[];
    audit_logs: any[];
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

export const investigateCloud = async (export_payload: string): Promise<CloudInvestigationResult> => {
    const response = await axios.post(`${API_BASE_URL}/investigate`, { export_payload });
    return response.data;
};
