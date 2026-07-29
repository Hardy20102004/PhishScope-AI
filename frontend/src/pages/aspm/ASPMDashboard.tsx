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

interface ExecutiveSummary {
  total_applications: int;
  critical_applications: int;
  total_repositories: int;
  average_risk_score: number;
  open_critical_findings: int;
  open_high_findings: int;
}

const ASPMDashboard: React.FC = () => {
  const [summary, setSummary] = useState<ExecutiveSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/aspm/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching ASPM summary:', error);
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
        ASPM Executive Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Applications
              </Typography>
              <Typography variant="h3">
                {summary?.total_applications || 0}
              </Typography>
              <Chip 
                label={`${summary?.critical_applications || 0} Critical`} 
                color="error" 
                size="small" 
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Connected Repositories
              </Typography>
              <Typography variant="h3">
                {summary?.total_repositories || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Open Vulnerabilities
              </Typography>
              <Typography variant="h3" color="error">
                {(summary?.open_critical_findings || 0) + (summary?.open_high_findings || 0)}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                <Chip label={`${summary?.open_critical_findings || 0} Crit`} color="error" size="small" />
                <Chip label={`${summary?.open_high_findings || 0} High`} color="warning" size="small" />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ASPMDashboard;
