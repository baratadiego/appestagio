import React, { useEffect, useState } from 'react';

export default function NotificationsBadge() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    fetch('/api/notifications/?read=false', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('access') }
    })
      .then(res => res.json())
      .then(data => setCount(data.length));
  }, []);

  return (
    <span>
      Notificações
      {count > 0 && <span className="badge">{count}</span>}
    </span>
  );
}