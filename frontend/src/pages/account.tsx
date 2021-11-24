import React, { useEffect } from 'react';
import { useStore } from 'effector-react';
import { useNavigate } from 'react-router';

import { $account } from '../store/account';

import Profile from '../components/Profile';

function AccountPage() {
  const store = useStore($account);
  const navigate = useNavigate();

  useEffect(() => {
    if (store.id === 0) navigate('/account/login');
  }, []);

  if (store.id !== 0) {
    return <Profile />;
  }

  return <></>;
}

export default AccountPage;
