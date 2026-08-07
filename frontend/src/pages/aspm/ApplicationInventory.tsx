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

interface Application {
  id: string;
  name: string;
  description: string;
  criticality: string;
  is_internet_facing: boolean;
}

const ApplicationInventory: React.FC = () => {
  const [apps, setApps] = useState<Application[]>([]);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const response = await api.get('/api/v1/aspm/applications');
        setApps(response.data);
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    };
    fetchApps();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Application Inventory
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Criticality</TableCell>
              <TableCell>Exposure</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {apps.map((app) => (
              <TableRow key={app.id}>
                <TableCell>{app.name}</TableCell>
                <TableCell>{app.description}</TableCell>
                <TableCell>
                  <Chip 
                    label={app.criticality} 
                    color={app.criticality === 'CRITICAL' ? 'error' : app.criticality === 'HIGH' ? 'warning' : 'default'} 
                    size="small" 
                  />
                </TableCell>
                <TableCell>
                  {app.is_internet_facing ? 
                    <Chip label="Internet Facing" color="error" variant="outlined" size="small" /> : 
                    <Chip label="Internal" color="success" variant="outlined" size="small" />
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

export default ApplicationInventory;
