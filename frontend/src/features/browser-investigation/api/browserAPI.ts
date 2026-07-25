import axios from 'axios';

const API_BASE_URL = '/api/v1/browser-investigation'; 

export interface BrowserInvestigationResult {
    history: any[];
    cookies: any[];
    extensions: any[];
    downloads: any[];
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

export const investigateBrowser = async (export_payload: string): Promise<BrowserInvestigationResult> => {
    const response = await axios.post(`${API_BASE_URL}/investigate`, { export_payload });
    return response.data;
};
