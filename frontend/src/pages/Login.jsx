import React, { useState } from 'react';
import { Alert, Box, Button, Card, CardContent, TextField, Typography } from '@mui/material';
import api from '../services/api';
import useAuth from '../hooks/useAuth';
export default function Login() { const { login } = useAuth(); const [email, setEmail] = useState('demo@finsight.ai'); const [password, setPassword] = useState('Demo123!'); const [error, setError] = useState('');
  const submit = async (event) => { event.preventDefault(); try { const response = await api.post('/auth/login', new URLSearchParams({ username: email, password })); login(response.data); } catch (e) { setError(e.response?.data?.detail || 'Login failed'); } };
  return <Box className="login"><Card><CardContent><Typography variant="h4" color="primary">FinSight AI</Typography><Typography color="text.secondary">Financial intelligence for confident decisions</Typography><Box component="form" onSubmit={submit} sx={{ mt: 3, display: 'grid', gap: 2 }}><TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} /><TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />{error && <Alert severity="error">{error}</Alert>}<Button type="submit" variant="contained">Sign in</Button></Box><Typography variant="caption">Demo: demo@finsight.ai / Demo123!</Typography></CardContent></Card></Box>;
}
