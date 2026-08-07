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

interface SBOMSummary {
  total_sboms: number;
  total_artifacts: number;
  total_dependencies: number;
  unverified_provenance: number;
  average_supply_chain_score: number;
}

export const SBOMExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<SBOMSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/api/v1/sbom/executive-summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching SBOM summary:', error);
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
        Software Supply Chain Executive Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total SBOMs
              </Typography>
              <Typography variant="h3">{summary?.total_sboms || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Artifacts
              </Typography>
              <Typography variant="h3">{summary?.total_artifacts || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
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
                Unverified Provenance
              </Typography>
              <Typography variant="h3" color="error">{summary?.unverified_provenance || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg Score
              </Typography>
              <Typography variant="h3" color="primary">{summary?.average_supply_chain_score || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
