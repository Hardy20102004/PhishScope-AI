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

interface IaCTemplate {
  id: string;
  name: string;
  technology: string;
  repository_url: string;
  file_path: string;
}

export const TemplateExplorer: React.FC = () => {
  const [templates, setTemplates] = useState<IaCTemplate[]>([]);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const response = await api.get('/api/v1/iac/templates');
        setTemplates(response.data);
      } catch (error) {
        console.error('Error fetching IaC templates:', error);
      }
    };
    fetchTemplates();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        IaC Template Explorer
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Template Name</TableCell>
              <TableCell>Technology</TableCell>
              <TableCell>Repository</TableCell>
              <TableCell>File Path</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {templates.map((tpl) => (
              <TableRow key={tpl.id}>
                <TableCell sx={{ fontWeight: 'bold' }}>{tpl.name}</TableCell>
                <TableCell>
                  <Chip label={tpl.technology} size="small" />
                </TableCell>
                <TableCell>{tpl.repository_url}</TableCell>
                <TableCell>{tpl.file_path}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
