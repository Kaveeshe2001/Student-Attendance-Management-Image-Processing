import React, { useState } from 'react';
import { Box, Tab, Tabs, Typography, Paper } from '@mui/material';
import ImageComparison from '../components/ImageComparison';
import ImageViewer from '../components/ImageViewer';

export default function Visualization({ imageFile }) {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const generateMockSrc = (label) => {
    if (!imageFile) return null;
    const canvas = document.createElement('canvas');
    canvas.width = 600;
    canvas.height = 300;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, 600, 300);
    ctx.fillStyle = '#38bdf8';
    ctx.font = '20px sans-serif';
    ctx.fillText(label, 150, 160);
    return canvas.toDataURL();
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Box>
        <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary' }}>
          Interactive Visual Analytics
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Compare intermediate image pipeline outputs and inspect detected details.
        </Typography>
      </Box>

      {!imageFile ? (
        <Paper sx={{ p: 4, textAlign: 'center', color: 'text.secondary', border: '1px solid', borderColor: 'divider', borderRadius: '12px' }}>
          Please upload and process a scanned document from the Dashboard page to unlock visualization maps.
        </Paper>
      ) : (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {/* Tab Selector */}
          <Paper elevation={0} sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'background.paper', borderRadius: '12px', px: 1 }}>
            <Tabs value={activeTab} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
              <Tab label="Original vs Perspective" />
              <Tab label="Perspective vs Threshold" />
              <Tab label="Threshold vs Grid" />
              <Tab label="Grid vs Cell Extraction" />
              <Tab label="OCR Overlay" />
              <Tab label="Signature Detection Overlay" />
              <Tab label="Attendance Overlay" />
            </Tabs>
          </Paper>

          {/* Render Active Visual Comparison */}
          {activeTab === 0 && (
            <ImageComparison
              beforeSrc={generateMockSrc('Original Raw Scan')}
              afterSrc={generateMockSrc('Perspective Warp Corrected')}
              beforeTitle="Raw Scan Page"
              afterTitle="Corrected Document Bounding Area"
            />
          )}

          {activeTab === 1 && (
            <ImageComparison
              beforeSrc={generateMockSrc('Warped RGB image')}
              afterSrc={generateMockSrc('Threshold Binary Image')}
              beforeTitle="Corrected RGB table"
              afterTitle="High Contrast Binary Details"
            />
          )}

          {activeTab === 2 && (
            <ImageComparison
              beforeSrc={generateMockSrc('Threshold Binary Image')}
              afterSrc={generateMockSrc('Isolated Grid Lines')}
              beforeTitle="High Contrast Binary"
              afterTitle="Detected Grid Lines"
            />
          )}

          {activeTab === 3 && (
            <ImageComparison
              beforeSrc={generateMockSrc('Isolated Grid Lines')}
              afterSrc={generateMockSrc('Warped image with cells boundary grid overlay')}
              beforeTitle="Detected Grid Lines"
              afterTitle="Cell Extraction boundary segments overlay"
            />
          )}

          {activeTab === 4 && (
            <ImageViewer
              title="OCR Overlay"
              algoText="Tesseract OCR + Bounding Box mapping"
              description="Displays detected character texts overlaid directly on top of student index number columns."
              src={generateMockSrc('Corrected image with OCR Bounding Boxes')}
            />
          )}

          {activeTab === 5 && (
            <ImageViewer
              title="Signature Detection Bounding Boxes"
              algoText="Signature Bounding Box Crop + Ink Density"
              description="Displays student signature crops side-by-side with computed ink ratios."
              src={generateMockSrc('Corrected image with Signature Bounding Boxes')}
            />
          )}

          {activeTab === 6 && (
            <ImageViewer
              title="Final Attendance Overlay"
              algoText="Attendance Decision Matrix Overlay"
              description="Visualizes final student attendance statuses (Present/Absent/Review) mapped on the document."
              src={generateMockSrc('Warped image with Final Attendance badges')}
            />
          )}
        </Box>
      )}
    </Box>
  );
}
