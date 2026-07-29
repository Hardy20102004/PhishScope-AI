import React from 'react';
import { 
  Box, 
  Typography, 
  Alert
} from '@mui/material';

export const SecurityGatesDashboard: React.FC = () => {

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Security Gates
      </Typography>
      
      <Alert severity="info">
        This view displays security guardrails (SAST, DAST, SCA, Secrets) enforced during CI/CD execution.
      </Alert>
    </Box>
  );
};
