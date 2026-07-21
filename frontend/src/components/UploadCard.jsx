import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, Button, Paper } from '@mui/material';
import { CloudUpload as UploadIcon, CheckCircle as CheckIcon, Cancel as ErrorIcon } from '@mui/icons-material';

export default function UploadCard({ accept, title, subtitle, onFileSelect, file, fileType }) {
  const [loading, setLoading] = useState(false);
  const [dimensions, setDimensions] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0];
      
      // Calculate image dimensions if it is an image
      if (selectedFile.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = new Image();
          img.onload = () => {
            setDimensions({ width: img.width, height: img.height });
            onFileSelect({
              file: selectedFile,
              preview: e.target.result,
              width: img.width,
              height: img.height,
              size: (selectedFile.size / 1024 / 1024).toFixed(2) + ' MB'
            });
          };
          img.src = e.target.result;
        };
        reader.readAsDataURL(selectedFile);
      } else {
        onFileSelect({
          file: selectedFile,
          size: (selectedFile.size / 1024).toFixed(1) + ' KB'
        });
      }
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: accept,
    multiple: false
  });

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
        gap: 2,
        bgcolor: 'background.paper',
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'text.primary' }}>
          {title}
        </Typography>
      </Box>

      {/* DROPZONE */}
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'divider',
          borderRadius: '12px',
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          bgcolor: isDragActive ? 'action.hover' : 'background.default',
          transition: 'all 0.2s ease',
          '&:hover': {
            borderColor: 'primary.main',
            bgcolor: 'action.hover'
          }
        }}
      >
        <input {...getInputProps()} />
        <UploadIcon sx={{ fontSize: 44, color: 'primary.main', mb: 1.5 }} />
        <Typography variant="body1" sx={{ fontWeight: 600, color: 'text.primary', mb: 0.5 }}>
          {isDragActive ? "Drop the file here" : subtitle}
        </Typography>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          Supported file formats: {Object.values(accept).flat().join(', ')}
        </Typography>
      </Box>

      {/* FILE INFO META */}
      {file && (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 2,
            p: 1.5,
            borderRadius: '10px',
            bgcolor: 'background.default',
            border: '1px solid',
            borderColor: 'divider'
          }}
        >
          {file.preview ? (
            <img 
              src={file.preview} 
              alt="Thumbnail" 
              style={{ width: 48, height: 48, borderRadius: 6, objectFit: 'cover', border: '1px solid var(--mui-palette-divider)' }} 
            />
          ) : (
            <Box 
              sx={{ 
                width: 48, 
                height: 48, 
                borderRadius: '6px', 
                bgcolor: 'rgba(16, 185, 129, 0.1)', 
                color: '#10b981',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <CheckIcon />
            </Box>
          )}

          <Box sx={{ flexGrow: 1, overflow: 'hidden' }}>
            <Typography variant="body2" sx={{ fontWeight: 600, color: 'text.primary', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {file.file.name}
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block' }}>
              {file.size} {file.width && `• ${file.width} x ${file.height} px`}
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <CheckIcon sx={{ color: '#10b981', fontSize: 18 }} />
            <Typography variant="caption" sx={{ color: '#10b981', fontWeight: 600 }}>
              Loaded
            </Typography>
          </Box>
        </Box>
      )}
    </Paper>
  );
}
