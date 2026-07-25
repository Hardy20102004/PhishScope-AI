import axios from 'axios';

const API_BASE_URL = '/api/v1/qr-intelligence'; 

export interface QRInvestigationResult {
    image_metadata: Record<string, any>;
    decoded_payload: Record<string, any>;
    visual_analysis: Record<string, any>;
    tampering_analysis: Record<string, any>;
    payment_analysis: Record<string, any>;
    risk_score: Record<string, any>;
    ai_summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

export const investigateQR = async (raw_payload: string): Promise<QRInvestigationResult> => {
    // In a full implementation, we'd upload an image file using FormData.
    // For this prototype, we pass the decoded raw payload or a simulated string.
    const response = await axios.post(`${API_BASE_URL}/investigate`, { raw_payload });
    return response.data;
};
