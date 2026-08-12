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
    const response = await axios.post(`${API_BASE_URL}/investigate`, { raw_payload });
    return response.data;
};

export interface QRScanResult {
    success: boolean;
    raw_payload?: string;
    payload_type?: string;
    message: string;
    metadata: {
        filename: string;
        resolution: string;
        file_size_bytes: number;
        format: string;
        contains_multiple_qrs: boolean;
    };
}

export const scanQRImage = async (file: File): Promise<QRScanResult> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE_URL}/scan-image`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

