import React from 'react';
import { useSocket } from '../sockets/useSocket';
import RoomCard from '../components/RoomCard';
import { Center, Heading, Link, SimpleGrid } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import { useStore } from 'effector-react';
import { $account } from '../store/account';

function HomePage() {
  const { socket, rooms } = useSocket();
  const account = useStore($account);

  return (
    <>
      <Center>
        <Heading mb="5" textAlign="center">
          Users rooms
        </Heading>
      </Center>
      {account.id === 0 ? (
        <Heading fontSize="2xl" textAlign="center">
          Register or Login to see active rooms
        </Heading>
      ) : (
        <>
          {Object.keys(rooms).length === 0 ? (
            <Center h="70vh">
              <Heading fontSize="2xl" textAlign="center">
                There are no active sessions,{' '}
                <Link as={RouterLink} color="teal.500" to={`/race/${account.id}`}>
                  create one
                </Link>
              </Heading>
            </Center>
          ) : (
            <SimpleGrid minChildWidth="300px" spacing={5}>
              {Object.keys(rooms).map((roomId) => (
                <RoomCard roomId={roomId as unknown as number} room={rooms[roomId as unknown as number]} />
              ))}
            </SimpleGrid>
          )}
        </>
      )}
    </>
  );
}

export default HomePage;
