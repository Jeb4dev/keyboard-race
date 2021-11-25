import React, { useEffect } from 'react';

import { useSocket } from '../sockets/useSocket';
import { createRace } from '../sockets/actions';

function RacePage() {
  const { socket, rooms } = useSocket();
  useEffect(() => {
    if (socket) createRace(socket);
  }, [socket]);

  return <></>;
}

export default RacePage;
