import React, { useState, useEffect, createContext, useRef } from 'react';
import { connect, Socket } from 'socket.io-client';

import { getAuthHeaders } from '../store/api';

interface ISocketContext {
  rooms: any;
  socket: Socket | undefined;
}

export const SocketContext = createContext<ISocketContext>({
  rooms: [],
  socket: {} as Socket,
} as ISocketContext);

interface SocketProviderProps {
  children: React.ReactNode;
}

function SocketProvider({ children }: SocketProviderProps) {
  const socketRef = useRef<Socket>();

  const [rooms, setRooms] = useState<any>({});
  useEffect(() => {
    socketRef.current = connect(import.meta.env.VITE_SOCKET_URL, {
      forceNew: true,
      extraHeaders: getAuthHeaders(),
    });
    const socket = socketRef.current;

    socket.on('connect', () => {
      console.log('conn');
      socket.emit('sv_get_active_rooms');
    });
    socket.on('sv_get_active_rooms', (activeRooms) => {
      console.log('rooms', activeRooms);
      setRooms(activeRooms);
    });
    socket.on('cl_create_race', (userId) => {
      setRooms({ ...rooms, [userId]: {} });
    });
  }, []);

  return (
    <SocketContext.Provider
      value={{
        socket: socketRef.current,
        rooms,
      }}
    >
      {children}
    </SocketContext.Provider>
  );
}

export default SocketProvider;
