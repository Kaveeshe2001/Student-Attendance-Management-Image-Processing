import React, { useEffect, useState } from 'react';
import { Box, Typography, IconButton, useTheme } from '@mui/material';
import {
  Brightness4 as DarkModeIcon,
  Brightness7 as LightModeIcon,
  AccessTime as TimeIcon
} from '@mui/icons-material';

export default function Header({ toggleColorMode, mode }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const dateString = time.toLocaleDateString(undefined, options);
  const timeString = time.toTimeString().split(' ')[0];

  return (
    <Box
      sx={{
        height: 70,
        bgcolor: 'background.paper',
        borderBottom: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        px: 3,
        flexShrink: 0
      }}
    >
      <Box>
        <Typography variant="h6" sx={{ fontWeight: 700, color: 'text.primary', fontSize: '1.25rem' }}>
          Student Attendance Management System (SAMS)
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', fontSize: '0.8rem' }}>
          AI Powered Attendance Recognition & Document Analysis
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, textAlign: 'right' }}>
          <TimeIcon sx={{ color: 'text.secondary', fontSize: 18 }} />
          <Typography variant="body2" sx={{ fontWeight: 500, color: 'text.primary', fontSize: '0.85rem' }}>
            {dateString} <span style={{ color: '#3b82f6', marginLeft: 6 }}>{timeString}</span>
          </Typography>
        </Box>

        <IconButton onClick={toggleColorMode} color="inherit" sx={{ border: '1px solid', borderColor: 'divider', borderRadius: '8px' }}>
          {mode === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
        </IconButton>
      </Box>
    </Box>
  );
}
