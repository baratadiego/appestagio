import React from 'react';

export default function CoordenadorDashboard({ user }) {
  return (
    <div>
      <h2>Bem-vindo, {user.first_name} (Coordenador)</h2>
      {/* Botões de ação rápida */}
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => window.location.href = '/novo-estagiario'}>
          Novo Estagiário
        </button>
        <button onClick={() => window.location.href = '/novo-convenio'}>
          Novo Convênio
        </button>
      </div>
      <p>Estatísticas mockadas: 12 estágios em andamento, 3 convênios aguardando aprovação.</p>
      <ul>
        <li>Tarefa: Aprovar convênio "Inovação Digital"</li>
        <li>Tarefa: Revisar relatório de Ana Carolina</li>
      </ul>
    </div>
  );
}