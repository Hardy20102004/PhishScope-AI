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

interface PipelineRun {
  id: string;
  ci_provider: string;
  run_identifier: string;
  branch: string;
  commit_sha: string;
  status: string;
  sdlc_phase: string;
}

export const PipelineDashboard: React.FC = () => {
  const [pipelines, setPipelines] = useState<PipelineRun[]>([]);

  useEffect(() => {
    const fetchPipelines = async () => {
      try {
        const response = await api.get('/api/v1/devsecops/pipelines');
        setPipelines(response.data);
      } catch (error) {
        console.error('Error fetching pipelines:', error);
      }
    };
    fetchPipelines();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'SUCCESS': return 'success';
      case 'FAILED': return 'error';
      case 'BLOCKED': return 'error';
      case 'RUNNING': return 'primary';
      case 'QUEUED': return 'default';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        CI/CD Pipeline Security Integration
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>CI Provider</TableCell>
              <TableCell>Run ID</TableCell>
              <TableCell>Branch</TableCell>
              <TableCell>SDLC Phase</TableCell>
              <TableCell>Security Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {pipelines.map((pipe) => (
              <TableRow key={pipe.id}>
                <TableCell>{pipe.ci_provider}</TableCell>
                <TableCell>{pipe.run_identifier}</TableCell>
                <TableCell>
                  <Chip label={pipe.branch} size="small" />
                  <Typography variant="caption" sx={{ ml: 1 }}>
                    {pipe.commit_sha.substring(0, 7)}
                  </Typography>
                </TableCell>
                <TableCell>{pipe.sdlc_phase}</TableCell>
                <TableCell>
                  <Chip 
                    label={pipe.status} 
                    color={getStatusColor(pipe.status)} 
                    size="small" 
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
