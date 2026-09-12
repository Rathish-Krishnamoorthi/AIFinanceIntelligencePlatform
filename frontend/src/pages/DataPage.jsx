import React, { useEffect, useState } from 'react';
import { Typography } from '@mui/material';
import api from '../services/api';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import DataTable from '../components/DataTable';
export default function DataPage({ title, endpoint, columns }) {
  const [rows, setRows] = useState(null); const [error, setError] = useState('');
  useEffect(() => { api.get(endpoint).then((r) => setRows(r.data)).catch((e) => setError(e.response?.data?.detail || e.message)); }, [endpoint]);
  return <><Typography variant="h4" gutterBottom>{title}</Typography><ErrorMessage message={error} />{!rows ? <Loading /> : <DataTable rows={rows} columns={columns} />}</>;
}
