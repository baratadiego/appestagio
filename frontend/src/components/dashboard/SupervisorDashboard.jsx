import React from 'react';
export default function SupervisorDashboard({ user }) {
  return (
    <div>
      <h2>Bem-vindo, {user.first_name} (Supervisor)</h2>
      <p>Estatísticas mockadas: 4 estagiários supervisionados, 2 avaliações pendentes.</p>
      <ul>
        <li>Tarefa: Avaliar estágio de Bruno Oliveira</li>
        <li>Tarefa: Validar plano de estágio de Carla Costa</li>
      </ul>
    </div>
  );
}

async function fetchData() {
  const response = await fetch('/api/v1/me/');
  const data = await response.json();
  return data;
}

async function fetchNotifications() {
  const response = await fetch('/api/v1/notifications/');
  const notifications = await response.json();
  return notifications;
}