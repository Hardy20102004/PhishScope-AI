import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { 
  Box, 
  Typography, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper,
  Chip
} from '@mui/material';

interface CertificateMetadata {
  id: string;
  name: string;
  location_uri: string;
  expires_at: string;
}

export const CertificateDashboard: React.FC = () => {
  const [certs, setCerts] = useState<CertificateMetadata[]>([]);

  useEffect(() => {
    const fetchCerts = async () => {
      try {
        const response = await api.get('/api/v1/secrets/certificates');
        setCerts(response.data);
      } catch (error) {
        console.error('Error fetching certificates:', error);
      }
    };
    fetchCerts();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        TLS Certificate Governance
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Certificate Name</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Expiration Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {certs.map((cert) => (
              <TableRow key={cert.id}>
                <TableCell sx={{ fontWeight: 'bold' }}>{cert.name}</TableCell>
                <TableCell>{cert.location_uri}</TableCell>
                <TableCell>
                  <Chip 
                    label={cert.expires_at ? new Date(cert.expires_at).toLocaleDateString() : 'Unknown'} 
                    size="small" 
                    color="warning" 
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
