import React, { useEffect, useState } from 'react';
import AlunoDashboard from './dashboard/AlunoDashboard';
import CoordenadorDashboard from './dashboard/CoordenadorDashboard';
import SupervisorDashboard from './dashboard/SupervisorDashboard';

export default function DashboardRouter() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch('/api/me/', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('access') }
    })
      .then(res => res.json())
      .then(setUser);
  }, []);

  if (!user) return <div>Carregando...</div>;

  if (user.role === 'COORDENADOR') return <CoordenadorDashboard user={user} />;
  if (user.role === 'SUPERVISOR') return <SupervisorDashboard user={user} />;
  return <AlunoDashboard user={user} />;
}