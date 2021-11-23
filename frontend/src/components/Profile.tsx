import React from 'react';
import { useStore } from 'effector-react';
import { Box, Button, Center, Heading } from '@chakra-ui/react';

import { $account, logout } from '../store/account';

function Profile() {
  const store = useStore($account);
  return (
    <Box>
      <Heading textAlign="center">{store.username}</Heading>
      <Center pt="4">
        <Button onClick={() => logout()} bgColor="red.600">
          Logout
        </Button>
      </Center>
    </Box>
  );
}

export default Profile;
