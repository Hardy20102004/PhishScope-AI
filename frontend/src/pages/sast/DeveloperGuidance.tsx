import React from 'react';
import { 
  Box, 
  Typography, 
  Alert,
  Paper
} from '@mui/material';

export const DeveloperGuidance: React.FC = () => {

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        AI Secure Code Assistant & Guidance
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        This module connects findings with the AI Security Brain to generate contextual remediation strategies and code snippets.
      </Alert>
      
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>Example: SQL Injection Remediation</Typography>
        <Typography variant="body1" paragraph>
          <strong>Explanation:</strong> The parameter `userId` is concatenated directly into the SQL query string on line 42 of `query.js`, allowing an attacker to manipulate the statement logic.
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Remediation Steps:</strong> Replace the concatenated string with a parameterized query using prepared statements. This ensures the database driver treats the input strictly as data, neutralizing any injected commands.
        </Typography>
        <Typography variant="body2" sx={{ fontFamily: 'monospace', bgcolor: '#f5f5f5', p: 2, borderRadius: 1 }}>
          {`// Before
const query = "SELECT * FROM users WHERE id = " + req.body.userId;

// After
const query = "SELECT * FROM users WHERE id = $1";
const values = [req.body.userId];
await db.query(query, values);`}
        </Typography>
      </Paper>
    </Box>
  );
};
