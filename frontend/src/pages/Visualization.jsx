import React, { useState, useEffect } from 'react';
import { Box, Tab, Tabs, Typography, Paper, CircularProgress } from '@mui/material';
import ImageComparison from '../components/ImageComparison';
import ImageViewer from '../components/ImageViewer';
import axios from 'axios';

export default function Visualization({ imageFile, sessionId }) {
  const [activeTab, setActiveTab] = useState(0);
  const [visuals, setVisuals] = useState(null);
  const [loading, setLoading] = useState(false);
  const [timeKey, setTimeKey] = useState(new Date().getTime());

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  useEffect(() => {
    if (!sessionId) {
      setVisuals(null);
      return;
    }

    setLoading(true);
    // Unique timestamp cache-busting configuration
    const timestamp = new Date().getTime();
    setTimeKey(timestamp);

    axios.get(`/api/visualizations/${sessionId}`, {
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Expires': '0'
      },
      params: {
        t: timestamp
      }
    })
    .then(res => {
      setVisuals(res.data);
      setLoading(false);
    })
    .catch(err => {
      console.error("Failed to load visual maps:", err);
      setLoading(false);
    });
  }, [sessionId]);

  const getImgUrl = (path) => {
    if (!path) return null;
    // Add cache buster query parameter
    return `${path}?t=${timeKey}`;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

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

      {!imageFile || !sessionId || !visuals ? (
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
              <Tab label="Grid vs Cells" />
              <Tab label="OCR Overlay" />
              <Tab label="Signature Detection Overlay" />
              <Tab label="Attendance Overlay" />
            </Tabs>
          </Paper>

          {/* Render Active Visual Comparison */}
          {activeTab === 0 && (
            <ImageComparison
              beforeSrc={getImgUrl(visuals.original)}
              afterSrc={getImgUrl(visuals.perspective)}
              beforeTitle="Raw Scan Page"
              afterTitle="Corrected Document Bounding Area"
            />
          )}

          {activeTab === 1 && (
            <ImageComparison
              beforeSrc={getImgUrl(visuals.perspective)}
              afterSrc={getImgUrl(visuals.threshold)}
              beforeTitle="Corrected RGB table"
              afterTitle="High Contrast Binary Details"
            />
          )}

          {activeTab === 2 && (
            <ImageComparison
              beforeSrc={getImgUrl(visuals.threshold)}
              afterSrc={getImgUrl(visuals.grid)}
              beforeTitle="High Contrast Binary"
              afterTitle="Detected Grid Lines"
            />
          )}

          {activeTab === 3 && (
            <ImageComparison
              beforeSrc={getImgUrl(visuals.grid)}
              afterSrc={getImgUrl(visuals.cells)}
              beforeTitle="Detected Grid Lines"
              afterTitle="Cell Extraction boundary segments overlay"
            />
          )}

          {activeTab === 4 && (
            <ImageViewer
              title="OCR Overlay"
              algoText="Tesseract OCR + Bounding Box mapping"
              description="Displays detected character texts overlaid directly on top of student index number columns."
              src={getImgUrl(visuals.ocr)}
            />
          )}

          {activeTab === 5 && (
            <ImageViewer
              title="Signature Detection Bounding Boxes"
              algoText="Signature Bounding Box Crop + Ink Density"
              description="Displays student signature crops side-by-side with computed ink ratios."
              src={getImgUrl(visuals.signature)}
            />
          )}

          {activeTab === 6 && (
            <ImageViewer
              title="Final Attendance Overlay"
              algoText="Attendance Decision Matrix Overlay"
              description="Visualizes final student attendance statuses (Present/Absent/Review) mapped on the document."
              src={getImgUrl(visuals.attendance)}
            />
          )}
        </Box>
      )}
    </Box>
  );
}
