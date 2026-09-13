import React from 'react';
import { Card, Table, TableHead, TableRow, TableCell, TableBody, TableContainer } from '@mui/material';
import EmptyState from './EmptyState';
export default function DataTable({ rows = [], columns }) {
  if (!rows.length) return <Card><EmptyState /></Card>;
  return <Card><TableContainer><Table size="small"><TableHead><TableRow>{columns.map(([key, label]) => <TableCell key={key}>{label}</TableCell>)}</TableRow></TableHead><TableBody>{rows.map((row, index) => <TableRow hover key={row._id || index}>{columns.map(([key, , render]) => <TableCell key={key} sx={{ py: 1.7, whiteSpace: 'nowrap' }}>{render ? render(row[key], row) : row[key]}</TableCell>)}</TableRow>)}</TableBody></Table></TableContainer></Card>;
}
