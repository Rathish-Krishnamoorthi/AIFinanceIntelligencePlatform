import React from 'react';
import { Box, Typography } from '@mui/material';
import { SearchOff } from '@mui/icons-material';

export default function EmptyState({ title = 'Nothing to show yet', description = 'When new financial activity is available, it will appear here.' }) {
  return <Box sx={{ minHeight: 220, display: 'grid', placeItems: 'center', textAlign: 'center', p: 4 }}>
    <Box><SearchOff sx={{ fontSize: 42, color: 'primary.light', mb: 1 }} /><Typography variant="h6">{title}</Typography><Typography color="text.secondary" sx={{ mt: .5 }}>{description}</Typography></Box>
  </Box>;
}
