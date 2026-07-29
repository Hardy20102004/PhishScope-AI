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

interface SASTRule {
  id: string;
  rule_id: string;
  name: string;
  cwe: string;
  owasp_category: string;
  severity: string;
}

export const RuleCoverageDashboard: React.FC = () => {
  const [rules, setRules] = useState<SASTRule[]>([]);

  useEffect(() => {
    const fetchRules = async () => {
      try {
        const response = await api.get('/api/v1/sast/rules');
        setRules(response.data);
      } catch (error) {
        console.error('Error fetching SAST rules:', error);
      }
    };
    fetchRules();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Rule Coverage & Configuration
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Rule ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>CWE</TableCell>
              <TableCell>OWASP</TableCell>
              <TableCell>Severity</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rules.map((rule) => (
              <TableRow key={rule.id}>
                <TableCell>{rule.rule_id}</TableCell>
                <TableCell>{rule.name}</TableCell>
                <TableCell>{rule.cwe}</TableCell>
                <TableCell>{rule.owasp_category}</TableCell>
                <TableCell>
                  <Chip label={rule.severity} size="small" variant="outlined" />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
