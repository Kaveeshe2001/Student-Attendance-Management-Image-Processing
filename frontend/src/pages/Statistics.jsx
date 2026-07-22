import React, { useState, useEffect } from 'react';
import { Box, Grid, Typography, Paper, CircularProgress } from '@mui/material';
import ChartCard from '../components/ChartCard';
import StatisticsCard from '../components/StatisticsCard';
import axios from 'axios';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

const COLORS = ['#10b981', '#ef4444', '#f59e0b'];

export default function Statistics({ results, imageFile, sessionId }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!sessionId) {
      setStats(null);
      return;
    }

    setLoading(true);
    // Disable browser caching
    axios.get(`/api/statistics/${sessionId}`, {
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Expires': '0'
      },
      params: {
        t: new Date().getTime()
      }
    })
      .then(res => {
        setStats(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load session statistics:", err);
        setLoading(false);
      });
  }, [sessionId]);

  const total = results.length;
  const present = results.filter(r => r.status === 'Present').length;
  const absent = results.filter(r => r.status === 'Absent').length;
  const review = results.filter(r => r.requires_review).length;

  // Dynamic Pie/Bar Data
  const attendanceData = [
    { name: 'Present', value: present },
    { name: 'Absent', value: absent },
    { name: 'Manual Review', value: review }
  ];

  // Dynamic OCR Confidence Distribution
  const getConfRange = (val) => {
    const num = val <= 1.0 ? val * 100 : val;
    if (num >= 0 && num < 20) return '0-20%';
    if (num >= 20 && num < 40) return '20-40%';
    if (num >= 40 && num < 60) return '40-60%';
    if (num >= 60 && num < 80) return '60-80%';
    return '80-100%';
  };

  const confidenceData = [
    { range: '0-20%', count: results.filter(r => getConfRange(r.confidence) === '0-20%').length },
    { range: '20-40%', count: results.filter(r => getConfRange(r.confidence) === '20-40%').length },
    { range: '40-60%', count: results.filter(r => getConfRange(r.confidence) === '40-60%').length },
    { range: '60-80%', count: results.filter(r => getConfRange(r.confidence) === '60-80%').length },
    { range: '80-100%', count: results.filter(r => getConfRange(r.confidence) === '80-100%').length }
  ];

  // System Pipeline Components Statistics
  const pipelineMetricsData = stats ? [
    { name: 'Tables', count: stats.tables_detected },
    { name: 'Cells', count: stats.cells_detected },
    { name: 'Valid Cells', count: stats.cells_valid },
    { name: 'OCR Reads', count: stats.ocr_texts },
    { name: 'Signatures', count: stats.signatures }
  ] : [];

  const matchedRate = total > 0 && stats ? ((stats.matched_students / total) * 100).toFixed(1) : "0.0";

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
          Performance & Analytics Dashboard
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Monitor system metrics, character recognition quality, and validation checks.
        </Typography>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={2}>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={total} label="Total Students" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={present} label="Present" borderLeftColor="#10b981" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={absent} label="Absent" borderLeftColor="#ef4444" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={review} label="Manual Review" borderLeftColor="#f59e0b" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={`${matchedRate}%`} label="OCR Matching Rate" />
        </Grid>
      </Grid>

      {!imageFile || !sessionId ? (
        <Paper sx={{ p: 4, textAlign: 'center', color: 'text.secondary', border: '1px solid', borderColor: 'divider', borderRadius: '12px' }}>
          Please upload and process a scanned document from the Dashboard page to populate advanced charts.
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {/* Chart 1: Attendance Verdict */}
          <Grid item xs={12} md={6}>
            <ChartCard title="Attendance Verdict Ratio" subtitle="Proportion of Present, Absent, and Manual Review records">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={attendanceData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {attendanceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartCard>
          </Grid>

          {/* Chart 2: Pipeline component statistics */}
          <Grid item xs={12} md={6}>
            <ChartCard title="Extraction & CV Yields" subtitle="Volume of elements processed across CV stages">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={pipelineMetricsData}>
                  <XAxis dataKey="name" stroke="#8892b0" />
                  <YAxis stroke="#8892b0" />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </Grid>

          {/* Chart 3: OCR Confidence histogram */}
          <Grid item xs={12} md={6}>
            <ChartCard title="OCR Confidence Distribution" subtitle="Number of character match results per confidence rating">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={confidenceData}>
                  <XAxis dataKey="range" stroke="#8892b0" />
                  <YAxis stroke="#8892b0" />
                  <Tooltip />
                  <Area type="monotone" dataKey="count" stroke="#10b981" fill="#d1fae5" fillOpacity={0.4} />
                </AreaChart>
              </ResponsiveContainer>
            </ChartCard>
          </Grid>

          {/* Chart 4: Attendance Volume Comparison */}
          <Grid item xs={12} md={6}>
            <ChartCard title="Attendance Status Breakdown" subtitle="Detailed volume check comparison">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={attendanceData}>
                  <XAxis dataKey="name" stroke="#8892b0" />
                  <YAxis stroke="#8892b0" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]}>
                    {attendanceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}
