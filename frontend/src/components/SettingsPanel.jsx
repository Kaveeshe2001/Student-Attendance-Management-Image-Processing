import React from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Slider, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel, 
  FormControlLabel, 
  Checkbox, 
  Button, 
  Divider 
} from '@mui/material';

export default function SettingsPanel({ config, setConfig }) {
  const handleChange = (field, value) => {
    setConfig(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        borderRadius: '16px',
        border: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        gap: 3,
        bgcolor: 'background.paper',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.05)'
      }}
    >
      <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'text.primary' }}>
        SAMS Configuration Panel
      </Typography>
      <Divider />

      {/* OCR ENGINE SELECTOR */}
      <Box>
        <FormControl fullWidth size="small">
          <InputLabel>OCR Engine Provider</InputLabel>
          <Select
            value={config.ocrProvider}
            label="OCR Engine Provider"
            onChange={(e) => handleChange('ocrProvider', e.target.value)}
          >
            <MenuItem value="tesseract">Tesseract OCR (Local Executable)</MenuItem>
            <MenuItem value="google-vision">Google Cloud Vision API (Remote)</MenuItem>
            <MenuItem value="azure-di">Azure Document Intelligence (Remote)</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* CONFIDENCE SLIDER */}
      <Box>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 1, color: 'text.primary' }}>
          OCR Confidence Threshold ({Math.round(config.confidenceThreshold * 100)}%)
        </Typography>
        <Slider
          value={config.confidenceThreshold}
          min={0.1}
          max={1.0}
          step={0.05}
          onChange={(e, val) => handleChange('confidenceThreshold', val)}
          valueLabelFormat={(val) => `${Math.round(val * 100)}%`}
          valueLabelDisplay="auto"
        />
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          Minimum confidence score required for an OCR read to match student database names automatically without manual review.
        </Typography>
      </Box>

      {/* SIGNATURE SLIDER */}
      <Box>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 1, color: 'text.primary' }}>
          Signature Detection Ink Threshold ({(config.sigThreshold * 100).toFixed(1)}%)
        </Typography>
        <Slider
          value={config.sigThreshold}
          min={0.01}
          max={0.20}
          step={0.01}
          onChange={(e, val) => handleChange('sigThreshold', val)}
          valueLabelFormat={(val) => `${(val * 100).toFixed(1)}%`}
          valueLabelDisplay="auto"
        />
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          Minimum ratio of dark pixels in a signature bounding box required to classify a student as "Present". Bypassed in fallback positioning mode.
        </Typography>
      </Box>

      <Divider />

      {/* OTHER CHECKBOXES */}
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        <FormControlLabel
          control={
            <Checkbox
              checked={config.saveProcessedImages}
              onChange={(e) => handleChange('saveProcessedImages', e.target.checked)}
            />
          }
          label="Save intermediate processed images in results/"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={config.enableDebugLogs}
              onChange={(e) => handleChange('enableDebugLogs', e.target.checked)}
            />
          }
          label="Enable pipeline debug logs & metrics console"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={config.useFallbackMatching}
              onChange={(e) => handleChange('useFallbackMatching', e.target.checked)}
            />
          }
          label="Enable automatic positional cell matcher fallback"
        />
      </Box>

      <Button variant="contained" color="primary" sx={{ borderRadius: '8px', fontWeight: 600, mt: 2 }}>
        Apply & Save Settings
      </Button>
    </Paper>
  );
}
