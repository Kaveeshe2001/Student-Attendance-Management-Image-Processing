import React from 'react';
import { Paper, Box, Typography } from '@mui/material';

export default function ChartCard({ title, subtitle, children }) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2.5,
        borderRadius: '16px',
        border: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        bgcolor: 'background.paper',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.05)'
      }}
    >
      <Box>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'text.primary' }}>
          {title}
        </Typography>
        {subtitle && (
          <Typography variant="caption" sx={{ color: 'text.secondary' }}>
            {subtitle}
          </Typography>
        )}
      </Box>

      <Box sx={{ width: '100%', height: 260, position: 'relative' }}>
        {children}
      </Box>
    </Paper>
  );
}
