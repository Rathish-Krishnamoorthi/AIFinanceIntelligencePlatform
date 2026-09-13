import React, { useEffect, useState } from 'react';
import api from '../services/api';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import DataTable from '../components/DataTable';
import PageHeader from '../components/PageHeader';
export default function DataPage({ title, endpoint, columns }) {
  const [rows, setRows] = useState(null); const [error, setError] = useState('');
  useEffect(() => { api.get(endpoint).then((r) => setRows(r.data)).catch((e) => setError(e.response?.data?.detail || e.message)); }, [endpoint]);
  return <><PageHeader title={title} description="Monitor and understand the signals across your financial operations." action="Export report" /><ErrorMessage message={error} />{!rows ? <Loading /> : <DataTable rows={rows} columns={columns} />}</>;
}
