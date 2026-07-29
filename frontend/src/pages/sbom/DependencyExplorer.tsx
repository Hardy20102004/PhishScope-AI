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

interface Dependency {
  id: string;
  name: string;
  version: string;
  purl: string;
  is_direct: boolean;
  license: string;
  is_end_of_life: boolean;
}

export const DependencyExplorer: React.FC = () => {
  const [dependencies, setDependencies] = useState<Dependency[]>([]);

  useEffect(() => {
    const fetchDeps = async () => {
      try {
        const response = await api.get('/api/v1/sbom/dependencies');
        setDependencies(response.data);
      } catch (error) {
        console.error('Error fetching dependencies:', error);
      }
    };
    fetchDeps();
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
              <TableCell>Package Name</TableCell>
              <TableCell>Version</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>License</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dependencies.map((dep) => (
              <TableRow key={dep.id}>
                <TableCell>
                  <Typography variant="body1">{dep.name}</Typography>
                  {dep.purl && <Typography variant="caption" color="textSecondary">{dep.purl}</Typography>}
                </TableCell>
                <TableCell>{dep.version}</TableCell>
                <TableCell>
                  <Chip label={dep.is_direct ? 'Direct' : 'Transitive'} size="small" variant="outlined" />
                </TableCell>
                <TableCell>{dep.license || 'Unknown'}</TableCell>
                <TableCell>
                  {dep.is_end_of_life ? 
                    <Chip label="EOL" color="error" size="small" /> : 
                    <Chip label="Active" color="success" size="small" />
                  }
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
