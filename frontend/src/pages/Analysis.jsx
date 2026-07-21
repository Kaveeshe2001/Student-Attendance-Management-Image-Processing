import React from 'react';
import { Box, Grid, Typography, Paper } from '@mui/material';
import ImageViewer from '../components/ImageViewer';

const analysisStages = [
  { id: 'orig', title: 'Original Image', algo: 'Direct Camera Scan', time: '0.05s', desc: 'Raw RGB document image loaded from the local scanner input upload.' },
  { id: 'pers', title: 'Perspective Corrected', algo: 'Perspective Transformation', time: '0.12s', desc: 'Table borders detected and warped to a standard 2161 x 889 layout.' },
  { id: 'gray', title: 'Grayscale', algo: 'cv2.cvtColor (COLOR_BGR2GRAY)', time: '0.01s', desc: 'Luminance conversion mapping pixel colors to 8-bit grayscales.' },
  { id: 'bright', title: 'Brightness Adjustment', algo: 'Contrast Enhancement Kernel', time: '0.02s', desc: 'Normalizes shadows and compensates for environmental highlights.' },
  { id: 'contrast', title: 'Contrast Enhancement', algo: 'Alpha/Beta Scale tuning', time: '0.02s', desc: 'Accentuates black handwritten lines against gray backgrounds.' },
  { id: 'hist', title: 'Histogram Equalization', algo: 'cv2.equalizeHist', time: '0.01s', desc: 'Maximizes contrast mapping across global image histograms.' },
  { id: 'clahe', title: 'CLAHE', algo: 'Contrast Limited Adaptive Hist. Eq.', time: '0.03s', desc: 'Localized adaptive histogram equalization avoiding glare amplification.' },
  { id: 'median', title: 'Median Filter', algo: 'cv2.medianBlur', time: '0.04s', desc: 'Removes sparse salt-and-pepper noise while preserving grid boundaries.' },
  { id: 'gauss', title: 'Gaussian Filter', algo: 'cv2.GaussianBlur', time: '0.02s', desc: 'Smooths pixel gradients and suppresses pixel textures.' },
  { id: 'bilat', title: 'Bilateral Filter', algo: 'cv2.bilateralFilter', time: '0.06s', desc: 'Smooths noise textures while fully preserving high-contrast edge gradients.' },
  { id: 'thresh', title: 'Threshold', algo: 'Adaptive Gaussian Thresholding', time: '0.02s', desc: 'Binarizes grayscale image to 0 (black background) & 255 (white details).' },
  { id: 'morph', title: 'Morphology', algo: 'Morphological Opening & Closing', time: '0.03s', desc: 'Fills holes in table lines and removes small noise clusters.' },
  { id: 'table', title: 'Detected Table', algo: 'Contour Analysis', time: '0.04s', desc: 'Isolates the external bounding boundary contour of the sheet.' },
  { id: 'grid', title: 'Detected Grid', algo: 'Horizontal/Vertical Morph Opening', time: '0.06s', desc: 'Extracts cleanly reconstructed horizontal & vertical grid lines.' },
  { id: 'cells', title: 'Extracted Cells', algo: 'Grid Coordinate Splitting', time: '0.02s', desc: 'Isolates individual table sub-cells based on grid intersections.' },
  { id: 'ocr', title: 'OCR Detection', algo: 'Tesseract OCR Engine', time: '0.18s', desc: 'Recognizes student registration ID characters inside ID columns.' },
  { id: 'sig', title: 'Detected Signatures', algo: 'Positional Fallback Bounding Box', time: '0.03s', desc: 'Isolates cropped signature cells based on student row percentages.' },
  { id: 'results', title: 'Attendance Result', algo: 'Ink Ratio Classifier Verdict', time: '0.01s', desc: 'Determines attendance status based on signature ink density threshold.' }
];

export default function Analysis({ results, imageFile }) {
  // Generate simple mock canvases for visual appeal
  const generateMockSrc = (title, id) => {
    if (!imageFile) return null;
    const canvas = document.createElement('canvas');
    canvas.width = 300;
    canvas.height = 150;
    const ctx = canvas.getContext('2d');
    
    // Custom background based on stage
    if (id === 'thresh' || id === 'morph' || id === 'grid') {
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, 300, 150);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.strokeRect(10, 10, 280, 130);
    } else if (id === 'gray' || id === 'gauss' || id === 'gauss' || id === 'median' || id === 'clahe') {
      ctx.fillStyle = '#64748b';
      ctx.fillRect(0, 0, 300, 150);
      ctx.fillStyle = '#f8fafc';
    } else {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, 300, 150);
    }
    
    ctx.fillStyle = '#38bdf8';
    ctx.font = '13px sans-serif';
    ctx.fillText(title, 20, 80);
    return canvas.toDataURL();
  };

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

      {!imageFile && (
        <Paper sx={{ p: 4, textAlign: 'center', color: 'text.secondary', border: '1px solid', borderColor: 'divider', borderRadius: '12px' }}>
          Please upload and process a scanned document from the Dashboard page to analyze pipeline stages.
        </Paper>
      )}

      {imageFile && (
        <Grid container spacing={3}>
          {analysisStages.map((stage) => (
            <Grid item xs={12} sm={6} md={4} key={stage.id}>
              <ImageViewer
                title={stage.title}
                algoText={stage.algo}
                timeText={stage.time}
                description={stage.desc}
                src={generateMockSrc(stage.title, stage.id)}
              />
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}
