import React, { createContext, useContext, useEffect, useState } from 'react';
import api from '../services/api';
import { PERMISSIONS } from '../auth/permissions';

const AuthContext = createContext(null);
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem('token')));
  useEffect(() => {
    if (!localStorage.getItem('token')) return setLoading(false);
    api.get('/auth/me').then((response) => setUser(hydrate(response.data))).catch(() => {
      localStorage.removeItem('token');
      setUser(null);
    }).finally(() => setLoading(false));
  }, []);
  const hydrate = (value) => value ? { ...value, permissions: value.permissions || PERMISSIONS[value.role] || [] } : null;
  const login = (data) => { localStorage.setItem('token', data.access_token); setUser(hydrate(data.user)); };
  const updateUser = (data) => setUser((current) => hydrate({ ...current, ...data }));
  const logout = () => { localStorage.removeItem('token'); setUser(null); };
  return <AuthContext.Provider value={{ user, loading, login, updateUser, logout, isAuthenticated: Boolean(user), permissions: user?.permissions || [] }}>{children}</AuthContext.Provider>;
}
export default AuthContext;
