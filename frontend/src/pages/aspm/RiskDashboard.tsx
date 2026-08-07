import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent,
  LinearProgress,
  Chip
} from '@mui/material';

interface Application {
  id: string;
  name: string;
}

interface ApplicationRisk {
  overall_risk_score: number;
  critical_findings_count: number;
  high_findings_count: number;
}

const RiskDashboard: React.FC = () => {
  const [apps, setApps] = useState<Application[]>([]);
  const [riskData, setRiskData] = useState<Record<string, ApplicationRisk>>({});

  useEffect(() => {
    const fetchAppsAndRisk = async () => {
      try {
        const appsRes = await api.get('/api/v1/aspm/applications');
        const appsList = appsRes.data;
        setApps(appsList);

        const riskPromises = appsList.map((app: Application) => 
          api.get(`/api/v1/aspm/applications/${app.id}/risk`)
        );
        
        const riskResponses = await Promise.allSettled(riskPromises);
        
        const newRiskData: Record<string, ApplicationRisk> = {};
        riskResponses.forEach((res, index) => {
          if (res.status === 'fulfilled') {
            newRiskData[appsList[index].id] = res.value.data;
          }
        });
        
        setRiskData(newRiskData);
      } catch (error) {
        console.error('Error fetching risk data:', error);
      }
    };
    
    fetchAppsAndRisk();
  }, []);

  const getRiskColor = (score: number) => {
    if (score >= 80) return 'error';
    if (score >= 50) return 'warning';
    return 'success';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Application Risk Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {apps.map(app => {
          const risk = riskData[app.id];
          if (!risk) return null;
          
          return (
            <Grid item xs={12} md={6} key={app.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>{app.name}</Typography>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    Overall Risk Score
                  </Typography>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ width: '100%', mr: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={risk.overall_risk_score} 
                        color={getRiskColor(risk.overall_risk_score)}
                      />
                    </Box>
                    <Box sx={{ minWidth: 35 }}>
                      <Typography variant="body2" color="textSecondary">
                        {Math.round(risk.overall_risk_score)}
                      </Typography>
                    </Box>
                  </Box>
                  
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip label={`${risk.critical_findings_count} Critical`} color="error" size="small" />
                    <Chip label={`${risk.high_findings_count} High`} color="warning" size="small" />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
};

export default RiskDashboard;
