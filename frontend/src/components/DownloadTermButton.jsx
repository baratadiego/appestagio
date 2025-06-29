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