import React, { useState, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, Box, CssBaseline } from '@mui/material';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Footer from './components/Footer';

// Pages
import Dashboard from './pages/Dashboard';
import Analysis from './pages/Analysis';
import Visualization from './pages/Visualization';
import Statistics from './pages/Statistics';
import Results from './pages/Results';
import Settings from './pages/Settings';
import About from './pages/About';

export default function App() {
  const [mode, setMode] = useState('light');
  const [imageFile, setImageFile] = useState(null);
  const [xmlFile, setXmlFile] = useState(null);
  const [results, setResults] = useState([]);
  const [logs, setLogs] = useState([]);
  const [analytics, setAnalytics] = useState({});
  
  const [config, setConfig] = useState({
    ocrProvider: 'tesseract',
    confidenceThreshold: 0.8,
    sigThreshold: 0.08,
    saveProcessedImages: true,
    enableDebugLogs: true,
    useFallbackMatching: true
  });

  const toggleColorMode = () => {
    setMode((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === 'light'
            ? {
                background: {
                  default: '#f4f6fa',
                  paper: '#ffffff',
                },
                text: {
                  primary: '#1e293b',
                  secondary: '#64748b',
                },
                divider: '#e2e8f0',
              }
            : {
                background: {
                  default: '#090d16',
                  paper: '#151e2e',
                },
                text: {
                  primary: '#f1f5f9',
                  secondary: '#94a3b8',
                },
                divider: '#1e293b',
              }),
        },
        typography: {
          fontFamily: "'Inter', sans-serif",
        },
        components: {
          MuiPaper: {
            styleOverrides: {
              root: {
                backgroundImage: 'none',
              },
            },
          },
        },
      }),
    [mode]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
          {/* Collapsible Left Sidebar */}
          <Sidebar />

          {/* Main Layout Area */}
          <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, overflow: 'hidden' }}>
            <Header toggleColorMode={toggleColorMode} mode={mode} />

            {/* Scrollable Page Body */}
            <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 3 }}>
              <Routes>
                <Route 
                  path="/" 
                  element={
                    <Dashboard 
                      imageFile={imageFile} 
                      setImageFile={setImageFile}
                      xmlFile={xmlFile} 
                      setXmlFile={setXmlFile}
                      results={results} 
                      setResults={setResults}
                      logs={logs} 
                      setLogs={setLogs}
                      setAnalytics={setAnalytics}
                    />
                  } 
                />
                <Route 
                  path="/analysis" 
                  element={<Analysis results={results} imageFile={imageFile} />} 
                />
                <Route 
                  path="/visualization" 
                  element={<Visualization imageFile={imageFile} />} 
                />
                <Route 
                  path="/statistics" 
                  element={<Statistics results={results} imageFile={imageFile} />} 
                />
                <Route 
                  path="/results" 
                  element={<Results results={results} imageFile={imageFile} />} 
                />
                <Route 
                  path="/settings" 
                  element={<Settings config={config} setConfig={setConfig} />} 
                />
                <Route 
                  path="/about" 
                  element={<About />} 
                />
              </Routes>
            </Box>

            <Footer />
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}
