import { Navigate, Outlet } from 'react-router-dom';

export function RotaProtegida() {
  const token = localStorage.getItem('authToken');

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}