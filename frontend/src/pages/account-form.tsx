import React from 'react';
import { useParams } from 'react-router';
import { Center } from '@chakra-ui/react';

import AuthForm from '../components/forms/AuthForm';

function AccountFormPage() {
  const { form } = useParams();

  if (form !== 'login' && form !== 'register') {
    return <Center>Page not found</Center>;
  }

  return (
    <Center>
      <AuthForm authType={form as 'login' | 'register'} />
    </Center>
  );
}

export default AccountFormPage;
