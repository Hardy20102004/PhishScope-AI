import axios from 'axios';

const API_BASE_URL = '/api/v1/website-investigation'; 

export interface WebsiteInvestigationResult {
    url: string;
    snapshot_metadata: Record<string, any>;
    html_analysis: Record<string, any>;
    javascript_analysis: any[];
    form_analysis: any[];
    cookie_analysis: Record<string, any>;
    security_headers: Record<string, any>;
    visual_analysis: Record<string, any>;
    risk_score: Record<string, any>;
    ai_summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

export const investigateWebsite = async (url: string): Promise<WebsiteInvestigationResult> => {
    const response = await axios.post(`${API_BASE_URL}/investigate`, { url });
    return response.data;
};
