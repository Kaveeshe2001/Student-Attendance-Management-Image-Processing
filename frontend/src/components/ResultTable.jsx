import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
  TextField,
  InputAdornment,
  Box,
  Typography,
  Chip
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';

export default function ResultTable({ rows }) {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchQuery, setSearchQuery] = useState('');

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
    setPage(0);
  };

  const filteredRows = rows.filter((row) => {
    return (
      row.student_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.student_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.status?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  return (
    <Paper
      elevation={0}
      sx={{
        p: 2.5,
        borderRadius: '16px',
        border: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        bgcolor: 'background.paper',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.05)'
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'text.primary' }}>
          Attendance Verification Logs
        </Typography>

        <TextField
          size="small"
          placeholder="Search records..."
          value={searchQuery}
          onChange={handleSearchChange}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon sx={{ color: 'text.secondary', fontSize: 18 }} />
              </InputAdornment>
            )
          }}
          sx={{
            width: 240,
            '& .MuiOutlinedInput-root': {
              borderRadius: '8px'
            }
          }}
        />
      </Box>

      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 700, bgcolor: 'background.paper' }}>Student ID</TableCell>
              <TableCell sx={{ fontWeight: 700, bgcolor: 'background.paper' }}>Official Name</TableCell>
              <TableCell sx={{ fontWeight: 700, bgcolor: 'background.paper' }}>Attendance</TableCell>
              <TableCell sx={{ fontWeight: 700, bgcolor: 'background.paper' }}>Signature Captured</TableCell>
              <TableCell sx={{ fontWeight: 700, bgcolor: 'background.paper' }}>Confidence</TableCell>
              <TableCell sx={{ fontWeight: 700, bgcolor: 'background.paper' }}>Ink Ratio</TableCell>
              <TableCell sx={{ fontWeight: 700, bgcolor: 'background.paper' }}>Review Needed</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredRows
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row, index) => (
                <TableRow key={index} hover sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                  <TableCell sx={{ fontWeight: 600 }}>{row.student_id}</TableCell>
                  <TableCell>{row.student_name}</TableCell>
                  <TableCell>
                    <Chip
                      size="small"
                      label={row.status}
                      sx={{
                        fontWeight: 600,
                        fontSize: '0.75rem',
                        borderRadius: '6px',
                        bgcolor: row.status === 'Present' ? '#ecfdf5' : row.status === 'Absent' ? '#fef2f2' : '#fffbeb',
                        color: row.status === 'Present' ? '#10b981' : row.status === 'Absent' ? '#ef4444' : '#f59e0b'
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      size="small" 
                      label={row.signature_detected ? "Yes" : "No"} 
                      sx={{
                        fontWeight: 600,
                        fontSize: '0.75rem',
                        borderRadius: '6px',
                        bgcolor: row.signature_detected ? '#eff6ff' : '#f8fafc',
                        color: row.signature_detected ? '#3b82f6' : '#64748b'
                      }}
                    />
                  </TableCell>
                  <TableCell sx={{ fontWeight: 500 }}>
                    {row.confidence ? `${(row.confidence * 100).toFixed(0)}%` : '0%'}
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>
                    {row.ink_ratio ? `${(row.ink_ratio * 100).toFixed(1)}%` : '0.0%'}
                  </TableCell>
                  <TableCell>
                    <Chip
                      size="small"
                      label={row.requires_review ? "Yes" : "No"}
                      sx={{
                        fontWeight: 600,
                        fontSize: '0.75rem',
                        borderRadius: '6px',
                        bgcolor: row.requires_review ? '#fffbeb' : '#f8fafc',
                        color: row.requires_review ? '#f59e0b' : '#64748b'
                      }}
                    />
                  </TableCell>
                </TableRow>
              ))}
            {filteredRows.length === 0 && (
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ color: 'text.secondary', py: 8 }}>
                  No student records available. Process document to inspect.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={filteredRows.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}
