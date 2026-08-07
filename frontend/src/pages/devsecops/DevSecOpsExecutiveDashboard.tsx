import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CircularProgress,
  Chip
} from '@mui/material';

interface DevSecOpsSummary {
  total_pipelines_run: number;
  failed_security_gates: number;
  open_exception_requests: number;
  average_security_score: number;
}

export const DevSecOpsExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<DevSecOpsSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/devsecops/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching DevSecOps summary:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        DevSecOps Executive Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Pipeline Runs
              </Typography>
              <Typography variant="h3">
                {summary?.total_pipelines_run || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Failed Security Gates
              </Typography>
              <Typography variant="h3" color="error">
                {summary?.failed_security_gates || 0}
              </Typography>
              <Chip label="Blocked Pipelines" color="error" size="small" sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending Exceptions
              </Typography>
              <Typography variant="h3" color="warning.main">
                {summary?.open_exception_requests || 0}
              </Typography>
              <Chip label="Needs Approval" color="warning" size="small" sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg. Dev Security Score
              </Typography>
              <Typography variant="h3" color="primary">
                {summary?.average_security_score || 100}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
