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

interface EngineeringMetric {
  id: string;
  project_name: string;
  technical_debt_score: number;
  security_trend_score: number;
  calculated_at: string;
}

export const CopilotDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<EngineeringMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await api.get('/api/v1/copilot/intelligence');
        setMetrics(response.data);
      } catch (error) {
        console.error('Error fetching copilot metrics:', error);
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
        Developer Security Copilot & Intelligence
      </Typography>
      
      <Grid container spacing={3}>
        {metrics.length === 0 ? (
          <Grid item xs={12}>
            <Typography>No engineering metrics available yet.</Typography>
          </Grid>
        ) : (
          metrics.map(metric => (
            <Grid item xs={12} md={4} key={metric.id}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Project: {metric.project_name}
                  </Typography>
                  
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6">Technical Debt Score</Typography>
                    <Typography 
                      variant="h3" 
                      color={metric.technical_debt_score > 50 ? 'error' : 'success'}
                    >
                      {metric.technical_debt_score}
                    </Typography>
                  </Box>

                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6">Security Trend Score</Typography>
                    <Typography 
                      variant="h3" 
                      color={metric.security_trend_score > 0 ? 'success' : 'error'}
                    >
                      {metric.security_trend_score > 0 ? '+' : ''}{metric.security_trend_score}
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
