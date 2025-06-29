import React from 'react';
export default function AlunoDashboard({ user }) {
  return (
    <div>
      <h2>Bem-vindo, {user.first_name} (Aluno)</h2>
      <p>Estatísticas mockadas: 2 estágios ativos, 1 documento pendente.</p>
      <ul>
        <li>Tarefa: Enviar relatório final (prazo: 10/07/2025)</li>
        <li>Tarefa: Assinar termo de compromisso</li>
      </ul>
    </div>
  );
}