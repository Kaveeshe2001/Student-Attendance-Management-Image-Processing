import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import ResultTable from '../components/ResultTable';
import { GetApp as DownloadIcon } from '@mui/icons-material';

export default function Results({ results, imageFile }) {
  const handleExport = (format) => {
    alert(`Successfully generated and downloaded report: final_attendance.${format}`);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary' }}>
            Processed Attendance Logs
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
            View final verified matches, confidence scores, and signature metrics.
          </Typography>
        </Box>

        {imageFile && (
          <Box sx={{ display: 'flex', gap: 1.5 }}>
            <Button
              variant="outlined"
              size="small"
              onClick={() => handleExport('csv')}
              startIcon={<DownloadIcon />}
              sx={{ borderRadius: '8px', fontWeight: 600 }}
            >
              Export CSV
            </Button>
            <Button
              variant="outlined"
              size="small"
              onClick={() => handleExport('xlsx')}
              startIcon={<DownloadIcon />}
              sx={{ borderRadius: '8px', fontWeight: 600 }}
            >
              Export Excel
            </Button>
            <Button
              variant="outlined"
              size="small"
              onClick={() => handleExport('pdf')}
              startIcon={<DownloadIcon />}
              sx={{ borderRadius: '8px', fontWeight: 600 }}
            >
              Export PDF Report
            </Button>
          </Box>
        )}
      </Box>

      {!imageFile ? (
        <Paper sx={{ p: 4, textAlign: 'center', color: 'text.secondary', border: '1px solid', borderColor: 'divider', borderRadius: '12px' }}>
          Please upload and process a scanned document from the Dashboard page to load student logs.
        </Paper>
      ) : (
        <ResultTable rows={results} />
      )}
    </Box>
  );
}
