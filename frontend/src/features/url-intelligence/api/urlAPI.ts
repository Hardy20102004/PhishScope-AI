import axios from 'axios';

const API_BASE_URL = '/api/v1/url-intelligence'; // Assuming API routes through a proxy

export interface URLInvestigationResult {
    canonical_url: string;
    parsed: Record<string, any>;
    intelligence: Record<string, any>;
    redirect_chain: any[];
    infrastructure: Record<string, any>;
    brand: Record<string, any>;
    risk_score: Record<string, any>;
    ai_summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

export const investigateURL = async (url: string): Promise<URLInvestigationResult> => {
    const response = await axios.post(`${API_BASE_URL}/investigate`, { url });
    return response.data;
};
