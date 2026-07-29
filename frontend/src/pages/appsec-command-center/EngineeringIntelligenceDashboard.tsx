import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CircularProgress 
} from '@mui/material';

interface EngineeringProductivityMetric {
  id: string;
  application_id: string;
  mean_time_to_remediate_days: number;
  deployment_frequency_per_week: number;
  security_friction_score: number;
}

export const EngineeringIntelligenceDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<EngineeringProductivityMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await api.get('/api/v1/appsec-command-center/engineering-intelligence');
        setMetrics(response.data);
      } catch (error) {
        console.error('Error fetching DevSecOps metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        DevSecOps Intelligence & Engineering Productivity
      </Typography>
      
      <Grid container spacing={3}>
        {metrics.length === 0 ? (
          <Grid item xs={12}>
            <Typography>No DevSecOps intelligence data available.</Typography>
          </Grid>
        ) : (
          metrics.map(metric => (
            <Grid item xs={12} md={4} key={metric.id}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Application: {metric.application_id}
                  </Typography>
                  
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6">Mean Time To Remediate (MTTR)</Typography>
                    <Typography variant="h4" color={metric.mean_time_to_remediate_days > 7 ? 'error' : 'success'}>
                      {metric.mean_time_to_remediate_days.toFixed(1)} Days
                    </Typography>
                  </Box>

                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6">Deployment Frequency</Typography>
                    <Typography variant="h4" color="primary">
                      {metric.deployment_frequency_per_week.toFixed(1)} / Week
                    </Typography>
                  </Box>
                  
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6">Security Friction Score</Typography>
                    <Typography variant="h4" color={metric.security_friction_score > 50 ? 'error' : 'success'}>
                      {metric.security_friction_score.toFixed(1)}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Box>
  );
};
