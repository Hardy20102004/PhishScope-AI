import axios from 'axios';

const API_BASE_URL = '/api/v1/email-intelligence'; 

export interface EmailInvestigationResult {
    header_data: Record<string, any>;
    auth_results: Record<string, any>;
    routing_hops: any[];
    conversation_analysis: Record<string, any>;
    attachments: any[];
    campaign_correlation: Record<string, any>;
    risk_score: Record<string, any>;
    ai_summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

export const investigateEmail = async (raw_eml: string): Promise<EmailInvestigationResult> => {
    const response = await axios.post(`${API_BASE_URL}/investigate`, { raw_eml });
    return response.data;
};
