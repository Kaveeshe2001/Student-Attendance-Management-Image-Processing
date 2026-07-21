import React from 'react';
import { Box, Typography } from '@mui/material';
import SettingsPanel from '../components/SettingsPanel';

export default function Settings({ config, setConfig }) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Box>
        <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary' }}>
          System Configuration
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Adjust character classification parameters, signature threshold tolerances, theme modes, and debugger preferences.
        </Typography>
      </Box>

      <SettingsPanel config={config} setConfig={setConfig} />
    </Box>
  );
}
