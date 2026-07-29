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

interface SCALicense {
  id: string;
  spdx_id: string;
  is_copyleft: boolean;
  is_approved: boolean;
}

export const LicenseDashboard: React.FC = () => {
  const [licenses, setLicenses] = useState<SCALicense[]>([]);

  useEffect(() => {
    const fetchLicenses = async () => {
      try {
        const response = await api.get('/api/v1/sca/licenses');
        setLicenses(response.data);
      } catch (error) {
        console.error('Error fetching SCA licenses:', error);
      }
    };
    fetchLicenses();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Open Source License Governance
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>SPDX ID</TableCell>
              <TableCell>Copyleft Risk</TableCell>
              <TableCell>Enterprise Policy</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {licenses.map((lic) => (
              <TableRow key={lic.id}>
                <TableCell>{lic.spdx_id}</TableCell>
                <TableCell>
                  <Chip 
                    label={lic.is_copyleft ? 'High Risk (Copyleft)' : 'Low Risk'} 
                    size="small" 
                    color={lic.is_copyleft ? 'error' : 'success'} 
                  />
                </TableCell>
                <TableCell>
                  <Chip 
                    label={lic.is_approved ? 'Approved' : 'Violates Policy'} 
                    size="small" 
                    color={lic.is_approved ? 'primary' : 'warning'} 
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
