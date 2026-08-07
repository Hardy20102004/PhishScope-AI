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

interface IaCSummary {
  total_templates: number;
  critical_findings: number;
  pending_deployments: number;
  blocked_deployments: number;
}

export const IaCExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<IaCSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/iac/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching IaC summary:', error);
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
        IaC Security & Configuration Governance
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Templates Analyzed
              </Typography>
              <Typography variant="h3">{summary?.total_templates || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical Misconfigurations
              </Typography>
              <Typography variant="h3" color="error">{summary?.critical_findings || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending Deployments
              </Typography>
              <Typography variant="h3" color="primary">{summary?.pending_deployments || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Blocked Deployments
              </Typography>
              <Typography variant="h3" color="error.light">{summary?.blocked_deployments || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
