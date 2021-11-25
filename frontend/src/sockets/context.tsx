import React, { useState, useEffect, createContext, useRef } from 'react';
import { connect, Socket } from 'socket.io-client';

import { getAuthHeaders } from '../store/api';
import { getRooms } from './actions';

interface ISocketContext {
  rooms: IRooms;
  socket: Socket | undefined;
}

export interface IRoom {
  users: number[];
  room_title: string;
  started: boolean;
  words: {
    words_title: string;
    words: string;
  };
  time_start: number;
}

type IRooms = Record<number, IRoom>;

export const SocketContext = createContext<ISocketContext>({
  rooms: [],
  socket: {} as Socket,
} as ISocketContext);

interface SocketProviderProps {
  children: React.ReactNode;
}

function SocketProvider({ children }: SocketProviderProps) {
  const socketRef = useRef<Socket>();

  const [rooms, setRooms] = useState<IRooms>({});
  useEffect(() => {
    socketRef.current = connect(import.meta.env.VITE_SOCKET_URL, {
      forceNew: true,
      extraHeaders: getAuthHeaders(),
    });
    const socket = socketRef.current;

    const roomsUpdate = () => getRooms(socket);

    socket
      .on('connect', () => {
        console.log('conn');
        socket.emit('sv_get_active_rooms');
      })
      .on('sv_get_active_rooms', (activeRooms) => {
        console.log('rooms', activeRooms);
        setRooms(activeRooms);
      })
      .on('cl_create_race', (newRooms) => {
        roomsUpdate();
      })
      .on('cl_join_race', roomsUpdate)
      .on('cl_user_left_race', roomsUpdate)
      .on('cl_start_race', roomsUpdate)
      .on('cl_user_should_update_rooms', roomsUpdate);
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
