import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

export default function LoadingOverlay({ active, message }) {
  if (!active) return null;

  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        bgcolor: 'rgba(15, 23, 42, 0.75)',
        backdropFilter: 'blur(10px)',
        zIndex: 9999,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 2,
        color: '#ffffff'
      }}
    >
      <CircularProgress size={60} thickness={4} sx={{ color: '#3b82f6' }} />
      <Typography variant="h6" sx={{ fontWeight: 600, letterSpacing: 0.5 }}>
        {message || "Processing Scan Sheet..."}
      </Typography>
      <Typography variant="body2" sx={{ color: '#8892b0' }}>
        Please wait. Executing CV and threshold pipelines on server.
      </Typography>
    </Box>
  );
}
