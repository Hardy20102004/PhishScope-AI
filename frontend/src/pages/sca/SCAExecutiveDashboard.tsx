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

interface SCASummary {
  total_dependencies: number;
  vulnerable_dependencies: number;
  license_violations: number;
  average_risk_score: number;
  abandoned_packages: number;
}

export const SCAExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<SCASummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/sca/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching SCA summary:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Software Composition Analysis Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Dependencies
              </Typography>
              <Typography variant="h3">{summary?.total_dependencies || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Vulnerable Components
              </Typography>
              <Typography variant="h3" color="error">{summary?.vulnerable_dependencies || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                License Violations
              </Typography>
              <Typography variant="h3" color="warning.main">{summary?.license_violations || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Abandoned Packages
              </Typography>
              <Typography variant="h3" color="error.light">{summary?.abandoned_packages || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg Risk Score
              </Typography>
              <Typography variant="h3" color="primary">
                {summary?.average_risk_score.toFixed(1) || '0.0'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
