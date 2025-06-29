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