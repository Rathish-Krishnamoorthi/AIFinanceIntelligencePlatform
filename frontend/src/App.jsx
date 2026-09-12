import React, { useState } from 'react';
import { AppBar, Box, Toolbar, Typography } from '@mui/material';
import useAuth from './hooks/useAuth';
import Loading from './components/Loading';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Invoices from './pages/Invoices';
import Vendors from './pages/Vendors';
import Anomalies from './pages/Anomalies';
import Forecasting from './pages/Forecasting';
import Budgets from './pages/Budgets';
import RiskDashboard from './pages/RiskDashboard';
import Approvals from './pages/Approvals';
import FinancialAssistant from './pages/FinancialAssistant';
import Notifications from './pages/Notifications';
import AuditLogs from './pages/AuditLogs';

const pages = { dashboard: Dashboard, transactions: Transactions, invoices: Invoices, vendors: Vendors, anomalies: Anomalies, cash: Forecasting, budgets: Budgets, risk: RiskDashboard, approvals: Approvals, assistant: FinancialAssistant, notifications: Notifications, audit: AuditLogs };
const nav = [['dashboard', 'Dashboard'], ['transactions', 'Transactions'], ['invoices', 'Invoices'], ['vendors', 'Vendors'], ['anomalies', 'Anomalies'], ['cash', 'Cash Flow'], ['budgets', 'Budgets'], ['risk', 'Risk Intelligence'], ['approvals', 'Approvals'], ['assistant', 'AI Assistant'], ['notifications', 'Notifications'], ['audit', 'Audit Logs']];
export default function App() { const { user, loading } = useAuth(); const [page, setPage] = useState('dashboard'); if (loading) return <Loading />; if (!user) return <Login />; const Page = pages[page]; return <><Navbar /><Sidebar items={nav} page={page} onNavigate={setPage} /><Box component="main" sx={{ ml: '220px', pt: 10, px: 4, pb: 4 }}><Page /></Box></>; }
