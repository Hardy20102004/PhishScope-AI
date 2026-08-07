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

interface Artifact {
  id: string;
  name: string;
  version: string;
  type: string;
  hash_sha256: string;
  created_at: string;
}

export const ArtifactInventory: React.FC = () => {
  const [artifacts, setArtifacts] = useState<Artifact[]>([]);

  useEffect(() => {
    const fetchArtifacts = async () => {
      try {
        const response = await api.get('/api/v1/sbom/artifacts');
        setArtifacts(response.data);
      } catch (error) {
        console.error('Error fetching artifacts:', error);
      }
    };
    fetchArtifacts();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Software Artifact Inventory
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Version</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>SHA-256 Hash</TableCell>
              <TableCell>Added On</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {artifacts.map((artifact) => (
              <TableRow key={artifact.id}>
                <TableCell>{artifact.name}</TableCell>
                <TableCell>{artifact.version}</TableCell>
                <TableCell>
                  <Chip label={artifact.type} size="small" />
                </TableCell>
                <TableCell>
                  <Typography variant="caption" sx={{ fontFamily: 'monospace' }}>
                    {artifact.hash_sha256 ? artifact.hash_sha256.substring(0, 16) + '...' : 'N/A'}
                  </Typography>
                </TableCell>
                <TableCell>{new Date(artifact.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
