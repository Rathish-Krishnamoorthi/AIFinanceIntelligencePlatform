import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
export default function MetricCard({ title, value, color = 'primary' }) {
  return <Card><CardContent><Typography color="text.secondary">{title}</Typography><Typography variant="h5" color={color} sx={{ mt: 1, fontWeight: 700 }}>{value}</Typography></CardContent></Card>;
}
