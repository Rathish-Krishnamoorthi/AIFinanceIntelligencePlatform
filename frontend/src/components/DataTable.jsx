import React from 'react';
import { Card, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material';
export default function DataTable({ rows = [], columns }) {
  return <Card><Table size="small"><TableHead><TableRow>{columns.map(([key, label]) => <TableCell key={key}>{label}</TableCell>)}</TableRow></TableHead><TableBody>{rows.map((row, index) => <TableRow key={row._id || index}>{columns.map(([key, , render]) => <TableCell key={key}>{render ? render(row[key], row) : row[key]}</TableCell>)}</TableRow>)}</TableBody></Table></Card>;
}
