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

interface SASTSummary {
  total_scans: number;
  critical_findings: number;
  high_findings: number;
  average_lines_scanned: number;
}

export const SASTExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<SASTSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/sast/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching SAST summary:', error);
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
        SAST Executive Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Scans
              </Typography>
              <Typography variant="h3">{summary?.total_scans || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical Findings
              </Typography>
              <Typography variant="h3" color="error">{summary?.critical_findings || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
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
                Avg Lines Scanned
              </Typography>
              <Typography variant="h3" color="primary">
                {summary?.average_lines_scanned ? summary.average_lines_scanned.toLocaleString() : 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
