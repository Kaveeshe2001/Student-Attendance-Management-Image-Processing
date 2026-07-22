import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import ResultTable from '../components/ResultTable';
import { GetApp as DownloadIcon } from '@mui/icons-material';

export default function Results({ results, imageFile, sessionId }) {
  const handleExport = (format) => {
    if (format === 'csv') {
      const headers = ['Student ID', 'Student Name', 'Status', 'Confidence', 'Ink Ratio', 'Requires Review'];
      const csvRows = results.map(r => [
        r.student_id,
        r.student_name,
        r.status,
        Number(r.confidence).toFixed(2) + '%',
        r.ink_ratio.toFixed(4),
        r.requires_review ? 'Yes' : 'No'
      ]);

      const csvContent = [
        headers.join(','),
        ...csvRows.map(row => row.map(val => `"${val.replace(/"/g, '""')}"`).join(','))
      ].join('\n');

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute("download", `sams_attendance_report_${sessionId || 'export'}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      alert(`Report generated in ${format.toUpperCase()} format.`);
    }
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
