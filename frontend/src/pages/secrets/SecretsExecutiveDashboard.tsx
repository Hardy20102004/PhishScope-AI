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

interface SecretsSummary {
  total_active_secrets: number;
  total_exposures: number;
  expiring_certificates_30d: number;
  dormant_credentials: number;
}

export const SecretsExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<SecretsSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/secrets/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching secrets summary:', error);
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
        Secrets & Credential Governance
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Credentials Tracked
              </Typography>
              <Typography variant="h3">{summary?.total_active_secrets || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical Exposures
              </Typography>
              <Typography variant="h3" color="error">{summary?.total_exposures || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Certificates Expiring (30d)
              </Typography>
              <Typography variant="h3" color="warning.main">{summary?.expiring_certificates_30d || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Dormant Credentials
              </Typography>
              <Typography variant="h3" color="error.light">{summary?.dormant_credentials || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
