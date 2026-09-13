import React from 'react';
import { Card, CardContent, Stack, Typography } from '@mui/material';

export default function ChartCard({ title, description, children, action }) {
  return <Card sx={{ height: '100%' }}><CardContent sx={{ p: { xs: 2, md: 2.5 } }}>
    <Stack direction="row" justifyContent="space-between" alignItems="flex-start" spacing={2}>
      <div><Typography variant="h6">{title}</Typography>{description && <Typography variant="caption" color="text.secondary">{description}</Typography>}</div>
      {action}
    </Stack>
    <div className="chart-wrap" style={{ marginTop: 16, minWidth: 0 }}>{children}</div>
  </CardContent></Card>;
}
