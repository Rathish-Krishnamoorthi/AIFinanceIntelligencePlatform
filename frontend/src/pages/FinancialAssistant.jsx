import React, { useEffect, useState } from 'react';
import { Alert, Box, Button, Card, CardContent, Chip, Stack, TextField, Typography } from '@mui/material';
import api from '../services/api';
import useAuth from '../hooks/useAuth';

export default function FinancialAssistant() {
  const { user } = useAuth();
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [workflows, setWorkflows] = useState([]);
  const [error, setError] = useState('');
  const load = () => api.get('/assistant/workflows').then((response) => setWorkflows(response.data.actions)).catch((e) => setError(e.response?.data?.detail || e.message));
  useEffect(load, []);
  const ask = async () => { try { setAnswer((await api.post('/assistant/chat', { question })).data); } catch (e) { setError(e.response?.data?.detail || 'Assistant request failed'); } };
  return <><Typography variant="h4" gutterBottom>AI Financial Operations Agent</Typography><Typography color="text.secondary" sx={{ mb: 3 }}>Grounded in your database: expense triage, invoice validation, and approval workflows.</Typography>{error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}<Stack spacing={2} sx={{ mb: 3 }}>{workflows.map((item) => <Card key={item.type}><CardContent sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 2 }}><Box><Typography fontWeight={700}>{item.label}</Typography><Typography variant="body2" color="text.secondary">{item.count} records in {user?.department || 'your visible scope'}</Typography></Box><Chip label={item.automatable ? 'Automatable' : 'Review required'} color={item.automatable ? 'success' : 'warning'} variant="outlined" /></CardContent></Card>)}</Stack><Card><CardContent><TextField fullWidth multiline value={question} onChange={(e) => setQuestion(e.target.value)} label="Ask about live expenses, invoices, vendors, or risk" /><Button onClick={ask} variant="contained" sx={{ mt: 2 }} disabled={!question.trim()}>Ask agent</Button>{answer && <Typography sx={{ mt: 3 }}><b>{answer.answer}</b><br />Evidence: {answer.evidence.join(' · ')}<br />Reasoning: {answer.reasoning}</Typography>}</CardContent></Card></>;
}
