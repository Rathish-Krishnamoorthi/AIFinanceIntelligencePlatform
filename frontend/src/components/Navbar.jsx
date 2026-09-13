import React from 'react';
import { AccountCircle, Logout, NotificationsNone, Search } from '@mui/icons-material';
import { AppBar, Avatar, Button, IconButton, InputBase, Stack, Toolbar, Typography } from '@mui/material';
import useAuth from '../hooks/useAuth';
export default function Navbar({ pageTitle = 'Dashboard', collapsed = false, onProfileClick }) {
  const { user, logout } = useAuth();
  return <AppBar position="fixed" elevation={0} sx={{ zIndex: 1300, ml: { xs: 0, md: collapsed ? '76px' : '248px' }, width: { xs: '100%', md: collapsed ? 'calc(100% - 76px)' : 'calc(100% - 248px)' }, bgcolor: 'rgba(255,255,255,0.92)', color: 'text.primary', borderBottom: '1px solid rgba(23,48,66,0.08)', backdropFilter: 'blur(14px)', transition: 'margin-left 180ms ease, width 180ms ease' }}>
    <Toolbar sx={{ minHeight: '72px !important', px: { xs: 2, md: 4 } }}>
      <Stack direction="row" alignItems="center" spacing={1.5} sx={{ flexGrow: 1 }}>
        <Typography color="text.secondary" sx={{ fontWeight: 700, fontSize: 14 }}>{pageTitle}</Typography>
      </Stack>
      <Stack direction="row" alignItems="center" spacing={1.25}>
        <Stack direction="row" alignItems="center" sx={{ display: { xs: 'none', sm: 'flex' }, bgcolor: '#f4f7f8', borderRadius: 2, px: 1.25, py: .5, width: 180 }}><Search sx={{ fontSize: 18, color: 'text.secondary' }} /><InputBase placeholder="Search" sx={{ ml: .75, fontSize: 13 }} /></Stack>
        <IconButton aria-label="Notifications" sx={{ color: 'text.secondary' }}><NotificationsNone /></IconButton>
        <Avatar onClick={onProfileClick} sx={{ width: 32, height: 32, bgcolor: 'primary.light', cursor: 'pointer' }}><AccountCircle fontSize="small" /></Avatar>
        <Typography onClick={onProfileClick} sx={{ display: { xs: 'none', sm: 'block' }, fontWeight: 700, fontSize: 14, cursor: 'pointer' }}>{user?.name}</Typography>
        <Button color="inherit" startIcon={<Logout fontSize="small" />} onClick={logout}>Sign out</Button>
      </Stack>
    </Toolbar>
  </AppBar>;
}
