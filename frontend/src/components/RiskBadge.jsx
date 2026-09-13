import React from 'react';
import { Chip } from '@mui/material';
export default function RiskBadge({ level }) { const value = level || 'LOW'; const color = value === 'CRITICAL' || value === 'HIGH' ? 'error' : value === 'MEDIUM' || value === 'SUSPICIOUS' ? 'warning' : 'success'; return <Chip size="small" label={value} color={color} sx={{ fontWeight: 800, fontSize: 11 }} />; }
