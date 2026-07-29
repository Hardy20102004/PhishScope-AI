import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  TextField, 
  Button,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';

export const DeveloperAssistantPanel: React.FC = () => {
  const [messages, setMessages] = useState<{role: string, content: string}[]>([
    { role: 'SYSTEM', content: 'Enterprise AI Security Copilot connected. Context: payment-service/src/payment.py' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    
    // Add user message
    const newMessages = [...messages, { role: 'USER', content: input }];
    setMessages(newMessages);
    setInput('');

    // Mock AI response demonstrating explainability and human-governed interaction
    setTimeout(() => {
      setMessages(prev => [
        ...prev, 
        { 
          role: 'ASSISTANT', 
          content: 'I analyzed the SQL query you just wrote. It appears vulnerable to SQL Injection (CWE-89) because it concatenates user input directly into the query string. I recommend using SQLAlchemy parameterized queries. Shall I generate a suggested diff for your review?'
        }
      ]);
    }, 1000);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600, margin: '0 auto' }}>
      <Typography variant="h5" gutterBottom>
        Developer Assistant (IDE Simulation)
      </Typography>
      
      <Paper sx={{ height: 400, overflowY: 'auto', p: 2, mb: 2, display: 'flex', flexDirection: 'column' }}>
        <List>
          {messages.map((msg, idx) => (
            <React.Fragment key={idx}>
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary={
                    <Typography 
                      component="span" 
                      variant="subtitle2" 
                      color={msg.role === 'USER' ? 'primary' : (msg.role === 'SYSTEM' ? 'textSecondary' : 'secondary')}
                    >
                      {msg.role}
                    </Typography>
                  }
                  secondary={msg.content}
                />
              </ListItem>
              {idx < messages.length - 1 && <Divider component="li" />}
            </React.Fragment>
          ))}
        </List>
      </Paper>

      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask Copilot for code review or architectural guidance..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <Button variant="contained" color="primary" onClick={handleSend}>
          Send
        </Button>
      </Box>
    </Box>
  );
};
