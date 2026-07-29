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

interface DASTSummary {
  total_targets: number;
  active_scans: number;
  critical_findings: number;
  high_findings: number;
  endpoints_assessed_30d: number;
}

export const DASTExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<DASTSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/dast/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching DAST summary:', error);
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
        DAST & Runtime Assessment Executive Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Authorized Targets
              </Typography>
              <Typography variant="h3">{summary?.total_targets || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Scans
              </Typography>
              <Typography variant="h3" color="primary">{summary?.active_scans || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical Runtime Findings
              </Typography>
              <Typography variant="h3" color="error">{summary?.critical_findings || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                High Findings
              </Typography>
              <Typography variant="h3" color="warning.main">{summary?.high_findings || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Endpoints Assessed (30d)
              </Typography>
              <Typography variant="h3" color="info.main">
                {summary?.endpoints_assessed_30d ? summary.endpoints_assessed_30d.toLocaleString() : 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
