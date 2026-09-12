import React, { useEffect, useState } from 'react';
import { Alert, Grid, Typography } from '@mui/material';
import api from '../services/api';
import MetricCard from '../components/MetricCard';
import AIInsightCard from '../components/AIInsightCard';
import Loading from '../components/Loading';
import { money } from '../utils/formatters';
export default function Dashboard() {
  const [data, setData] = useState(null); const [insights, setInsights] = useState([]); const [error, setError] = useState('');
  useEffect(() => { Promise.all([api.get('/dashboard/summary'), api.get('/dashboard/insights')]).then(([a, b]) => { setData(a.data); setInsights(b.data); }).catch((e) => setError(e.message)); }, []);
  if (error) return <Alert severity="error">{error}</Alert>; if (!data) return <Loading />;
  const metrics = [['Revenue', money(data.total_revenue)], ['Expenses', money(data.total_expenses), 'error'], ['Net cash flow', money(data.net_cash_flow), 'success'], ['Accounts payable', money(data.accounts_payable), 'warning'], ['Pending invoices', data.pending_invoices], ['Risk score', `${data.financial_risk_score}/100`, 'warning']];
  return <><Typography variant="h4" gutterBottom>Executive overview</Typography><Typography color="text.secondary" sx={{ mb: 3 }}>Explainable intelligence across your financial operations · {data.database_mode === 'demo' ? 'Demo fallback data' : ''}</Typography><Grid container spacing={2}>{metrics.map(([title, value, color]) => <Grid item xs={12} sm={6} md={2} key={title}><MetricCard title={title} value={value} color={color} /></Grid>)}</Grid><Typography variant="h5" sx={{ mt: 4, mb: 2 }}>AI insights</Typography><Grid container spacing={2}>{insights.map((item) => <Grid item xs={12} md={6} key={item._id}><AIInsightCard insight={item} /></Grid>)}</Grid></>;
}
