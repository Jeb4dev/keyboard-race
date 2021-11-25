import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Flex, Heading, Spacer, Box, Button } from '@chakra-ui/react';
import { FaSignInAlt, FaUser } from 'react-icons/fa';
import { useStore } from 'effector-react';

import { $account } from '../store/account';
import { useNavigate, useLocation } from 'react-router';

function Header() {
  const store = useStore($account);
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthorized = store.id !== 0;
  const onCreateRace = () => {
    navigate(`/race/${store.id}`);
    if (location.pathname === `/race/${store.id}`) {
      window.location.reload();
    }
  };

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
          <Button onClick={onCreateRace}>Create Race</Button>
        </Box>
        <Box p="2">
          <Link to={isAuthorized ? '/account' : '/account/login'}>
            <Button>{isAuthorized ? <FaUser /> : <FaSignInAlt />}</Button>
          </Link>
        </Box>
      </Flex>
    </Container>
  );
}

export default Header;
