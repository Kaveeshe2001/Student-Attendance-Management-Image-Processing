import React from 'react';
import { Box, Typography, Paper, LinearProgress } from '@mui/material';

const pipelineStages = [
  "Image Loading",
  "Perspective Correction",
  "Grayscale",
  "Enhancement",
  "Threshold",
  "Table Detection",
  "Cell Extraction",
  "OCR",
  "Student Matching",
  "Signature Detection",
  "Attendance Decision",
  "XML Merge",
  "Completed"
];

export default function ProgressPipeline({ activeStep, statusText }) {
  const percent = activeStep === -1 ? 0 : Math.round(((activeStep + 1) / pipelineStages.length) * 100);

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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'text.primary' }}>
          AI Document Analysis Pipeline
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 500, fontSize: '0.8rem' }}>
          {statusText || "Ready to process"}
        </Typography>
      </Box>

      {/* HORIZONTAL PROGRESS BAR */}
      <Box sx={{ width: '100%', position: 'relative' }}>
        <LinearProgress 
          variant="determinate" 
          value={percent} 
          sx={{
            height: 6,
            borderRadius: 3,
            bgcolor: 'action.hover',
            '& .MuiLinearProgress-bar': {
              borderRadius: 3,
              background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)'
            }
          }}
        />
      </Box>

      {/* PIPELINE STAGES TIMELINE */}
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          position: 'relative',
          overflowX: 'auto',
          pb: 1,
          pt: 1,
          gap: 2
        }}
      >
        {pipelineStages.map((stage, idx) => {
          const isActive = idx === activeStep;
          const isCompleted = idx < activeStep;
          
          return (
            <Box 
              key={stage} 
              sx={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center',
                flexShrink: 0,
                minWidth: 70,
                position: 'relative'
              }}
            >
              {/* Node Circle */}
              <Box
                sx={{
                  width: 32,
                  height: 32,
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  border: '3px solid',
                  transition: 'all 0.3s ease',
                  borderColor: isCompleted ? '#10b981' : isActive ? 'primary.main' : 'divider',
                  bgcolor: isCompleted ? '#10b981' : isActive ? 'primary.light' : 'background.paper',
                  color: isCompleted ? '#ffffff' : isActive ? 'primary.main' : 'text.disabled',
                  boxShadow: isActive ? '0 0 10px rgba(59, 130, 246, 0.4)' : 'none'
                }}
              >
                {idx + 1}
              </Box>
              
              {/* Label */}
              <Typography 
                variant="caption" 
                sx={{ 
                  fontSize: '0.7rem', 
                  fontWeight: 600, 
                  color: isCompleted ? 'text.primary' : isActive ? 'primary.main' : 'text.disabled',
                  marginTop: 1,
                  textAlign: 'center',
                  maxWidth: 80,
                  lineHeight: 1.1
                }}
              >
                {stage}
              </Typography>
            </Box>
          );
        })}
      </Box>
    </Paper>
  );
}
