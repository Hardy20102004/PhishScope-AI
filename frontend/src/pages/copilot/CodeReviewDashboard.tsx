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

interface CodeReviewRecord {
  id: string;
  repository_url: string;
  pull_request_id: string;
  commit_hash: string;
  status: string;
  findings_count: number;
  created_at: string;
}

export const CodeReviewDashboard: React.FC = () => {
  const [reviews, setReviews] = useState<CodeReviewRecord[]>([]);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await api.get('/api/v1/copilot/review');
        setReviews(response.data);
      } catch (error) {
        console.error('Error fetching copilot reviews:', error);
      }
    };
    fetchReviews();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        AI Secure Code Review Log
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Repository</TableCell>
              <TableCell>Pull Request</TableCell>
              <TableCell>Commit</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Security Findings</TableCell>
              <TableCell>Reviewed At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reviews.map((review) => (
              <TableRow key={review.id}>
                <TableCell>{review.repository_url}</TableCell>
                <TableCell>{review.pull_request_id || 'N/A'}</TableCell>
                <TableCell sx={{ fontFamily: 'monospace' }}>{review.commit_hash?.substring(0,8) || 'N/A'}</TableCell>
                <TableCell>
                  <Chip 
                    label={review.status} 
                    size="small" 
                    color={review.status === 'COMPLETED' ? 'success' : 'warning'} 
                  />
                </TableCell>
                <TableCell>
                  <Typography color={review.findings_count > 0 ? 'error' : 'success'}>
                    {review.findings_count}
                  </Typography>
                </TableCell>
                <TableCell>{new Date(review.created_at).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
