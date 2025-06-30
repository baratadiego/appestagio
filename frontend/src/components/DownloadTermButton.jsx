import React from 'react';

export default function DownloadTermButton({ estagioId }) {
  const handleDownload = () => {
    window.open(`/api/v1/estagios/${estagioId}/download_term/`, '_blank');
  };

  return (
    <button onClick={handleDownload}>
      Download Termo de Compromisso (PDF)
    </button>
  );
}

const fetchData = async () => {
  const response = await fetch('/api/v1/me/');
  const data = await response.json();
  console.log(data);
};

const fetchNotifications = async () => {
  const response = await fetch('/api/v1/notifications/');
  const notifications = await response.json();
  console.log(notifications);
};