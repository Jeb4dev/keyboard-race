import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useStore } from 'effector-react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Button, Flex, FormControl, FormLabel, Heading, Input, Link, Spacer, Text } from '@chakra-ui/react';

import { $account, login, register as registerEvent, fetchAccount } from '../../store/account';
import { useNavigate } from 'react-router';

type AuthValues = {
  username: string;
  password: string;
};

interface AuthProps {
  authType: 'login' | 'register';
}

function AuthForm({ authType }: AuthProps) {
  const store = useStore($account);
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
    reset,
  } = useForm<AuthValues>();

  useEffect(() => {
    if (store.id !== 0) {
      // fetchAccount();
      navigate('/account');
    }
  }, [store.id]);

  useEffect(() => {
    reset();
  }, [authType]);

  const onSubmit = (data: AuthValues) => {
    if (authType === 'login') login(data);
    else registerEvent(data);
    setError('username', { message: store.error });
  };

  const name = authType[0].toUpperCase() + authType.slice(1);
  const opposite = authType === 'login' ? 'register' : 'login';
  const oppositeName = opposite[0].toUpperCase() + opposite.slice(1);

  return (
    <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p="6">
      <Heading textAlign="center" fontSize="3xl" pb="4">
        {name}
      </Heading>
      <Text textAlign="center" color="red.400">
        {errors.username?.message}
      </Text>
      <form onSubmit={handleSubmit(onSubmit)}>
        <FormControl id="username-input" isRequired pb="2">
          <FormLabel>Username</FormLabel>
          <Input
            {...register('username', {
              required: true,
            })}
            placeholder="Your username"
          />
        </FormControl>
        <FormControl id="password-input" isRequired>
          <FormLabel>Password</FormLabel>
          <Input
            {...register('password', {
              required: true,
            })}
            type="password"
            placeholder="Your password"
          />
        </FormControl>
        <Flex pt="4">
          <Button type="submit">{name}</Button>
          <Spacer />
          <Box p="2">
            <Link as={RouterLink} to={`/account/${opposite}`}>
              {oppositeName}
            </Link>
          </Box>
        </Flex>
      </form>
    </Box>
  );
}

export default AuthForm;
