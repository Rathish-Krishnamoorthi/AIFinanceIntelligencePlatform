import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import useAuth from '../hooks/useAuth';
export default function Navbar() { const { user, logout } = useAuth(); return <AppBar position="fixed"><Toolbar><Typography variant="h6" sx={{ flexGrow: 1 }}>FinSight AI</Typography><Typography sx={{ mr: 2 }}>{user?.name}</Typography><Button color="inherit" onClick={logout}>Sign out</Button></Toolbar></AppBar>; }
