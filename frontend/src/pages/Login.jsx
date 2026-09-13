import React, { useState } from 'react';
import { Alert, Box, Button, Card, CardContent, Divider, Stack, TextField, Typography } from '@mui/material';
import api, { apiErrorMessage } from '../services/api';
import useAuth from '../hooks/useAuth';

export default function Login({ workspaceLabel = 'Fintel' }) {
  const { login } = useAuth();
  const [register, setRegister] = useState(false);
  const [name, setName] = useState('');
  const [department, setDepartment] = useState('General');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const submit = async (event) => {
    event.preventDefault();
    try {
      const normalizedEmail = email.trim().toLowerCase();
      const response = register
        ? await api.post('/auth/register', { name: name.trim(), email: normalizedEmail, password, department: department.trim() })
        : await api.post('/auth/login', new URLSearchParams({ username: normalizedEmail, password }));
      login(response.data);
    } catch (e) {
      setError(apiErrorMessage(e));
    }
  };
  return <Box className="login"><Card><CardContent>
    <Stack direction="row" spacing={1.5} alignItems="center"><span className="brand-mark">F</span><Typography variant="h4" color="primary">Fintel</Typography></Stack>
    <Typography color="text.secondary" sx={{ mt: 2 }}>{workspaceLabel === 'Fintel' ? 'Financial intelligence for confident decisions.' : `Sign in to the ${workspaceLabel} workspace.`}</Typography>
    <Box component="form" onSubmit={submit} sx={{ mt: 3, display: 'grid', gap: 2 }}>
      {register && <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} required />}
      <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      {register && <TextField label="Department" value={department} onChange={(e) => setDepartment(e.target.value)} required />}
      {error && <Alert severity="error">{error}</Alert>}
      <Button type="submit" variant="contained" size="large">{register ? 'Create account' : 'Sign in'}</Button>
    </Box>
    <Divider sx={{ my: 3 }} />
    <Button size="small" onClick={() => { setRegister(!register); setError(''); }}>{register ? 'Already have an account? Sign in' : 'Create a new account'}</Button>
  </CardContent></Card></Box>;
}
