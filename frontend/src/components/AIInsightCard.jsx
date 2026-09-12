import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import RiskBadge from './RiskBadge';
export default function AIInsightCard({ insight }) { return <Card><CardContent><RiskBadge level={insight.severity} /><Typography variant="h6" sx={{ mt: 1 }}>{insight.title}</Typography><Typography>{insight.description}</Typography><Typography color="text.secondary" sx={{ mt: 1 }}>Why: {insight.evidence?.join(' · ')}</Typography></CardContent></Card>; }
