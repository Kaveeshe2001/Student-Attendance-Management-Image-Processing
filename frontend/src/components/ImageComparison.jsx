import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

export default function ImageComparison({ beforeSrc, afterSrc, beforeTitle, afterTitle }) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
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
        Side-by-Side Image Processing Comparison
      </Typography>

      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 2,
          height: 380
        }}
      >
        {/* BEFORE PANEL */}
        <Box
          sx={{
            bgcolor: '#070a13',
            borderRadius: '12px',
            border: '1px solid',
            borderColor: 'divider',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              top: 10,
              left: 10,
              bgcolor: 'rgba(0, 0, 0, 0.5)',
              color: '#ffffff',
              px: 1.5,
              py: 0.5,
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: 600,
              zIndex: 10
            }}
          >
            {beforeTitle || "Original Input"}
          </Box>
          {beforeSrc ? (
            <img src={beforeSrc} alt="before" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          ) : (
            <Typography sx={{ color: 'text.disabled', fontStyle: 'italic', fontSize: '0.85rem' }}>
              No image.
            </Typography>
          )}
        </Box>

        {/* AFTER PANEL */}
        <Box
          sx={{
            bgcolor: '#070a13',
            borderRadius: '12px',
            border: '1px solid',
            borderColor: 'divider',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifycontent: 'center'
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              top: 10,
              left: 10,
              bgcolor: 'rgba(0, 0, 0, 0.5)',
              color: '#ffffff',
              px: 1.5,
              py: 0.5,
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: 600,
              zIndex: 10
            }}
          >
            {afterTitle || "Warp Corrected"}
          </Box>
          {afterSrc ? (
            <img src={afterSrc} alt="after" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          ) : (
            <Typography sx={{ color: 'text.disabled', fontStyle: 'italic', fontSize: '0.85rem' }}>
              No image.
            </Typography>
          )}
        </Box>
      </Box>
    </Paper>
  );
}
