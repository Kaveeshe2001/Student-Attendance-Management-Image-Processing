import React from 'react';
import { Box, Typography, Paper, Grid, Chip } from '@mui/material';
import { School as SchoolIcon, DeveloperBoard as DevIcon, Settings as TechIcon } from '@mui/icons-material';

const techStack = [
  "OpenCV",
  "Python",
  "React",
  "Tesseract OCR",
  "XML Parsing",
  "Computer Vision",
  "Adaptive Thresholding",
  "Perspective Warp",
  "Material UI",
  "Vite"
];

export default function About() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Box>
        <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary' }}>
          About SAMS
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Student Attendance Management System (SAMS) • Technical Metadata & Architecture.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Col 1: Project Details */}
        <Grid item xs={12} md={8}>
          <Paper elevation={0} sx={{ p: 3, borderRadius: '16px', border: '1px solid', borderColor: 'divider', display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
              <SchoolIcon sx={{ color: 'primary.main' }} /> Project Specifications
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', lineHeight: 1.6 }}>
              The Student Attendance Management System (SAMS) is a computer vision and image processing pipeline designed to digitize scanned printed attendance sheets automatically. By integrating custom threshold filters, edge detectors, perspective warp transforms, table contour grids, cell extraction, Tesseract character recognition, and positional fallback matching, the system recognizes student index numbers and detects signature ink density to produce structured CSV logs.
            </Typography>

            <Typography variant="subtitle2" sx={{ fontWeight: 700, mt: 1 }}>
              Key Algorithms:
            </Typography>
            <Box component="ul" sx={{ pl: 2, color: 'text.secondary', fontSize: '0.85rem', display: 'flex', flexDirection: 'column', gap: 1 }}>
              <li><strong>Perspective Warp Correction:</strong> Detects document bounding limits and aligns the scan sheet to a standard grid.</li>
              <li><strong>Adaptive Gaussian Binarization:</strong> Separates handwriting and grids from paper backgrounds under varying exposures.</li>
              <li><strong>Grid Extraction:</strong> Projects horizontal and vertical pixel density profiles to generate clean cell intersections mathematically.</li>
              <li><strong>Signature Ink Classifier:</strong> Preprocesses cropped sign-blocks and computes foreground pixel densities to verify attendance.</li>
            </Box>
          </Paper>
        </Grid>

        {/* Col 2: Dev Info */}
        <Grid item xs={12} md={4}>
          <Paper elevation={0} sx={{ p: 3, borderRadius: '16px', border: '1px solid', borderColor: 'divider', display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
              <DevIcon sx={{ color: 'primary.main' }} /> Team Information
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                NSBM Green University
              </Typography>
              <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block' }}>
                Faculty of Computing • Batch 22.1
              </Typography>
              <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block' }}>
                Course: Computer Graphics and Visualization
              </Typography>
              <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block' }}>
                Module ID: CGV-302
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Technology Stack Grid */}
        <Grid item xs={12}>
          <Paper elevation={0} sx={{ p: 3, borderRadius: '16px', border: '1px solid', borderColor: 'divider', display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
              <TechIcon sx={{ color: 'primary.main' }} /> Supported Technologies
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {techStack.map(tech => (
                <Chip key={tech} label={tech} variant="outlined" sx={{ fontWeight: 600, fontSize: '0.8rem' }} />
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
