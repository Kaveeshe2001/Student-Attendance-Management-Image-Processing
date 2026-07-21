import React, { useState, useEffect } from 'react';
import { Box, Grid, Typography, Paper, CircularProgress } from '@mui/material';
import ImageViewer from '../components/ImageViewer';
import axios from 'axios';

const analysisStagesMeta = [
  { id: 'original', title: '1. Original Image', algo: 'Direct Scanner Upload', desc: 'Raw RGB document image loaded from the user file upload.' },
  { id: 'perspective', title: '2. Perspective Corrected', algo: 'Perspective Transformation', desc: 'Table borders detected and warped to a standard rect contour area.' },
  { id: 'grayscale', title: '3. Grayscale conversion', algo: 'cv2.cvtColor (COLOR_BGR2GRAY)', desc: 'Luminance conversion mapping pixel colors to 8-bit grayscales.' },
  { id: 'threshold', title: '4. Threshold Binarization', algo: 'Adaptive Gaussian Thresholding', desc: 'Binarizes grayscale image to 0 (black background) & 255 (white details).' },
  { id: 'table', title: '5. Detected Table', algo: 'Contour Analysis', desc: 'Isolates the external bounding boundary contour of the sheet.' },
  { id: 'grid', title: '6. Detected Grid Lines', algo: 'Morphological Line Separators', desc: 'Extracts cleanly reconstructed horizontal & vertical grid lines.' },
  { id: 'cells', title: '7. Extracted Cells', algo: 'Grid Splitting Intersections', desc: 'Isolates individual table sub-cells based on grid intersections.' },
  { id: 'ocr', title: '8. OCR Bounding Boxes', algo: 'Tesseract OCR Engine', desc: 'Recognizes student registration ID characters inside ID columns.' },
  { id: 'signature', title: '9. Signatures Isolated', algo: 'Row Percentage Fallback', desc: 'Isolates cropped signature cells based on student row percentages.' },
  { id: 'attendance', title: '10. Attendance Overlay', algo: 'Ink Ratio Classifier Verdict', desc: 'Determines attendance status based on signature ink density threshold.' }
];

export default function Analysis({ imageFile, sessionId }) {
  const [visuals, setVisuals] = useState(null);
  const [loading, setLoading] = useState(false);
  const [timeKey, setTimeKey] = useState(new Date().getTime());

  useEffect(() => {
    if (!sessionId) {
      setVisuals(null);
      return;
    }

    setLoading(true);
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
      console.error("Failed to load pipeline stages for analysis:", err);
      setLoading(false);
    });
  }, [sessionId]);

  const getImgUrl = (path) => {
    if (!path) return null;
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
          Pipeline Stage Analysis
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Inspect the input image at every step of SAMS's threshold and computer vision pipelines.
        </Typography>
      </Box>

      {!imageFile || !sessionId || !visuals ? (
        <Paper sx={{ p: 4, textAlign: 'center', color: 'text.secondary', border: '1px solid', borderColor: 'divider', borderRadius: '12px' }}>
          Please upload and process a scanned document from the Dashboard page to analyze pipeline stages.
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {analysisStagesMeta.map((stage) => {
            const imgSrc = getImgUrl(visuals[stage.id]);
            if (!imgSrc) return null;
            return (
              <Grid item xs={12} sm={6} md={4} key={stage.id}>
                <ImageViewer
                  title={stage.title}
                  algoText={stage.algo}
                  description={stage.desc}
                  src={imgSrc}
                />
              </Grid>
            );
          })}
        </Grid>
      )}
    </Box>
  );
}
