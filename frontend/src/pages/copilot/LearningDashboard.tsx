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
  LinearProgress
} from '@mui/material';

interface LearningProgress {
  id: string;
  topic: string;
  modules_completed: number;
  last_engaged_at: string;
}

export const LearningDashboard: React.FC = () => {
  const [progress, setProgress] = useState<LearningProgress[]>([]);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const response = await api.get('/api/v1/copilot/learning');
        setProgress(response.data);
      } catch (error) {
        console.error('Error fetching learning progress:', error);
      }
    };
    fetchProgress();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Developer Security Training & Knowledge
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Security Topic</TableCell>
              <TableCell>Modules Completed</TableCell>
              <TableCell>Progress Tracker</TableCell>
              <TableCell>Last Engaged</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {progress.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} align="center">No active training modules</TableCell>
              </TableRow>
            ) : (
              progress.map((item) => (
                <TableRow key={item.id}>
                  <TableCell sx={{ fontWeight: 'bold' }}>{item.topic}</TableCell>
                  <TableCell>{item.modules_completed} Modules</TableCell>
                  <TableCell>
                    <LinearProgress 
                      variant="determinate" 
                      value={(item.modules_completed / 10) * 100} // assuming 10 is max for demo
                      sx={{ height: 10, borderRadius: 5 }}
                    />
                  </TableCell>
                  <TableCell>{new Date(item.last_engaged_at).toLocaleDateString()}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
