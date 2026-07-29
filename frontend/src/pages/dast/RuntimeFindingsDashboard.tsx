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

interface DASTFinding {
  id: string;
  vulnerability_name: string;
  url: string;
  method: string;
  severity: string;
  created_at: string;
}

export const RuntimeFindingsDashboard: React.FC = () => {
  const [findings, setFindings] = useState<DASTFinding[]>([]);

  useEffect(() => {
    const fetchFindings = async () => {
      try {
        const response = await api.get('/api/v1/dast/findings');
        setFindings(response.data);
      } catch (error) {
        console.error('Error fetching DAST findings:', error);
      }
    };
    fetchFindings();
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'error';
      case 'HIGH': return 'warning';
      case 'MEDIUM': return 'info';
      case 'LOW': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Runtime Assessment Findings
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Vulnerability</TableCell>
              <TableCell>URL</TableCell>
              <TableCell>Method</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Discovered</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {findings.map((finding) => (
              <TableRow key={finding.id}>
                <TableCell>{finding.vulnerability_name}</TableCell>
                <TableCell sx={{ fontFamily: 'monospace' }}>{finding.url}</TableCell>
                <TableCell>
                  <Chip label={finding.method} size="small" />
                </TableCell>
                <TableCell>
                  <Chip 
                    label={finding.severity} 
                    size="small" 
                    color={getSeverityColor(finding.severity) as any} 
                  />
                </TableCell>
                <TableCell>{new Date(finding.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
