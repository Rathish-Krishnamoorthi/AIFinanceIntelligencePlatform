import React from 'react';
import { Chip } from '@mui/material';
export default function RiskBadge({ level }) { return <Chip size="small" label={level || 'LOW'} color={level === 'HIGH' ? 'error' : level === 'MEDIUM' ? 'warning' : 'success'} />; }
