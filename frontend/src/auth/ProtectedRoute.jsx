import React from 'react';
import useAuth from '../hooks/useAuth';
import { hasPermission } from './permissions';
import Loading from '../components/Loading';

export default function ProtectedRoute({ permission, children }) {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  if (!user) return <AccessDenied message="Please sign in to continue." />;
  if (permission && !hasPermission(user, permission)) {
    return <AccessDenied message="You do not have permission to access this area." />;
  }
  return children;
}

function AccessDenied({ message }) {
  return <div role="alert" style={{ padding: 40, textAlign: 'center' }}><h2>Access denied</h2><p>{message}</p></div>;
}
