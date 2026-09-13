import React from 'react';
import { Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import { Box } from '@mui/material';
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
import Users from './pages/Users';
import Profile from './pages/Profile';
import ProtectedRoute from './auth/ProtectedRoute';
import { hasPermission, ROLE_ALIASES } from './auth/permissions';

const pages = { dashboard: Dashboard, transactions: Transactions, invoices: Invoices, vendors: Vendors, anomalies: Anomalies, cash: Forecasting, budgets: Budgets, risk: RiskDashboard, approvals: Approvals, assistant: FinancialAssistant, notifications: Notifications, audit: AuditLogs, users: Users, profile: Profile };
const definitions = {
  employee: [['dashboard', 'Dashboard', 'DASHBOARD_VIEW'], ['transactions', 'My Transactions', 'TRANSACTION_VIEW'], ['budgets', 'My Budget', 'BUDGET_VIEW'], ['cash', 'My Cash Flow', 'FORECAST_VIEW'], ['notifications', 'My Reports', 'NOTIFICATION_VIEW'], ['assistant', 'AI Insights', 'ASSISTANT_USE']],
  finance: [['dashboard', 'Dashboard', 'DASHBOARD_VIEW'], ['transactions', 'Transactions', 'TRANSACTION_VIEW'], ['invoices', 'Invoices', 'INVOICE_VIEW'], ['vendors', 'Vendors', 'VENDOR_VIEW'], ['approvals', 'Approvals', 'APPROVAL_VIEW'], ['budgets', 'Budgets', 'BUDGET_VIEW'], ['cash', 'Cash Flow', 'FORECAST_VIEW'], ['anomalies', 'Fraud Detection', 'ANOMALY_VIEW'], ['risk', 'Risk Dashboard', 'RISK_VIEW'], ['assistant', 'AI Assistant', 'ASSISTANT_USE']],
  cfo: [['dashboard', 'Executive Dashboard', 'DASHBOARD_VIEW'], ['transactions', 'Transactions', 'TRANSACTION_VIEW'], ['invoices', 'Invoices', 'INVOICE_VIEW'], ['vendors', 'Vendors', 'VENDOR_VIEW'], ['budgets', 'Budget Analytics', 'BUDGET_VIEW'], ['cash', 'Cash Flow Forecast', 'FORECAST_VIEW'], ['anomalies', 'Fraud & Risk', 'ANOMALY_VIEW'], ['risk', 'Vendor Risk', 'RISK_VIEW'], ['assistant', 'AI Decision Assistant', 'ASSISTANT_USE'], ['audit', 'Audit Logs', 'AUDIT_VIEW']],
  admin: [['dashboard', 'Admin Dashboard', 'DASHBOARD_VIEW'], ['users', 'Users & Roles', 'USER_VIEW'], ['audit', 'Audit Logs', 'AUDIT_VIEW']],
};
const rolePrefixes = { EMPLOYEE: 'employee', ACCOUNTANT: 'employee', FINANCE_MANAGER: 'finance', CFO: 'cfo', AUDITOR: 'cfo', SYSTEM_ADMIN: 'admin', ADMIN: 'admin' };

export default function App() {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  return <Routes><Route path="/login" element={user ? <RoleRedirect user={user} /> : <Login />} /><Route path="/:workspace/login" element={user ? <RoleRedirect user={user} /> : <RoleLogin />} /><Route path="/*" element={user ? <RoleRouter user={user} /> : <Navigate to="/login" replace />} /></Routes>;
}

function RoleLogin() {
  const { pathname } = useLocation();
  const workspace = pathname.split('/')[1];
  const labels = { employee: 'Employee', finance: 'Finance Manager', cfo: 'CFO', admin: 'System Admin' };
  return <Login workspaceLabel={labels[workspace] || 'Fintel'} />;
}

function RoleRouter({ user }) {
  const prefix = rolePrefixes[user.canonical_role || ROLE_ALIASES[user.role] || user.role] || 'employee';
  return <Routes>
    <Route path="/" element={<Navigate to={`/${prefix}/dashboard`} replace />} />
    <Route path={`/${prefix}/*`} element={<RoleLayout user={user} prefix={prefix} />} />
    <Route path="*" element={<Navigate to={`/${prefix}/dashboard`} replace />} />
  </Routes>;
}

function RoleRedirect({ user }) {
  const prefix = rolePrefixes[user.canonical_role || ROLE_ALIASES[user.role] || user.role] || 'employee';
  return <Navigate to={`/${prefix}/dashboard`} replace />;
}

function RoleLayout({ user, prefix }) {
  const [collapsed, setCollapsed] = React.useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const items = (definitions[prefix] || []).filter(([, , permission]) => hasPermission(user, permission));
  const key = location.pathname.split('/').filter(Boolean).pop() || 'dashboard';
  const active = items.some(([item]) => item === key) ? key : items[0]?.[0];
  const Page = pages[active] || Dashboard;
  const permission = items.find(([item]) => item === active)?.[2];
  const roleLabel = { employee: 'Employee', finance: 'Finance Manager', cfo: 'CFO', admin: 'System Admin' }[prefix];
  const destination = `/${prefix}/${active}`;
  if (location.pathname !== `/${prefix}` && key !== 'profile' && !items.some(([item]) => item === key)) {
    return <Navigate to={destination} replace />;
  }
  const profileDestination = `/${prefix}/profile`;
  return <><Navbar pageTitle={`${roleLabel} · ${active === 'profile' ? 'My Profile' : items.find(([item]) => item === active)?.[1] || ''}`} collapsed={collapsed} onProfileClick={() => navigate(profileDestination)} /><Sidebar items={items.map(([item, label]) => [item, label])} page={active} collapsed={collapsed} onToggle={() => setCollapsed((value) => !value)} onNavigate={(item) => navigate(`/${prefix}/${item}`)} /><Box component="main" className="page-shell" sx={{ ml: { xs: 0, md: collapsed ? '76px' : '248px' }, pt: { xs: 10, md: 11 }, px: { xs: 2, sm: 3, md: 5 }, pb: 5, transition: 'margin-left 180ms ease' }}><Routes><Route path="" element={<Navigate to={destination} replace />} /><Route path="profile" element={<Profile />} /><Route path=":page" element={<ProtectedRoute permission={permission}><Page /></ProtectedRoute>} /><Route path="*" element={<Navigate to={destination} replace />} /></Routes></Box></>;
}
