import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Flex, Heading, Spacer, Box, Button } from '@chakra-ui/react';
import { FaSignInAlt, FaUser } from 'react-icons/fa';

function Header() {
  const isAuthorized = false;

  return (
    <Container maxW="container.xl">
      <Flex>
        <Link to="/">
          <Heading as="h1" size="xl">
            Keyboard Race
          </Heading>
        </Link>
        <Spacer />
        <Box p="2">
          <Button>Create Race</Button>
        </Box>
        <Box p="2">
          <Link to="/account">
            <Button>{isAuthorized ? <FaUser /> : <FaSignInAlt />}</Button>
          </Link>
        </Box>
      </Flex>
    </Container>
  );
}

export default Header;
