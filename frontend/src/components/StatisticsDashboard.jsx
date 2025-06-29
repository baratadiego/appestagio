import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';

const StatisticsDashboard = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/v1/estatisticas/')
      .then(res => res.json())
      .then(setData)
      .catch(setError);
  }, []);

  if (error) return <div>Erro ao carregar estatísticas.</div>;
  if (!data) return <div>Carregando...</div>;

  return (
    <div>
      <Bar data={{
        labels: data.labels || [],
        datasets: [
          {
            label: 'Estatísticas',
            data: data.values || [],
            backgroundColor: 'rgba(75,192,192,0.4)',
          }
        ]
      }} />
    </div>
  );
};

export default StatisticsDashboard;
