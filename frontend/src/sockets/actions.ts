import { Socket } from 'socket.io-client';

export const getRooms = (socket?: Socket) => {
  console.log(123);
  socket?.emit('sv_get_active_rooms');
};

export const createRace = (socket?: Socket) => {
  socket?.emit('sv_create_race');
};

export const joinRace = (socket: Socket | undefined, room: number) => {
  socket?.emit('sv_join_race', {
    room,
  });
};

export const leaveRace = (socket: Socket | undefined, room: number) => {
  socket?.emit('sv_leave_race', {
    room,
  });
};

export const startRace = (socket?: Socket) => {
  socket?.emit('sv_start_race');
};
