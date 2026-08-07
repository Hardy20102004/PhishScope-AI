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

interface SecretMetadata {
  id: string;
  name: string;
  secret_type: string;
  lifecycle_status: string;
  location_uri: string;
}

export const CredentialGovernanceDashboard: React.FC = () => {
  const [secrets, setSecrets] = useState<SecretMetadata[]>([]);

  useEffect(() => {
    const fetchSecrets = async () => {
      try {
        const response = await api.get('/api/v1/secrets/inventory');
        setSecrets(response.data);
      } catch (error) {
        console.error('Error fetching secrets inventory:', error);
      }
    };
    fetchSecrets();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Credential Inventory
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Credential Name</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {secrets.map((sec) => (
              <TableRow key={sec.id}>
                <TableCell sx={{ fontWeight: 'bold' }}>{sec.name}</TableCell>
                <TableCell>
                  <Chip label={sec.secret_type} size="small" />
                </TableCell>
                <TableCell>{sec.location_uri}</TableCell>
                <TableCell>
                  <Chip 
                    label={sec.lifecycle_status} 
                    size="small" 
                    color={sec.lifecycle_status === 'ACTIVE' ? 'success' : 'warning'} 
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
