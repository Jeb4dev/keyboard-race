import React from 'react';
import { useSocket } from '../sockets/useSocket';
import RoomCard from '../components/RoomCard';

function HomePage() {
  const { socket, rooms } = useSocket();

  console.log(rooms);

  return (
    <>
      {Object.keys(rooms).map((roomId) => (
        <RoomCard roomId={roomId as unknown as number} room={rooms[roomId as unknown as number]} />
      ))}
    </>
  );
}

export default HomePage;
