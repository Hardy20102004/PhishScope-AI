import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { 
  Box, 
  Typography, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper,
  Chip,
  Button
} from '@mui/material';

interface DeploymentGovernance {
  id: string;
  template_id: string;
  status: string;
  requested_by: string;
  risk_score: number;
  created_at: string;
}

export const DeploymentGovernanceDashboard: React.FC = () => {
  const [deployments, setDeployments] = useState<DeploymentGovernance[]>([]);

  useEffect(() => {
    // In a real app we'd fetch actual deployments. Using static state for demonstration of approval flow.
    const mockDeployments = [
      {
        id: 'c8e1e75a-f111-4195-a45b-7b0b230fcd12',
        template_id: 'a123',
        status: 'PENDING_APPROVAL',
        requested_by: 'DevOps User',
        risk_score: 85.0,
        created_at: new Date().toISOString()
      },
      {
        id: 'd9e2e86b-f222-4206-b56c-8c1c341fde23',
        template_id: 'b456',
        status: 'APPROVED',
        requested_by: 'System Admin',
        risk_score: 15.0,
        created_at: new Date().toISOString()
      }
    ];
    setDeployments(mockDeployments);
  }, []);

  const handleApprove = async (id: string) => {
    try {
      // In a real app, this would hit /api/v1/iac/deployments/{id}/approve
      setDeployments(deployments.map(d => 
        d.id === id ? { ...d, status: 'APPROVED' } : d
      ));
    } catch (error) {
      console.error('Failed to approve deployment', error);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Deployment Governance & Approvals
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Deployment ID</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Risk Score</TableCell>
              <TableCell>Requested At</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {deployments.map((deployment) => (
              <TableRow key={deployment.id}>
                <TableCell sx={{ fontFamily: 'monospace' }}>{deployment.id.substring(0, 8)}...</TableCell>
                <TableCell>
                  <Chip 
                    label={deployment.status} 
                    size="small" 
                    color={deployment.status === 'APPROVED' ? 'success' : 'warning'} 
                  />
                </TableCell>
                <TableCell>
                  <Typography color={deployment.risk_score > 80 ? 'error' : 'textPrimary'}>
                    {deployment.risk_score}
                  </Typography>
                </TableCell>
                <TableCell>{new Date(deployment.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  {deployment.status === 'PENDING_APPROVAL' && (
                    <Button 
                      variant="contained" 
                      color="primary" 
                      size="small"
                      onClick={() => handleApprove(deployment.id)}
                    >
                      Approve Release
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
