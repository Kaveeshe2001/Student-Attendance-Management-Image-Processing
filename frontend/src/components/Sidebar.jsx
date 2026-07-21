import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Box, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  IconButton, 
  Typography, 
  Divider 
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Analytics as AnalyticsIcon,
  Visibility as VisibilityIcon,
  BarChart as BarChartIcon,
  AssignmentTurnedIn as ResultsIcon,
  Settings as SettingsIcon,
  Info as InfoIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  School as SchoolIcon
} from '@mui/icons-material';

const menuItems = [
  { text: 'Dashboard', path: '/', icon: <DashboardIcon /> },
  { text: 'Analysis', path: '/analysis', icon: <AnalyticsIcon /> },
  { text: 'Visualization', path: '/visualization', icon: <VisibilityIcon /> },
  { text: 'Statistics', path: '/statistics', icon: <BarChartIcon /> },
  { text: 'Results', path: '/results', icon: <ResultsIcon /> },
  { text: 'Settings', path: '/settings', icon: <SettingsIcon /> },
  { text: 'About', path: '/about', icon: <InfoIcon /> }
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <Box
      sx={{
        width: collapsed ? 70 : 260,
        height: '100vh',
        bgcolor: '#0a192f',
        color: '#8892b0',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        transition: 'width 0.3s ease',
        borderRight: '1px solid rgba(255, 255, 255, 0.08)',
        flexShrink: 0,
        zIndex: 100
      }}
    >
      <Box>
        {/* Brand Logo Header */}
        <Box sx={{ display: 'flex', alignItems: 'center', p: 2, height: 64, justifyContent: collapsed ? 'center' : 'space-between' }}>
          {!collapsed && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <SchoolIcon sx={{ color: '#64ffda', fontSize: 28 }} />
              <Typography variant="h6" sx={{ color: '#f8f9fa', fontWeight: 700, letterSpacing: 0.5, fontSize: '1.1rem' }}>
                SAMS Panel
              </Typography>
            </Box>
          )}
          {collapsed && <SchoolIcon sx={{ color: '#64ffda', fontSize: 28 }} />}
          <IconButton onClick={() => setCollapsed(!collapsed)} sx={{ color: '#8892b0' }}>
            {collapsed ? <ChevronRightIcon /> : <ChevronLeftIcon />}
          </IconButton>
        </Box>
        <Divider sx={{ bgcolor: 'rgba(255, 255, 255, 0.08)' }} />

        {/* Menu Items */}
        <List sx={{ px: 1, py: 2 }}>
          {menuItems.map((item) => (
            <ListItem
              key={item.text}
              component={NavLink}
              to={item.path}
              sx={{
                borderRadius: '8px',
                mb: 0.5,
                color: '#8892b0',
                '&.active': {
                  color: '#64ffda',
                  bgcolor: 'rgba(100, 255, 218, 0.08)',
                  '& .MuiListItemIcon-root': {
                    color: '#64ffda'
                  }
                },
                '&:hover': {
                  bgcolor: 'rgba(255, 255, 255, 0.04)',
                  color: '#f8f9fa',
                  '& .MuiListItemIcon-root': {
                    color: '#f8f9fa'
                  }
                },
                px: collapsed ? 1.5 : 2
              }}
            >
              <ListItemIcon sx={{ color: 'inherit', minWidth: collapsed ? 0 : 40 }}>
                {item.icon}
              </ListItemIcon>
              {!collapsed && (
                <ListItemText 
                  primary={item.text} 
                  primaryTypographyProps={{ fontSize: '0.95rem', fontWeight: 500 }}
                />
              )}
            </ListItem>
          ))}
        </List>
      </Box>

      {/* Footer Info */}
      <Box sx={{ p: 2, borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', alignItems: 'center', gap: 1.5, justifyContent: collapsed ? 'center' : 'flex-start' }}>
        <Box 
          sx={{ 
            width: 8, 
            height: 8, 
            bgcolor: '#10b981', 
            borderRadius: '50%', 
            boxShadow: '0 0 8px #10b981' 
          }} 
        />
        {!collapsed && (
          <Typography variant="caption" sx={{ color: '#8892b0', fontWeight: 500 }}>
            System Status: Connected
          </Typography>
        )}
      </Box>
    </Box>
  );
}
