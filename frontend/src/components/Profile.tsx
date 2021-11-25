import React, { useEffect, useState } from 'react';
import { useStore } from 'effector-react';
import { Box, Button, Center, Heading, Table, TableCaption, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';

import { $account, logout } from '../store/account';
import { getStats, StatisticsResponse } from '../store/api/user';
import { formatTime } from './StopDialog';

function Profile() {
  const store = useStore($account);
  const [stats, setStats] = useState<StatisticsResponse | null>(null);

  useEffect(() => {
    (async () => {
      setStats(await getStats(store.id));
    })();
  }, [setStats, store.id]);

  return (
    <Box>
      <Heading textAlign="center">{store.username}</Heading>
      <Table variant="simple">
        <TableCaption>User Statistics</TableCaption>
        <Thead>
          <Tr>
            <Th>Field</Th>
            <Th>Value</Th>
          </Tr>
        </Thead>
        <Tbody>
          <Tr>
            <Td>Best speed(wpm)</Td>
            <Td>{stats?.statistics.best_wpm}</Td>
          </Tr>
          <Tr>
            <Td>Total races</Td>
            <Td>{stats?.statistics.total_races}</Td>
          </Tr>
          <Tr>
            <Td>Average speed(wpm)</Td>
            <Td>{stats?.statistics.average_wpm}</Td>
          </Tr>
          <Tr>
            <Td>Average time</Td>
            <Td>{stats?.statistics.average_time ? formatTime(stats?.statistics.average_time) : 0}</Td>
          </Tr>
        </Tbody>
      </Table>
      <Center pt="4">
        <Button onClick={() => logout()} bgColor="red.600">
          Logout
        </Button>
      </Center>
    </Box>
  );
}

export default Profile;
