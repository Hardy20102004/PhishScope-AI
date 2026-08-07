import React from 'react';
import { 
  Box, 
  Typography, 
  Alert,
  Paper
} from '@mui/material';

export const PackageIntelligenceDashboard: React.FC = () => {

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Open Source Package Intelligence
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        This dashboard aggregates global threat intelligence and community health metrics for specific open source components (e.g. maintainer activity, abandonment probability).
      </Alert>
      
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>Example Insights</Typography>
        <Typography variant="body1" paragraph>
          <strong>NPM 'request' package:</strong> Detected as abandoned and deprecated. The AI guidance recommends replacing with 'axios' or native fetch API.
        </Typography>
      </Paper>
    </Box>
  );
};
