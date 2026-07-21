import React, { useEffect, useRef } from 'react';
import { Box, Typography, Paper } from '@mui/material';

export default function ProcessingLog({ logs }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [logs]);

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
      <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'text.primary' }}>
        Real-time Processing Logs
      </Typography>

      <Box
        ref={containerRef}
        sx={{
          bgcolor: '#070a13',
          borderRadius: '12px',
          p: 2,
          height: 300,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: 0.5,
          fontFamily: 'Consolas, Monaco, monospace',
          fontSize: '0.8rem',
          border: '1px solid rgba(255, 255, 255, 0.05)',
        }}
      >
        {logs.map((log, index) => {
          let color = '#38bdf8'; // Default info: blue
          if (log.includes('[WARNING]')) {
            color = '#fbbf24'; // Warning: orange
          } else if (log.includes('[ERROR]') || log.includes('failed')) {
            color = '#f87171'; // Error: red
          } else if (log.includes('[SUCCESS]')) {
            color = '#34d399'; // Success: green
          }

          return (
            <Typography
              key={index}
              sx={{
                color: color,
                fontFamily: 'inherit',
                fontSize: 'inherit',
                lineHeight: 1.4,
                whiteSpace: 'pre-wrap'
              }}
            >
              {log}
            </Typography>
          );
        })}
        {logs.length === 0 && (
          <Typography sx={{ color: '#64748b', fontStyle: 'italic', fontFamily: 'inherit', fontSize: 'inherit' }}>
            System ready. Waiting for input sheets...
          </Typography>
        )}
      </Box>
    </Paper>
  );
}
