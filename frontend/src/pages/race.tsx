import React, { useEffect } from 'react';
import { useParams } from 'react-router';
import { useStore } from 'effector-react';
import { Heading } from '@chakra-ui/react';

import { useSocket } from '../sockets/useSocket';
import { createRace, joinRace } from '../sockets/actions';

import { $account } from '../store/account';
import Room from '../components/Room';

function RacePage() {
  const account = useStore($account);
  const { socket, rooms } = useSocket();
  const params = useParams();
  const userId = parseInt(params.userId || '-1');

  useEffect(() => {
    if (socket) {
      if (account.id === userId) {
        if (!rooms[userId]) {
          createRace(socket);
          joinRace(socket, userId);
        }
      } else if (rooms[userId] && !rooms[userId].users.includes(account.id)) {
        joinRace(socket, userId);
      }
    }
  }, [socket, userId, rooms, account.id]);

  if (!rooms[userId]) {
    return <Heading textAlign="center">Room not found</Heading>;
  }

  return <Room roomId={userId} room={rooms[userId]} isOwner={account.id === userId} />;
}

export default RacePage;
