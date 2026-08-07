import React from 'react';
import { 
  Box, 
  Typography, 
  Alert
} from '@mui/material';

const PostureDashboard: React.FC = () => {

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Security Posture & Findings
      </Typography>
      
      <Alert severity="info">
        This view displays aggregated findings from SAST, DAST, SCA, and IaC scanning tools.
        Select an application from the Application Inventory to drill down into specific vulnerabilities.
      </Alert>
    </Box>
  );
};

export default PostureDashboard;
