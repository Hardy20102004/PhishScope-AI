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

interface SBOMRecord {
  id: string;
  name: string;
  version: string;
  format: string;
  component_count: number;
  ingested_at: string;
}

export const SBOMDashboard: React.FC = () => {
  const [sboms, setSboms] = useState<SBOMRecord[]>([]);

  useEffect(() => {
    const fetchSboms = async () => {
      try {
        const response = await api.get('/api/v1/sbom/records');
        setSboms(response.data);
      } catch (error) {
        console.error('Error fetching SBOMs:', error);
      }
    };
    fetchSboms();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Software Bill of Materials (SBOM) Records
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Version</TableCell>
              <TableCell>Format</TableCell>
              <TableCell>Components</TableCell>
              <TableCell>Ingested At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sboms.map((sbom) => (
              <TableRow key={sbom.id}>
                <TableCell>{sbom.name}</TableCell>
                <TableCell>{sbom.version}</TableCell>
                <TableCell>
                  <Chip label={sbom.format} size="small" color="primary" />
                </TableCell>
                <TableCell>{sbom.component_count}</TableCell>
                <TableCell>{new Date(sbom.ingested_at).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
