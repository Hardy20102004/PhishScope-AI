import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CircularProgress,
  Button
} from '@mui/material';

interface AppSecExecutiveMetric {
  id: string;
  enterprise_risk_score: number;
  compliance_posture: number;
  total_critical_vulnerabilities: number;
}

export const AppSecExecutiveBoard: React.FC = () => {
  const [metrics, setMetrics] = useState<AppSecExecutiveMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await api.get('/api/v1/appsec-command-center/executive-summary');
        setMetrics(response.data);
      } catch (error) {
        console.error('Error fetching executive metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  const handleProposeDecision = async () => {
    try {
      await api.post('/api/v1/appsec-command-center/governance', {
        policy_name: "Enforce SAST Blocking Across Enterprise",
        proposed_change: "Modify CI/CD pipeline template to block merge requests with HIGH/CRITICAL SAST findings."
      });
      alert('Governance Decision Proposed Successfully! Awaiting Architect Approval.');
    } catch (e) {
      console.error(e);
      alert('Failed to propose decision.');
    }
  };

  if (loading) return <CircularProgress />;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        AppSec Executive & Board Presentation
      </Typography>
      
      <Grid container spacing={3}>
        {metrics.length === 0 ? (
          <Grid item xs={12}>
            <Typography>No executive metrics available.</Typography>
          </Grid>
        ) : (
          metrics.map(metric => (
            <Grid item xs={12} key={metric.id}>
              <Card sx={{ bgcolor: 'background.paper', mb: 3 }}>
                <CardContent>
                  <Grid container spacing={4}>
                    <Grid item xs={12} md={4}>
                      <Typography variant="h6">Enterprise Risk Score</Typography>
                      <Typography variant="h2" color={metric.enterprise_risk_score > 50 ? 'error' : 'success'}>
                        {metric.enterprise_risk_score.toFixed(1)} / 100
                      </Typography>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Typography variant="h6">Compliance Posture</Typography>
                      <Typography variant="h2" color={metric.compliance_posture < 80 ? 'error' : 'success'}>
                        {metric.compliance_posture.toFixed(1)}%
                      </Typography>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Typography variant="h6">Total Critical Vulnerabilities</Typography>
                      <Typography variant="h2" color={metric.total_critical_vulnerabilities > 0 ? 'error' : 'success'}>
                        {metric.total_critical_vulnerabilities}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
      
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>Strategic Governance</Typography>
        <Typography variant="body1" paragraph>
          Execute a human-governed strategic policy adjustment impacting the entire application portfolio.
        </Typography>
        <Button variant="contained" color="secondary" onClick={handleProposeDecision}>
          Propose Enterprise Policy Change
        </Button>
      </Box>
    </Box>
  );
};
