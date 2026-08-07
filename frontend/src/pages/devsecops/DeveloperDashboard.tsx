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
  LinearProgress
} from '@mui/material';

interface DeveloperMetric {
  id: string;
  developer_email: string;
  code_quality_score: number;
  security_score: number;
  vulnerabilities_introduced: number;
  vulnerabilities_fixed: number;
}

export const DeveloperDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DeveloperMetric[]>([]);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await api.get('/api/v1/devsecops/developer-metrics');
        setMetrics(response.data);
      } catch (error) {
        console.error('Error fetching developer metrics:', error);
      }
    };
    fetchMetrics();
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'success';
    if (score >= 75) return 'warning';
    return 'error';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Developer Security Scorecards
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Developer</TableCell>
              <TableCell>Security Score</TableCell>
              <TableCell>Code Quality</TableCell>
              <TableCell>Vulns Fixed</TableCell>
              <TableCell>Vulns Introduced</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {metrics.map((dev) => (
              <TableRow key={dev.id}>
                <TableCell>{dev.developer_email}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box sx={{ width: '100%', mr: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={dev.security_score} 
                        color={getScoreColor(dev.security_score)}
                      />
                    </Box>
                    <Typography variant="body2">{Math.round(dev.security_score)}</Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box sx={{ width: '100%', mr: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={dev.code_quality_score} 
                        color={getScoreColor(dev.code_quality_score)}
                      />
                    </Box>
                    <Typography variant="body2">{Math.round(dev.code_quality_score)}</Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography color="success.main">+{dev.vulnerabilities_fixed}</Typography>
                </TableCell>
                <TableCell>
                  <Typography color="error.main">+{dev.vulnerabilities_introduced}</Typography>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
