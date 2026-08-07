import axios from 'axios';

const API_BASE_URL = '/api/v1/mobile-investigation'; 

export interface MobileInvestigationResult {
    device_metadata: Record<string, any>;
    applications: any[];
    communications: any[];
    locations: any[];
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

export const investigateMobile = async (export_payload: string): Promise<MobileInvestigationResult> => {
    // In a real implementation, we'd upload an actual backup file using FormData.
    const response = await axios.post(`${API_BASE_URL}/investigate`, { export_payload });
    return response.data;
};
