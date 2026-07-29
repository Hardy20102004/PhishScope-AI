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

interface DASTTarget {
  id: string;
  name: string;
  base_url: string;
  target_type: string;
  auth_method: string;
}

export const ApplicationTargetsDashboard: React.FC = () => {
  const [targets, setTargets] = useState<DASTTarget[]>([]);

  useEffect(() => {
    const fetchTargets = async () => {
      try {
        const response = await api.get('/api/v1/dast/targets');
        setTargets(response.data);
      } catch (error) {
        console.error('Error fetching DAST targets:', error);
      }
    };
    fetchTargets();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Authorized Application Targets
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Base URL</TableCell>
              <TableCell>Target Type</TableCell>
              <TableCell>Auth Method</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {targets.map((target) => (
              <TableRow key={target.id}>
                <TableCell>{target.name}</TableCell>
                <TableCell>
                  <Typography sx={{ fontFamily: 'monospace' }}>
                    <a href={target.base_url} target="_blank" rel="noreferrer" style={{ textDecoration: 'none', color: '#1976d2' }}>
                      {target.base_url}
                    </a>
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip label={target.target_type} size="small" color="primary" />
                </TableCell>
                <TableCell>{target.auth_method || 'None'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
