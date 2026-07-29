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

interface ConfigurationFinding {
  id: string;
  severity: string;
  category: string;
  title: string;
  description: string;
  resource_id: string;
}

export const ConfigurationDashboard: React.FC = () => {
  const [findings, setFindings] = useState<ConfigurationFinding[]>([]);

  useEffect(() => {
    const fetchFindings = async () => {
      try {
        const response = await api.get('/api/v1/iac/findings');
        setFindings(response.data);
      } catch (error) {
        console.error('Error fetching IaC findings:', error);
      }
    };
    fetchFindings();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Configuration Weaknesses
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Severity</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Finding</TableCell>
              <TableCell>Resource</TableCell>
              <TableCell>Details</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {findings.map((finding) => (
              <TableRow key={finding.id}>
                <TableCell>
                  <Chip 
                    label={finding.severity} 
                    size="small" 
                    color={finding.severity === 'CRITICAL' ? 'error' : (finding.severity === 'HIGH' ? 'warning' : 'info')} 
                  />
                </TableCell>
                <TableCell>{finding.category}</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>{finding.title}</TableCell>
                <TableCell>{finding.resource_id}</TableCell>
                <TableCell>{finding.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
