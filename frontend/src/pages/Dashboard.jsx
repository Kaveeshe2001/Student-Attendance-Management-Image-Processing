import React, { useState } from 'react';
import { Box, Button, Grid, Typography, Snackbar, Alert } from '@mui/material';
import UploadCard from '../components/UploadCard';
import ProgressPipeline from '../components/ProgressPipeline';
import ProcessingLog from '../components/ProcessingLog';
import StatisticsCard from '../components/StatisticsCard';
import ResultTable from '../components/ResultTable';
import LoadingOverlay from '../components/LoadingOverlay';
import axios from 'axios';

export default function Dashboard({ imageFile, setImageFile, xmlFile, setXmlFile, results, setResults, logs, setLogs, analytics, setAnalytics, sessionId, setSessionId }) {
  const [activeStep, setActiveStep] = useState(-1);
  const [statusText, setStatusText] = useState('');
  const [processing, setProcessing] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMsg, setToastMsg] = useState('');
  const [toastSeverity, setToastSeverity] = useState('success');

  const handleImageSelect = (fileData) => {
    setImageFile(fileData);
    setLogs(prev => [...prev, `[INFO] Scanned attendance sheet loaded: ${fileData.file.name}`]);
  };

  const handleXmlSelect = (fileData) => {
    setXmlFile(fileData);
    setLogs(prev => [...prev, `[INFO] Student record list loaded: ${fileData.file.name}`]);
  };

  const handleProcess = async () => {
    if (!imageFile || !xmlFile) return;

    setProcessing(true);
    setLogs([]);
    setResults([]);
    setSessionId(null);
    setActiveStep(0);
    setStatusText('Warping image scan...');

    try {
      const formData = new FormData();
      formData.append('image', imageFile.file);
      formData.append('xml', xmlFile.file);

      // Disable browser caching for API requests
      setLogs(prev => [...prev, "[INFO] Connecting to python backend REST APIs..."]);
      
      const uploadRes = await axios.post('/api/process', formData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
          'Expires': '0'
        }
      });

      const session = uploadRes.data;
      if (session && session.id) {
        const session_id = session.id;
        setSessionId(session_id);
        
        // Fetch results, logs, and stats in parallel from SQLite REST endpoints
        const cacheBypassConfig = {
          headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Expires': '0'
          },
          params: {
            t: new Date().getTime() // Cache-busting timestamp
          }
        };

        const [resultsRes, logsRes, statsRes] = await Promise.all([
          axios.get(`/api/results/${session_id}`, cacheBypassConfig),
          axios.get(`/api/logs/${session_id}`, cacheBypassConfig),
          axios.get(`/api/statistics/${session_id}`, cacheBypassConfig)
        ]);

        setResults(resultsRes.data.map(r => ({
          student_id: r.student_id,
          student_name: r.student_name,
          status: r.attendance,
          signature_detected: r.signature_detected,
          confidence: r.confidence,
          ink_ratio: r.ink_ratio,
          requires_review: r.review_required
        })));
        
        const formattedLogs = logsRes.data.map(l => `[${l.level}] [${l.stage}] ${l.message}`);
        setLogs(formattedLogs);
        
        setAnalytics({
          total: session.present_students + session.absent_students + session.manual_review,
          present: session.present_students,
          absent: session.absent_students,
          review: session.manual_review,
          signatures: statsRes.data.signatures,
          time: `${session.processing_time}s`
        });

        setActiveStep(12);
        setStatusText("Completed");
        setProcessing(false);
        setToastMsg("Document analyzed successfully via REST API!");
        setToastSeverity('success');
        setShowToast(true);
      }
    } catch (err) {
      console.error(err);
      const errMsg = err.response?.data?.detail || err.message || "Unknown error";
      setLogs(prev => [
        ...prev,
        `[ERROR] Connection failed: ${errMsg}`
      ]);
      setProcessing(false);
      setToastMsg(`SAMS execution failed: ${errMsg}`);
      setToastSeverity('error');
      setShowToast(true);
    }
  };

  const handleReset = () => {
    setImageFile(null);
    setXmlFile(null);
    setResults([]);
    setLogs([]);
    setSessionId(null);
    setActiveStep(-1);
    setStatusText('');
  };

  // Stats Card data
  const total = results.length;
  const present = results.filter(r => r.status === 'Present').length;
  const absent = results.filter(r => r.status === 'Absent').length;
  const review = results.filter(r => r.requires_review).length;
  const signatures = results.filter(r => r.signature_detected).length;

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      
      {/* ROW 1: DRAG & DROP UPLOAD CARDS */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <UploadCard
            title="Attendance Sheet Scanner Image"
            subtitle="Drag & drop scanned JPEG image here"
            accept={{ 'image/jpeg': ['.jpeg', '.jpg'], 'image/png': ['.png'] }}
            onFileSelect={handleImageSelect}
            file={imageFile}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <UploadCard
            title="Student XML Database"
            subtitle="Drag & drop student list XML here"
            accept={{ 'text/xml': ['.xml'] }}
            onFileSelect={handleXmlSelect}
            file={xmlFile}
          />
        </Grid>
      </Grid>

      {/* ROW 2: CONTROLS & PIPELINE */}
      <ProgressPipeline activeStep={activeStep} statusText={statusText} />

      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          onClick={handleProcess}
          disabled={!imageFile || !xmlFile || processing}
          sx={{
            background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
            color: '#ffffff',
            fontWeight: 600,
            borderRadius: '8px',
            px: 4,
            py: 1.2,
            boxShadow: '0 4px 15px rgba(37, 99, 235, 0.35)'
          }}
        >
          Process Attendance
        </Button>
        <Button variant="outlined" onClick={handleReset} sx={{ borderRadius: '8px', fontWeight: 600 }}>
          Reset
        </Button>
      </Box>

      {/* STATS COUNT OVERVIEW */}
      <Grid container spacing={2}>
        <Grid item xs={6} sm={4} md={2}>
          <StatisticsCard value={total} label="Total Students" />
        </Grid>
        <Grid item xs={6} sm={4} md={2}>
          <StatisticsCard value={present} label="Present" borderLeftColor="#10b981" />
        </Grid>
        <Grid item xs={6} sm={4} md={2}>
          <StatisticsCard value={absent} label="Absent" borderLeftColor="#ef4444" />
        </Grid>
        <Grid item xs={6} sm={4} md={2}>
          <StatisticsCard value={review} label="Manual Review" borderLeftColor="#f59e0b" />
        </Grid>
        <Grid item xs={6} sm={4} md={2}>
          <StatisticsCard value={signatures} label="Signatures Found" />
        </Grid>
        <Grid item xs={6} sm={4} md={2}>
          <StatisticsCard value={total > 0 && analytics?.time ? analytics.time : "0.00s"} label="Processing Time" />
        </Grid>
      </Grid>
 
      {/* TABLE & CONSOLE GRIDS */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <ResultTable rows={results} />
        </Grid>
        <Grid item xs={12} md={4}>
          <ProcessingLog logs={logs} />
        </Grid>
      </Grid>
 
      <LoadingOverlay active={processing} message="Executing AI Table Detection..." />
 
      <Snackbar open={showToast} autoHideDuration={3000} onClose={() => setShowToast(false)}>
        <Alert onClose={() => setShowToast(false)} severity={toastSeverity} sx={{ width: '100%' }}>
          {toastMsg}
        </Alert>
      </Snackbar>
    </Box>
  );
}
