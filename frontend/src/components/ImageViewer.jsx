import React, { useState } from 'react';
import { Box, Typography, Button, IconButton, Paper } from '@mui/material';
import {
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
  RotateRight as RotateIcon,
  Fullscreen as FullscreenIcon,
  SettingsBackupRestore as ResetIcon,
  GetApp as DownloadIcon
} from '@mui/icons-material';

export default function ImageViewer({ src, title, description, timeText, algoText }) {
  const [scale, setScale] = useState(1);
  const [rotation, setRotation] = useState(0);

  const handleZoomIn = () => setScale(prev => Math.min(prev + 0.25, 4));
  const handleZoomOut = () => setScale(prev => Math.max(prev - 0.25, 0.5));
  const handleRotate = () => setRotation(prev => (prev + 90) % 360);
  const handleReset = () => {
    setScale(1);
    setRotation(0);
  };

  const handleDownload = () => {
    if (!src) return;
    const a = document.createElement('a');
    a.href = src;
    a.download = (title || 'image') + '.png';
    a.click();
  };

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
        gap: 1.5,
        bgcolor: 'background.paper',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          <Typography variant="subtitle2" sx={{ fontWeight: 700, color: 'text.primary' }}>
            {title}
          </Typography>
          {algoText && (
            <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block', mt: 0.2 }}>
              Algorithm: {algoText} {timeText && `• ${timeText}`}
            </Typography>
          )}
        </Box>
        <IconButton size="small" onClick={handleDownload} disabled={!src} sx={{ color: 'text.secondary' }}>
          <DownloadIcon />
        </IconButton>
      </Box>

      {/* VIEWPORT AREA */}
      <Box
        sx={{
          height: 320,
          bgcolor: '#070a13',
          borderRadius: '12px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          overflow: 'hidden',
          border: '1px solid',
          borderColor: 'divider'
        }}
      >
        {src ? (
          <img
            src={src}
            alt={title}
            style={{
              maxHeight: '100%',
              maxWidth: '100%',
              objectFit: 'contain',
              transform: `scale(${scale}) rotate(${rotation}deg)`,
              transition: 'transform 0.15s ease',
              cursor: 'grab'
            }}
          />
        ) : (
          <Typography sx={{ color: 'text.disabled', fontStyle: 'italic', fontSize: '0.85rem' }}>
            No image generated. Process document to inspect.
          </Typography>
        )}

        {/* IMAGE CONTROLS */}
        {src && (
          <Box
            sx={{
              position: 'absolute',
              bottom: 12,
              left: '50%',
              transform: 'translateX(-50%)',
              bgcolor: 'rgba(15, 23, 42, 0.85)',
              backdropFilter: 'blur(10px)',
              borderRadius: '20px',
              px: 1.5,
              py: 0.5,
              display: 'flex',
              gap: 1.5,
              border: '1px solid rgba(255, 255, 255, 0.1)',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)'
            }}
          >
            <IconButton size="small" onClick={handleZoomIn} sx={{ color: '#ffffff', '&:hover': { color: '#3b82f6' } }}>
              <ZoomInIcon fontSize="small" />
            </IconButton>
            <IconButton size="small" onClick={handleZoomOut} sx={{ color: '#ffffff', '&:hover': { color: '#3b82f6' } }}>
              <ZoomOutIcon fontSize="small" />
            </IconButton>
            <IconButton size="small" onClick={handleRotate} sx={{ color: '#ffffff', '&:hover': { color: '#3b82f6' } }}>
              <RotateIcon fontSize="small" />
            </IconButton>
            <IconButton size="small" onClick={handleReset} sx={{ color: '#ffffff', '&:hover': { color: '#3b82f6' } }}>
              <ResetIcon fontSize="small" />
            </IconButton>
          </Box>
        )}
      </Box>

      {description && (
        <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block', mt: 0.5, lineHeight: 1.3 }}>
          {description}
        </Typography>
      )}
    </Paper>
  );
}
