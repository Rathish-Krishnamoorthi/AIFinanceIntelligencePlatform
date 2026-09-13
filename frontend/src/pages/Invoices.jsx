import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Alert, Button, Card, CardContent, Chip, Grid, Stack, TextField, Typography } from '@mui/material';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Loading from '../components/Loading';
import PageHeader from '../components/PageHeader';
import useAuth from '../hooks/useAuth';
import { hasPermission } from '../auth/permissions';

const roleLabels = { EMPLOYEE: 'Employee', ACCOUNTANT: 'Employee', FINANCE_MANAGER: 'Finance Manager', CFO: 'CFO', SYSTEM_ADMIN: 'System Admin', ADMIN: 'System Admin', AUDITOR: 'CFO' };

export default function Invoices() {
  const { user } = useAuth();
  const input = useRef(null);
  const [rows, setRows] = useState(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [department, setDepartment] = useState('');
  const [uploading, setUploading] = useState(false);
  const [dragging, setDragging] = useState(false);

  const load = () => api.get('/invoices').then((r) => setRows(r.data)).catch((e) => setError(e.response?.data?.detail || e.message));
  useEffect(() => {
    load();
  }, []);
  const stats = useMemo(() => {
    const values = rows || [];
    return [
      ['Total invoices', values.length],
      ['Pending review', values.filter((row) => row.validation_status === 'FAILED' || row.status === 'VALIDATED').length],
      ['Pending approval', values.filter((row) => row.approval_status === 'PENDING' && row.validation_status !== 'FAILED').length],
      ['Approved', values.filter((row) => row.approval_status === 'APPROVED').length],
      ['Paid', values.filter((row) => row.payment_status === 'PAID').length],
      ['High risk', values.filter((row) => row.risk_level === 'HIGH').length],
    ];
  }, [rows]);

  const upload = async (file) => {
    if (!file) return;
    setError('');
    setMessage('');
    if (file.type !== 'application/pdf' && !['image/jpeg', 'image/png'].includes(file.type)) return setError('Upload a PDF, JPG, or PNG vendor invoice.');
    if (file.size > 10 * 1024 * 1024) return setError('Invoice files must be 10 MB or smaller.');
    const data = new FormData();
    data.append('file', file);
    if (department) data.append('department', department);
    setUploading(true);
    try {
      await api.post('/invoices/upload', data, { headers: { 'Content-Type': 'multipart/form-data' } });
      setMessage('Invoice uploaded and sent through extraction, validation, duplicate, and risk checks.');
      await load();
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not process invoice');
    } finally {
      setUploading(false);
      if (input.current) input.current.value = '';
    }
  };
  const action = async (path, body) => {
    setError('');
    setMessage('');
    try {
      await api.post(path, body);
      setMessage('Invoice workflow updated.');
      load();
    } catch (e) {
      setError(e.response?.data?.detail || 'Invoice action failed');
    }
  };
  const viewDocument = async (invoiceId) => {
    setError('');
    try {
      const response = await api.get(`/invoices/${invoiceId}/document`, { responseType: 'blob' });
      const url = URL.createObjectURL(response.data);
      window.open(url, '_blank', 'noopener,noreferrer');
      window.setTimeout(() => URL.revokeObjectURL(url), 60_000);
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not open the invoice document');
    }
  };
  const canUpload = hasPermission(user, 'INVOICE_UPLOAD');
  const canApprove = hasPermission(user, 'INVOICE_APPROVE');
  const canPay = hasPermission(user, 'INVOICE_PAYMENT');
  const columns = [
    ['invoice_number', 'Invoice'],
    ['vendor_name', 'Vendor'],
    ['total_amount', 'Amount', (value, row) => `${row.currency || 'INR'} ${Number(value || 0).toLocaleString()}`],
    ['status', 'Review status'],
    ['approval_status', 'Approval'],
    ['payment_status', 'Payment'],
    ['risk_level', 'Risk'],
    ['risk_reasons', 'Why flagged', (value) => value?.join('; ') || 'No flags'],
    ['invoice_number', 'Actions', (value, row) => <Stack direction="row" spacing={.5}>{row.status === 'VALIDATED' && <Button size="small" onClick={() => action(`/approvals/${value}/submit`)}>Submit</Button>}{canApprove && row.approval_status === 'PENDING' && row.validation_status !== 'FAILED' && <><Button size="small" onClick={() => action(`/invoices/${value}/approve`)}>Approve</Button><Button size="small" color="error" onClick={() => action(`/invoices/${value}/reject`)}>Reject</Button></>}{canPay && row.approval_status === 'APPROVED' && row.payment_status !== 'PAID' && <Button size="small" onClick={() => { const amount = window.prompt(`Payment amount (outstanding: ${row.outstanding_amount ?? row.total_amount})`); if (amount) action(`/invoices/${value}/payment`, { amount: Number(amount), payment_method: 'Bank transfer' }); }}>Record payment</Button>}<Button size="small" onClick={() => viewDocument(value)}>View PDF</Button></Stack>],
  ];

  return <><PageHeader title="Invoice intake" description="Upload vendor invoices received by the company. FinSight extracts, validates, flags, and routes them for human review." /><Card sx={{ mb: 3, border: dragging ? '2px solid' : '1px solid', borderColor: dragging ? 'primary.main' : 'divider', bgcolor: dragging ? 'rgba(23,107,135,.04)' : 'background.paper' }} onDragOver={(event) => { event.preventDefault(); setDragging(true); }} onDragLeave={() => setDragging(false)} onDrop={(event) => { event.preventDefault(); setDragging(false); upload(event.dataTransfer.files?.[0]); }}><CardContent><Stack spacing={1.5} alignItems="center" sx={{ py: 2 }}><Typography variant="h6">Upload vendor invoice</Typography><Typography color="text.secondary">PDF, scanned PDF, JPG, or PNG · maximum 10 MB</Typography><Stack direction={{ xs: 'column', sm: 'row' }} spacing={1.5} alignItems="center"><TextField size="small" label="Department" value={department} onChange={(event) => setDepartment(event.target.value)} disabled={!['FINANCE_MANAGER', 'CFO'].includes(user?.canonical_role)} placeholder={user?.department || 'Department'} /><Button component="label" variant="contained" disabled={!canUpload || uploading}>{uploading ? 'Processing...' : 'Upload vendor invoice'}<input ref={input} hidden type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={(event) => upload(event.target.files?.[0])} /></Button></Stack>{!canUpload && <Typography variant="caption" color="text.secondary">Your role can view invoices but cannot upload them.</Typography>}</Stack></CardContent></Card>{message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}{error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}<Grid container spacing={1.5} sx={{ mb: 3 }}>{stats.map(([label, value]) => <Grid item xs={6} sm={4} md={2} key={label}><Card><CardContent sx={{ '&:last-child': { pb: 2 } }}><Typography variant="caption" color="text.secondary">{label}</Typography><Typography variant="h5">{value}</Typography></CardContent></Card></Grid>)}</Grid>{!rows ? <Loading /> : <DataTable rows={rows} columns={columns} />}</>;
}
