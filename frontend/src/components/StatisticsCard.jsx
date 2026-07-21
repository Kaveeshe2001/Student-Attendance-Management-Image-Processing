import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

export default function StatisticsCard({ value, label, borderLeftColor }) {
  return (
    <Card
      elevation={0}
      sx={{
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: '12px',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.05)',
        borderLeft: borderLeftColor ? `4px solid ${borderLeftColor}` : '1px solid var(--mui-palette-divider)',
        textAlign: 'center'
      }}
    >
      <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: 700, 
            color: borderLeftColor || 'text.primary',
            fontSize: '1.75rem' 
          }}
        >
          {value}
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 600, fontSize: '0.75rem', mt: 0.5 }}>
          {label}
        </Typography>
      </CardContent>
    </Card>
  );
}
