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
import GitHubIcon from '@mui/icons-material/GitHub';
import DescriptionIcon from '@mui/icons-material/Description'; // Placeholder for other providers

interface Repository {
  id: string;
  name: string;
  url: string;
  provider: string;
  is_active: boolean;
  last_scanned: string | null;
}

const RepositoryDashboard: React.FC = () => {
  const [repos, setRepos] = useState<Repository[]>([]);

  useEffect(() => {
    const fetchRepos = async () => {
      try {
        const response = await api.get('/api/v1/aspm/repositories');
        setRepos(response.data);
      } catch (error) {
        console.error('Error fetching repositories:', error);
      }
    };
    fetchRepos();
  }, []);

  const getProviderIcon = (provider: string) => {
    switch (provider.toUpperCase()) {
      case 'GITHUB':
        return <GitHubIcon />;
      default:
        return <DescriptionIcon />;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Code Repositories
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Provider</TableCell>
              <TableCell>Repository Name</TableCell>
              <TableCell>URL</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Last Scanned</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {repos.map((repo) => (
              <TableRow key={repo.id}>
                <TableCell>{getProviderIcon(repo.provider)}</TableCell>
                <TableCell>{repo.name}</TableCell>
                <TableCell><a href={repo.url} target="_blank" rel="noreferrer">{repo.url}</a></TableCell>
                <TableCell>
                  {repo.is_active ? 
                    <Chip label="Active" color="success" size="small" /> : 
                    <Chip label="Inactive" color="default" size="small" />
                  }
                </TableCell>
                <TableCell>
                  {repo.last_scanned ? new Date(repo.last_scanned).toLocaleString() : 'Never'}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default RepositoryDashboard;
