import React, { useEffect, useState } from 'react';
import { Alert, Box, Button, Grid, Stack, Typography } from '@mui/material';
import { ArrowUpward, CalendarMonth, East, TrendingDown, TrendingUp } from '@mui/icons-material';
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import api from '../services/api';
import MetricCard from '../components/MetricCard';
import AIInsightCard from '../components/AIInsightCard';
import ChartCard from '../components/ChartCard';
import Loading from '../components/Loading';
import PageHeader from '../components/PageHeader';
import { money } from '../utils/formatters';

const chartColors = ['#176b87', '#4ca2b8', '#d69a3a', '#2f8f73', '#8b6db1', '#c75454'];
const compactMoney = (value) => `₹${(Number(value || 0) / 100000).toFixed(1)}L`;

export default function Dashboard() {
  const [data, setData] = useState(null); const [insights, setInsights] = useState([]); const [revenue, setRevenue] = useState([]); const [cashFlow, setCashFlow] = useState([]); const [expenses, setExpenses] = useState([]); const [error, setError] = useState('');
  useEffect(() => {
    Promise.all([api.get('/dashboard/summary'), api.get('/dashboard/insights'), api.get('/dashboard/revenue'), api.get('/dashboard/cash-flow'), api.get('/dashboard/expenses')])
      .then(([summary, insightRows, revenueRows, cashRows, expenseRows]) => { setData(summary.data); setInsights(insightRows.data); setRevenue(revenueRows.data); setCashFlow(cashRows.data); setExpenses(expenseRows.data); })
      .catch((e) => setError(e.response?.data?.detail || 'We could not load your financial intelligence.'));
  }, []);
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!data) return <Loading />;
  const hasRecords = data.total_revenue > 0 || data.total_expenses > 0 || data.pending_invoices > 0;
  const helper = hasRecords ? 'Calculated from stored records' : 'No records yet';
  const metrics = [
    ['Revenue', money(data.total_revenue), 'success', ArrowUpward, helper],
    ['Expenses', money(data.total_expenses), 'error', TrendingUp, helper],
    ['Net cash flow', money(data.net_cash_flow), 'success', TrendingUp, helper],
    ['Accounts payable', money(data.accounts_payable), 'warning', TrendingDown, 'Due within 30 days'],
    ['Pending invoices', data.pending_invoices, 'primary', CalendarMonth, `${data.overdue_invoices} overdue`],
    ['Risk score', `${data.financial_risk_score}/100`, 'warning', TrendingDown, 'Medium risk band'],
  ];
  return <Box>
    <PageHeader title={`Good morning, ${data.user_name || 'Finance team'}`} description="Your live financial intelligence overview" action="Export report" />
    <Stack direction="row" spacing={1} sx={{ mb: 3, flexWrap: 'wrap', gap: 1 }}>
      <Button size="small" variant="contained">Last 30 days</Button><Button size="small" variant="outlined">All departments</Button><Button size="small" variant="outlined" startIcon={<CalendarMonth />}>Sep 01 — Sep 30</Button>
    </Stack>
    {!hasRecords && <Alert severity="info" sx={{ mb: 2 }}>Your account is ready. Add a transaction, import a CSV/Excel file, or process an invoice to populate this dashboard.</Alert>}
    <Grid container spacing={2}>{metrics.map(([title, value, color, Icon, metricHelper]) => <Grid item xs={12} sm={6} md={4} lg={2} key={title}><MetricCard title={title} value={value} color={color} icon={<Icon />} helper={metricHelper} /></Grid>)}</Grid>
    <Grid container spacing={2} sx={{ mt: 1 }}>
      <Grid item xs={12} lg={8}><ChartCard title="Revenue vs expenses" description="Monthly performance across your financial operations"><ResponsiveContainer width="100%" height={290}><LineChart data={revenue} margin={{ top: 20, right: 8, left: 0, bottom: 0 }}><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e7edef" /><XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fontSize: 11 }} /><YAxis tickFormatter={compactMoney} axisLine={false} tickLine={false} tick={{ fontSize: 11 }} /><Tooltip formatter={(value) => money(value)} /><Legend /><Line type="monotone" dataKey="revenue" name="Revenue" stroke="#176b87" strokeWidth={3} dot={false} /><Line type="monotone" dataKey="expenses" name="Expenses" stroke="#d69a3a" strokeWidth={3} dot={false} /></LineChart></ResponsiveContainer></ChartCard></Grid>
      <Grid item xs={12} lg={4}><ChartCard title="Expense distribution" description="Where money is being spent"><ResponsiveContainer width="100%" height={290}><PieChart><Pie data={expenses} dataKey="amount" nameKey="category" innerRadius={68} outerRadius={94} paddingAngle={3}>{expenses.map((entry, index) => <Cell key={entry.category} fill={chartColors[index % chartColors.length]} />)}</Pie><Tooltip formatter={(value) => money(value)} /><Legend iconType="circle" wrapperStyle={{ fontSize: 11 }} /></PieChart></ResponsiveContainer></ChartCard></Grid>
      <Grid item xs={12} lg={8}><ChartCard title="Cash flow outlook" description="Historical actuals compared with projected liquidity"><ResponsiveContainer width="100%" height={280}><AreaChart data={cashFlow}><defs><linearGradient id="cashFill" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#4ca2b8" stopOpacity={0.3} /><stop offset="95%" stopColor="#4ca2b8" stopOpacity={0} /></linearGradient></defs><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e7edef" /><XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 11 }} /><YAxis tickFormatter={compactMoney} axisLine={false} tickLine={false} tick={{ fontSize: 11 }} /><Tooltip formatter={(value) => money(value)} /><Legend /><Area type="monotone" dataKey="upper" name="Confidence range" stroke="transparent" fill="url(#cashFill)" /><Line type="monotone" dataKey="actual" name="Historical" stroke="#173042" strokeWidth={2.5} dot={false} /><Line type="monotone" dataKey="forecast" name="Forecast" stroke="#176b87" strokeWidth={2.5} strokeDasharray="6 4" dot={false} /></AreaChart></ResponsiveContainer></ChartCard></Grid>
      <Grid item xs={12} lg={4}><ChartCard title="AI risk brief" description="Based on available historical data"><Stack spacing={2} sx={{ mt: 2 }}><Box sx={{ p: 2, borderRadius: 2, bgcolor: 'rgba(200,135,39,.09)' }}><Typography variant="caption" sx={{ fontWeight: 800, color: 'warning.dark' }}>{data.financial_risk_score ? 'CURRENT RISK' : 'AWAITING DATA'}</Typography><Typography variant="h3" sx={{ mt: .5, fontWeight: 800 }}>{data.financial_risk_score}<Typography component="span" variant="body2" color="text.secondary"> / 100</Typography></Typography></Box><Typography color="text.secondary" sx={{ fontSize: 14 }}>{data.financial_risk_score ? 'Risk is calculated from the records currently visible to your role.' : 'Add or import transactions and invoices to calculate risk.'}</Typography><Button variant="text" endIcon={<East />}>View analysis</Button></Stack></ChartCard></Grid>
    </Grid>
    <Stack direction="row" alignItems="center" spacing={1} sx={{ mt: 5, mb: 2 }}><Typography variant="h5">AI financial insights</Typography><Typography variant="caption" sx={{ color: 'secondary.main', fontWeight: 800 }}>✦ EXPLAINABLE</Typography></Stack>
    <Grid container spacing={2}>{insights.map((item) => <Grid item xs={12} md={6} key={item._id}><AIInsightCard insight={item} /></Grid>)}</Grid>
  </Box>;
}
