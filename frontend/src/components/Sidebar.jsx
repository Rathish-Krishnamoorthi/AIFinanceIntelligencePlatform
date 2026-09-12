import React from 'react';
import { Drawer, List, ListItemButton, ListItemText } from '@mui/material';
export default function Sidebar({ items, page, onNavigate }) { return <Drawer variant="permanent" sx={{ '& .MuiDrawer-paper': { width: 220, boxSizing: 'border-box' } }}><List sx={{ mt: 8 }}>{items.map(([key, label]) => <ListItemButton key={key} selected={page === key} onClick={() => onNavigate(key)}><ListItemText primary={label} /></ListItemButton>)}</List></Drawer>; }
