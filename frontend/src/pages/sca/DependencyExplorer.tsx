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

interface SCADependency {
  id: string;
  ecosystem: string;
  package_name: string;
  resolved_version: string;
  dependency_type: string;
}

export const DependencyExplorer: React.FC = () => {
  const [dependencies, setDependencies] = useState<SCADependency[]>([]);

  useEffect(() => {
    const fetchDependencies = async () => {
      try {
        const response = await api.get('/api/v1/sca/dependencies');
        setDependencies(response.data);
      } catch (error) {
        console.error('Error fetching SCA dependencies:', error);
      }
    };
    fetchDependencies();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Dependency Explorer
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ecosystem</TableCell>
              <TableCell>Package Name</TableCell>
              <TableCell>Version</TableCell>
              <TableCell>Type</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dependencies.map((dep) => (
              <TableRow key={dep.id}>
                <TableCell>
                  <Chip label={dep.ecosystem} size="small" />
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>{dep.package_name}</TableCell>
                <TableCell>{dep.resolved_version}</TableCell>
                <TableCell>{dep.dependency_type}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
