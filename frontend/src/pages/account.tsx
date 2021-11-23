import React from 'react';
import { useStore } from 'effector-react';
import { Center } from '@chakra-ui/react';

import { $account } from '../store/account';

import Profile from '../components/Profile';
import Register from '../components/forms/Register';

function AccountPage() {
  const store = useStore($account);

  if (store.id !== 0) {
    return <Profile />;
  }

  return (
    <Center>
      <Register />
    </Center>
  );
}

export default AccountPage;
