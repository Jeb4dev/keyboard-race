import React from 'react';
import { useForm } from 'react-hook-form';
import { Box, Button, Flex, FormControl, FormLabel, Heading, Input, Link, Spacer, Text } from '@chakra-ui/react';

import { $account, register as registerEvent } from '../../store/account';
import { useStore } from 'effector-react';

type RegisterValues = {
  username: string;
  password: string;
};

function Register() {
  const store = useStore($account);
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<RegisterValues>();

  const onSubmit = (data: RegisterValues) => {
    registerEvent(data);
    setError('username', { message: store.error });
  };

  console.log(errors);

  return (
    <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p="6">
      <Heading textAlign="center" fontSize="3xl" pb="4">
        Register
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
            placeholder="ivan-smith"
          />
        </FormControl>
        <FormControl id="password-input" isRequired>
          <FormLabel>Password</FormLabel>
          <Input
            {...register('password', {
              required: true,
            })}
            type="password"
            placeholder="Str0ng_p@ssw0rd"
          />
        </FormControl>
        <Flex pt="4">
          <Button type="submit">Register</Button>
          <Spacer />
          <Box p="2">
            <Link>Login</Link>
          </Box>
        </Flex>
      </form>
    </Box>
  );
}

export default Register;
