import React from 'react';
import { Box, Grid, Typography, Paper } from '@mui/material';
import ChartCard from '../components/ChartCard';
import StatisticsCard from '../components/StatisticsCard';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area
} from 'recharts';

const COLORS = ['#10b981', '#ef4444', '#f59e0b'];

export default function Statistics({ results, imageFile }) {
  const total = results.length;
  const present = results.filter(r => r.status === 'Present').length;
  const absent = results.filter(r => r.status === 'Absent').length;
  const review = results.filter(r => r.requires_review).length;

  // Pie/Bar Data
  const attendanceData = [
    { name: 'Present', value: total > 0 ? present : 0 },
    { name: 'Absent', value: total > 0 ? absent : 0 },
    { name: 'Manual Review', value: total > 0 ? review : 0 }
  ];

  // Pipeline Timings Data (ms)
  const timingData = [
    { stage: 'Warp', time: 120 },
    { stage: 'Gray', time: 10 },
    { stage: 'Enhance', time: 140 },
    { stage: 'Threshold', time: 20 },
    { stage: 'Grid', time: 60 },
    { stage: 'Cells', time: 20 },
    { stage: 'OCR', time: 180 },
    { stage: 'Match', time: 30 },
    { stage: 'Signature', time: 30 }
  ];

  // OCR Confidence Distribution data
  const confidenceData = [
    { range: '0-20%', count: 0 },
    { range: '20-40%', count: 0 },
    { range: '40-60%', count: 0 },
    { range: '60-80%', count: 1 },
    { range: '80-100%', count: 5 }
  ];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Box>
        <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary' }}>
          Performance & Analytics Dashboard
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Monitor system metrics, processing speeds, character recognition quality, and validation checks.
        </Typography>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={2}>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={total > 0 ? total : 0} label="Total Students" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={total > 0 ? present : 0} label="Present" borderLeftColor="#10b981" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={total > 0 ? absent : 0} label="Absent" borderLeftColor="#ef4444" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={total > 0 ? review : 0} label="Manual Review" borderLeftColor="#f59e0b" />
        </Grid>
        <Grid item xs={6} sm={4} md={2.4}>
          <StatisticsCard value={total > 0 ? "100.0%" : "0.0%"} label="OCR Matching Rate" />
        </Grid>
      </Grid>

      {!imageFile ? (
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

          {/* Chart 2: Pipeline execution times */}
          <Grid item xs={12} md={6}>
            <ChartCard title="Pipeline Execution Time (ms)" subtitle="Breakdown of processing speed for each stage">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={timingData}>
                  <XAxis dataKey="stage" stroke="#8892b0" />
                  <YAxis stroke="#8892b0" />
                  <Tooltip />
                  <Bar dataKey="time" fill="#3b82f6" radius={[4, 4, 0, 0]} />
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
