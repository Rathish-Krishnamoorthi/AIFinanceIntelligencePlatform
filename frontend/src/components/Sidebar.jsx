import React from 'react';
import { AdminPanelSettings, AutoGraph, BugReport, Checklist, DashboardRounded, ListAlt, Menu, NotificationsNone, PeopleAlt, ReceiptLong, Savings, Security, SmartToy, SwapHoriz } from '@mui/icons-material';
import { Box, Divider, Drawer, IconButton, List, ListItemButton, ListItemIcon, ListItemText, Typography } from '@mui/material';

const icons = { dashboard: DashboardRounded, transactions: SwapHoriz, invoices: ReceiptLong, vendors: PeopleAlt, anomalies: BugReport, cash: AutoGraph, budgets: Savings, risk: Security, approvals: Checklist, assistant: SmartToy, notifications: NotificationsNone, audit: ListAlt, users: AdminPanelSettings };

export default function Sidebar({ items, page, onNavigate, onToggle, collapsed = false }) {
  const sections = [['Overview', ['dashboard']], ['Financial', ['transactions', 'invoices', 'vendors']], ['Intelligence', ['anomalies', 'cash', 'budgets', 'risk']], ['Operations', ['approvals', 'notifications', 'audit']], ['Administration', ['users']], ['AI', ['assistant']]];
  const itemMap = Object.fromEntries(items);
  return <Drawer variant="permanent" sx={{ display: { xs: 'none', md: 'block' }, '& .MuiDrawer-paper': { width: collapsed ? 76 : 248, overflowX: 'hidden', boxSizing: 'border-box', border: 0, borderRight: '1px solid rgba(23,48,66,0.07)', bgcolor: '#fbfcfc', pt: 9, transition: 'width 180ms ease' } }}>
    <Box sx={{ mx: 1.5, mt: 1.5, mb: 1.25, px: collapsed ? .75 : 1.25, py: 1, borderRadius: 3, bgcolor: 'rgba(23,107,135,.045)', border: '1px solid rgba(23,107,135,.08)', whiteSpace: 'nowrap' }}>
      <Box sx={{ display: 'flex', justifyContent: collapsed ? 'center' : 'flex-end', height: 30 }}>
        <IconButton aria-label="Toggle navigation" onClick={onToggle} size="small" sx={{ color: 'primary.main', bgcolor: 'rgba(23,107,135,.09)', '&:hover': { bgcolor: 'rgba(23,107,135,.16)' } }}><Menu fontSize="small" /></IconButton>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: collapsed ? 'center' : 'flex-start', gap: 1.25, pt: .75 }}>
        <span className="brand-mark" style={{ width: 34, height: 34, borderRadius: 10 }}>F</span>
        {!collapsed && <Typography variant="h6" sx={{ color: 'text.primary', fontWeight: 800, letterSpacing: '-0.03em' }}>Fintel</Typography>}
      </Box>
    </Box>
    <Divider sx={{ mx: 2, mb: 1 }} />
    {sections.map(([section, keys]) => { const visibleKeys = keys.filter((key) => itemMap[key]); if (!visibleKeys.length) return null; return <Box key={section} sx={{ mb: 1 }}><Typography variant="caption" sx={{ display: collapsed ? 'none' : 'block', px: 3, color: 'text.secondary', fontWeight: 800, letterSpacing: '.08em' }}>{section}</Typography><List sx={{ px: 1.5, pt: .5 }}>{visibleKeys.map((key) => { const Icon = icons[key] || DashboardRounded; return <ListItemButton key={key} selected={page === key} onClick={() => onNavigate(key)} title={collapsed ? itemMap[key] : undefined} sx={{ borderRadius: 2, mb: .25, minHeight: 40, justifyContent: collapsed ? 'center' : 'initial', px: collapsed ? 1.5 : 2, '&.Mui-selected': { bgcolor: 'rgba(23,107,135,.1)', color: 'primary.main', '&:hover': { bgcolor: 'rgba(23,107,135,.14)' } }, '&:hover': { bgcolor: 'rgba(23,107,135,.05)' } }}><ListItemIcon sx={{ minWidth: collapsed ? 0 : 38, color: 'inherit' }}><Icon fontSize="small" /></ListItemIcon>{!collapsed && <ListItemText primary={itemMap[key]} primaryTypographyProps={{ fontWeight: page === key ? 700 : 600, fontSize: 14 }} />}</ListItemButton>; })}</List></Box>; })}
  </Drawer>;
}
