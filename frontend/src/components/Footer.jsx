import React from 'react';
import { Box, Typography } from '@mui/material';

export default function Footer() {
  return (
    <Box
      sx={{
        height: 40,
        bgcolor: 'background.paper',
        borderTop: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        px: 3,
        flexShrink: 0
      }}
    >
      <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 500 }}>
        NSBM Green University • Department of Computer Graphics and Visualization
      </Typography>
      <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 500 }}>
        Project: Student Attendance Management System (SAMS) • Version 1.0
      </Typography>
    </Box>
  );
}
