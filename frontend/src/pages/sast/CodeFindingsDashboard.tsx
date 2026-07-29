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

interface SASTFinding {
  id: string;
  rule_id: string;
  file_path: string;
  line_number: number;
  severity: string;
  created_at: string;
}

export const CodeFindingsDashboard: React.FC = () => {
  const [findings, setFindings] = useState<SASTFinding[]>([]);

  useEffect(() => {
    const fetchFindings = async () => {
      try {
        const response = await api.get('/api/v1/sast/findings');
        setFindings(response.data);
      } catch (error) {
        console.error('Error fetching SAST findings:', error);
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
        Code Security Findings
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Rule ID</TableCell>
              <TableCell>File Path</TableCell>
              <TableCell>Line</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Discovered</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {findings.map((finding) => (
              <TableRow key={finding.id}>
                <TableCell>{finding.rule_id}</TableCell>
                <TableCell sx={{ fontFamily: 'monospace' }}>{finding.file_path}</TableCell>
                <TableCell>{finding.line_number}</TableCell>
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
