import React from 'react';
import { Box, Card, Grid, Skeleton, Stack } from '@mui/material';
export default function Loading() { return <Stack spacing={2} sx={{ p: { xs: 2, md: 4 } }}><Skeleton variant="text" width={260} height={54} /><Skeleton variant="text" width={420} height={24} /><Grid container spacing={2}>{[1, 2, 3, 4].map((item) => <Grid item xs={12} sm={6} md={3} key={item}><Card><Skeleton variant="rectangular" height={125} /></Card></Grid>)}</Grid><Card><Box sx={{ p: 3 }}><Skeleton variant="rectangular" height={300} /></Box></Card></Stack>; }
