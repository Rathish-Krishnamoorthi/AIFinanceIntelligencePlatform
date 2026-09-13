import React from 'react';
import { ArrowDownward, ArrowUpward, TrendingFlat } from '@mui/icons-material';
import { Box, Card, CardContent, Stack, Typography } from '@mui/material';
export default function MetricCard({ title, value, color = 'primary', icon, helper }) {
  const Trend = color === 'error' ? ArrowDownward : color === 'success' ? ArrowUpward : TrendingFlat;
  return <Card><CardContent sx={{ p: 2.25 }}><Stack direction="row" justifyContent="space-between" alignItems="center"><Typography color="text.secondary" sx={{ fontSize: 12, fontWeight: 700 }}>{title}</Typography>{icon && <Box sx={{ color: `${color}.main`, display: 'grid', placeItems: 'center' }}>{icon}</Box>}</Stack><Typography variant="h5" color={color} sx={{ mt: 1, fontWeight: 800, fontSize: { xs: 22, md: 24 } }}>{value}</Typography><Stack direction="row" alignItems="center" spacing={.5} sx={{ mt: 1, color: `${color}.main` }}><Trend sx={{ fontSize: 15 }} /><Typography variant="caption" sx={{ color: 'text.secondary', fontSize: 10 }}>{helper}</Typography></Stack></CardContent></Card>;
}
