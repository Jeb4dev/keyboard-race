import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import SocketProvider from '../sockets/context';
import Layout from './Layout';
import HomePage from '../pages/home';
import AccountPage from '../pages/account';
import AccountFormPage from '../pages/account-form';
import RacePage from '../pages/race';

function App() {
  return (
    <SocketProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/">
              <Route index element={<HomePage />} />
              <Route path="account">
                <Route index element={<AccountPage />} />
                <Route path=":form" element={<AccountFormPage />} />
              </Route>
              <Route path="race">
                <Route path=":userId" element={<RacePage />} />
              </Route>
            </Route>
          </Routes>
        </Layout>
      </BrowserRouter>
    </SocketProvider>
  );
}

export default App;
