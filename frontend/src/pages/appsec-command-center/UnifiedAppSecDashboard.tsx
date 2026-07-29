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

interface AppSecConsolidatedFinding {
  id: string;
  application_id: string;
  source_scanner: string;
  severity: string;
  cwe_id: string;
  title: string;
  is_remediated: boolean;
  created_at: string;
}

export const UnifiedAppSecDashboard: React.FC = () => {
  const [findings, setFindings] = useState<AppSecConsolidatedFinding[]>([]);

  useEffect(() => {
    const fetchFindings = async () => {
      try {
        const response = await api.get('/api/v1/appsec-command-center/consolidated-findings');
        setFindings(response.data);
      } catch (error) {
        console.error('Error fetching consolidated findings:', error);
      }
    };
    fetchFindings();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Unified Application Security Command Center
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Application</TableCell>
              <TableCell>Scanner</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>CWE ID</TableCell>
              <TableCell>Vulnerability</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {findings.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">No consolidated findings available</TableCell>
              </TableRow>
            ) : (
              findings.map((finding) => (
                <TableRow key={finding.id}>
                  <TableCell sx={{ fontWeight: 'bold' }}>{finding.application_id}</TableCell>
                  <TableCell>
                    <Chip size="small" label={finding.source_scanner} color="primary" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      size="small" 
                      label={finding.severity} 
                      color={
                        finding.severity === 'CRITICAL' ? 'error' : 
                        finding.severity === 'HIGH' ? 'error' : 'warning'
                      } 
                    />
                  </TableCell>
                  <TableCell>{finding.cwe_id || 'N/A'}</TableCell>
                  <TableCell>{finding.title}</TableCell>
                  <TableCell>
                    <Chip 
                      size="small" 
                      label={finding.is_remediated ? 'Remediated' : 'Open'} 
                      color={finding.is_remediated ? 'success' : 'default'} 
                    />
                  </TableCell>
                  <TableCell>{new Date(finding.created_at).toLocaleDateString()}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
