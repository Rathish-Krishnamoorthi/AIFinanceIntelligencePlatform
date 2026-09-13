import React from 'react';
import { Box, Button, Stack, Typography } from '@mui/material';
import { Download } from '@mui/icons-material';

export default function PageHeader({ eyebrow = 'Fintel Intelligence', title, description, action }) {
  return <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" alignItems={{ xs: 'flex-start', sm: 'center' }} spacing={2} sx={{ mb: 3 }}>
    <Box>
      <Typography variant="overline" sx={{ color: 'primary.main', fontWeight: 800, letterSpacing: '.12em' }}>{eyebrow}</Typography>
      <Typography variant="h4" sx={{ mt: .4 }}>{title}</Typography>
      {description && <Typography color="text.secondary" sx={{ mt: .75 }}>{description}</Typography>}
    </Box>
    {action && <Button variant="outlined" startIcon={<Download fontSize="small" />}>{action}</Button>}
  </Stack>;
}
