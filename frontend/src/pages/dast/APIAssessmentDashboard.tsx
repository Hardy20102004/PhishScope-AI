import React from 'react';
import { 
  Box, 
  Typography, 
  Alert,
  Paper
} from '@mui/material';

export const APIAssessmentDashboard: React.FC = () => {

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        API Security Assessment
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        This module provides specialized insights for REST, GraphQL, and SOAP API testing, including coverage mapping to the OWASP API Security Top 10.
      </Alert>
      
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>Fuzzing Coverage</Typography>
        <Typography variant="body1" paragraph>
          Dynamic fuzzing is currently assessing endpoints for Broken Object Level Authorization (BOLA), mass assignment, and improper asset management.
        </Typography>
      </Paper>
    </Box>
  );
};
