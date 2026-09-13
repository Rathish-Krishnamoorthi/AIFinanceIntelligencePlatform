import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import './styles.css';
import App from './App';
import { AuthProvider } from './context/AuthContext';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#176b87', dark: '#0d4458', light: '#4ca2b8' },
    secondary: { main: '#d69a3a' },
    background: { default: '#f4f7f8', paper: '#ffffff' },
    text: { primary: '#173042', secondary: '#6b7c87' },
    success: { main: '#2f8f73' },
    warning: { main: '#c88727' },
    error: { main: '#c75454' },
  },
  typography: {
    fontFamily: '"DM Sans", "Segoe UI", sans-serif',
    h4: { fontWeight: 800, letterSpacing: '-0.035em' },
    h5: { fontWeight: 800, letterSpacing: '-0.025em' },
    h6: { fontWeight: 700 },
    button: { textTransform: 'none', fontWeight: 700 },
  },
  shape: { borderRadius: 16 },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          border: '1px solid rgba(23, 48, 66, 0.07)',
          boxShadow: '0 10px 30px rgba(31, 65, 78, 0.06)',
          transition: 'transform 180ms ease, box-shadow 180ms ease',
          '&:hover': { transform: 'translateY(-2px)', boxShadow: '0 16px 34px rgba(31, 65, 78, 0.1)' },
        },
      },
    },
    MuiButton: { styleOverrides: { root: { borderRadius: 10, paddingInline: 18 } } },
    MuiTextField: { defaultProps: { size: 'small' } },
    MuiTableCell: { styleOverrides: { head: { fontWeight: 800, color: '#526775', background: '#f7fafb' } } },
  },
});

createRoot(document.getElementById('root')).render(
  <React.StrictMode><ThemeProvider theme={theme}><CssBaseline /><BrowserRouter><AuthProvider><App /></AuthProvider></BrowserRouter></ThemeProvider></React.StrictMode>
);
