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

interface SecretExposure {
  id: string;
  exposure_type: string;
  severity: string;
  details: string;
  detected_at: string;
}

export const ExposureDashboard: React.FC = () => {
  const [exposures, setExposures] = useState<SecretExposure[]>([]);

  useEffect(() => {
    const fetchExposures = async () => {
      try {
        const response = await api.get('/api/v1/secrets/exposures');
        setExposures(response.data);
      } catch (error) {
        console.error('Error fetching secret exposures:', error);
      }
    };
    fetchExposures();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Secret Exposures & Risks
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Exposure Type</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Details</TableCell>
              <TableCell>Detected At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {exposures.map((exp) => (
              <TableRow key={exp.id}>
                <TableCell>{exp.exposure_type}</TableCell>
                <TableCell>
                  <Chip 
                    label={exp.severity} 
                    size="small" 
                    color={exp.severity === 'CRITICAL' ? 'error' : 'warning'} 
                  />
                </TableCell>
                <TableCell>{exp.details}</TableCell>
                <TableCell>{new Date(exp.detected_at).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
