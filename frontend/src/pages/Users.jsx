import React, { useEffect, useState } from 'react';
import { Alert, Button, Card, CardContent, Divider, MenuItem, Stack, TextField, Typography } from '@mui/material';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Loading from '../components/Loading';
import PageHeader from '../components/PageHeader';

const initial = { name: '', email: '', password: '', role: 'FINANCE_MANAGER', department: 'Finance' };
const roleLabels = { EMPLOYEE: 'Employee', ACCOUNTANT: 'Employee', FINANCE_MANAGER: 'Finance Manager', CFO: 'CFO', SYSTEM_ADMIN: 'System Admin', ADMIN: 'System Admin' };

export default function Users() {
  const [rows, setRows] = useState(null);
  const [form, setForm] = useState(initial);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const load = () => api.get('/admin/users').then((response) => setRows(response.data)).catch((e) => setError(e.response?.data?.detail || e.message));
  useEffect(() => { load(); }, []);
  const change = (key) => (event) => setForm({ ...form, [key]: event.target.value });
  const create = async (event) => {
    event.preventDefault();
    setError('');
    setMessage('');
    try {
      await api.post('/admin/users', form);
      setForm(initial);
      setMessage('Account created. The user can sign in using the selected role workspace.');
      load();
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not create account');
    }
  };
  const remove = async (row) => {
    if (!window.confirm(`Delete ${row.name || row.email}? This cannot be undone.`)) return;
    setError('');
    setMessage('');
    try {
      await api.delete(`/admin/users/${row._id}`);
      setRows((current) => current.filter((item) => item._id !== row._id));
      setMessage('User deleted.');
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not delete user');
    }
  };
  const columns = [['name', 'Name'], ['email', 'Email'], ['role', 'Role', (value) => roleLabels[value] || value], ['department', 'Department'], ['is_active', 'Active', (value) => value === false ? 'No' : 'Yes'], ['actions', 'Actions', (_, row) => <Button color="error" size="small" onClick={() => remove(row)}>Delete</Button>]];
  return <><PageHeader title="User management" description="Create and manage accounts for the four supported application roles." /><Card sx={{ mb: 3 }}><CardContent><Typography variant="h6" sx={{ mb: .5 }}>Add user</Typography><Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>New public accounts are Employees. Use this form for Finance Manager, CFO, and System Admin accounts.</Typography><Stack component="form" onSubmit={create} direction={{ xs: 'column', md: 'row' }} spacing={1.5}><TextField label="Name" value={form.name} onChange={change('name')} required /><TextField label="Email" type="email" value={form.email} onChange={change('email')} required /><TextField label="Temporary password" type="password" value={form.password} onChange={change('password')} required inputProps={{ minLength: 8 }} /><TextField select label="Role" value={form.role} onChange={change('role')} sx={{ minWidth: 190 }}>{[['EMPLOYEE', 'Employee'], ['FINANCE_MANAGER', 'Finance Manager'], ['CFO', 'CFO'], ['SYSTEM_ADMIN', 'System Admin']].map(([value, label]) => <MenuItem key={value} value={value}>{label}</MenuItem>)}</TextField><TextField label="Department" value={form.department} onChange={change('department')} required /><Button type="submit" variant="contained">Add user</Button></Stack></CardContent></Card>{message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}{error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}<Divider sx={{ mb: 2 }} /><Typography variant="h6" sx={{ mb: 1.5 }}>Added users</Typography>{!rows ? <Loading /> : <DataTable rows={rows} columns={columns} />}</>;
}
