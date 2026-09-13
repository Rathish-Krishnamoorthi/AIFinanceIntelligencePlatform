import React from 'react';
import useAuth from '../hooks/useAuth';
import { hasPermission } from './permissions';

export default function PermissionGate({ permission, children, fallback = null }) {
  const { user } = useAuth();
  return hasPermission(user, permission) ? children : fallback;
}
