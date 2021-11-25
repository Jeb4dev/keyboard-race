import React from 'react';
import { Link } from 'react-router-dom';
import { Box, Button, Center, Flex, Heading, Spacer, Tag, Text } from '@chakra-ui/react';
import { IRoom } from '../sockets/context';

interface RoomCardProps {
  roomId: number;
  room: IRoom;
}

function RoomCard({ room, roomId }: RoomCardProps) {
  return (
    <Box maxW="sm" borderWidth="1px" borderRadius="lg" overflow="hidden" p="5">
      <Flex direction="column" h="100%">
        <Box>
          <Text>Race</Text>
        </Box>
        <Center>
          <Heading>{room.room_title}</Heading>
        </Center>
        <Spacer />
        <Box>
          <Flex>
            <Box>
              <Link to={`/race/${roomId}`}>
                <Button>Join</Button>
              </Link>
            </Box>
            <Spacer />
            <Center>
              <Tag h="4">{room.users.length} racers</Tag>
            </Center>
          </Flex>
        </Box>
      </Flex>
    </Box>
  );
}

export default RoomCard;
