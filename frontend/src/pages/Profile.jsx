import React, { useEffect, useState } from 'react';
import { Alert, Avatar, Button, Card, CardContent, Divider, Stack, TextField, Typography } from '@mui/material';
import api from '../services/api';
import Loading from '../components/Loading';
import PageHeader from '../components/PageHeader';
import useAuth from '../hooks/useAuth';

const roleLabels = { EMPLOYEE: 'Employee', ACCOUNTANT: 'Employee', FINANCE_MANAGER: 'Finance Manager', CFO: 'CFO', SYSTEM_ADMIN: 'System Admin', ADMIN: 'System Admin', AUDITOR: 'CFO' };

export default function Profile() {
  const { updateUser } = useAuth();
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ name: '', department: '', job_title: '', phone: '' });
  const [image, setImage] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/auth/profile').then(({ data }) => {
      setProfile(data);
      setForm({ name: data.name || '', department: data.department || '', job_title: data.job_title || '', phone: data.phone || '' });
      setImage(data.profile_image || '');
    }).catch((e) => setError(e.response?.data?.detail || 'Could not load profile'));
  }, []);

  const change = (key) => (event) => setForm({ ...form, [key]: event.target.value });
  const chooseImage = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) return setError('Please select an image file');
    if (file.size > 2_000_000) return setError('Profile image must be 2 MB or smaller');
    const reader = new FileReader();
    reader.onload = () => { setImage(String(reader.result)); setError(''); };
    reader.onerror = () => setError('Could not read the selected image');
    reader.readAsDataURL(file);
  };
  const save = async (event) => {
    event.preventDefault();
    setMessage('');
    setError('');
    try {
      const { data } = await api.put('/auth/profile', { ...form, profile_image: image || null });
      setProfile(data);
      updateUser(data);
      setMessage('Profile updated successfully.');
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not update profile');
    }
  };

  if (!profile) return error ? <Alert severity="error">{error}</Alert> : <Loading />;
  return <><PageHeader title="My profile" description="Manage your account details, role information, and profile image." /><Stack direction="column" spacing={3} sx={{ width: '100%' }}><Card sx={{ width: '100%' }}><CardContent><Stack alignItems="center" spacing={1.5}><Avatar src={image || undefined} sx={{ width: 112, height: 112, bgcolor: 'primary.main', fontSize: 42 }}>{profile.name?.[0]?.toUpperCase()}</Avatar><Button component="label" variant="outlined">Choose profile image<input hidden type="file" accept="image/png,image/jpeg,image/webp" onChange={chooseImage} /></Button><Typography variant="h6">{profile.name}</Typography><Typography color="text.secondary">{roleLabels[profile.role] || profile.role}</Typography></Stack></CardContent></Card><Card sx={{ width: '100%' }}><CardContent><Typography variant="h6" sx={{ mb: 2 }}>Account details</Typography><Stack component="form" onSubmit={save} spacing={2}><TextField label="Full name" value={form.name} onChange={change('name')} required fullWidth /><TextField label="Email" value={profile.email} disabled fullWidth /><TextField label="Role" value={roleLabels[profile.role] || profile.role} disabled fullWidth /><TextField label="Department" value={form.department} onChange={change('department')} fullWidth /><TextField label="Job title" value={form.job_title} onChange={change('job_title')} placeholder="e.g. Senior Accountant" fullWidth /><TextField label="Phone" value={form.phone} onChange={change('phone')} fullWidth /><Button type="submit" variant="contained">Save profile</Button></Stack></CardContent></Card><Card sx={{ width: '100%' }}><CardContent><Typography variant="h6" sx={{ mb: 2 }}>Role access</Typography><Typography variant="body2"><strong>Workspace:</strong> {roleLabels[profile.role] || profile.role}</Typography><Typography variant="body2"><strong>Organization:</strong> {profile.organization_id || 'Not assigned'}</Typography><Typography variant="body2"><strong>Account status:</strong> {profile.is_active ? 'Active' : 'Inactive'}</Typography><Divider sx={{ my: 2 }} /><Typography variant="body2" color="text.secondary">Permissions are managed by your administrator and cannot be changed from this page.</Typography></CardContent></Card></Stack>{message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}{error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}</>;
}
