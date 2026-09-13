import React from 'react';
import { Chip } from '@mui/material';

export default function StatusBadge({ value }) {
  const normalized = String(value || 'NORMAL').toUpperCase();
  const color = ['HIGH', 'CRITICAL', 'REJECTED', 'OVERDUE'].includes(normalized) ? 'error' : ['MEDIUM', 'PENDING', 'FLAGGED', 'SUSPICIOUS'].includes(normalized) ? 'warning' : ['PAID', 'APPROVED', 'LOW', 'NORMAL', 'ACTIVE'].includes(normalized) ? 'success' : 'default';
  return <Chip size="small" label={normalized} color={color} variant={color === 'default' ? 'outlined' : 'filled'} sx={{ fontWeight: 800, fontSize: 11 }} />;
}
