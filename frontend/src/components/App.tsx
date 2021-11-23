import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Layout from './Layout';
import HomePage from '../pages/home';
import AccountPage from '../pages/account';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/">
            <Route index element={<HomePage />} />
            <Route path="/account" element={<AccountPage />} />
          </Route>
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
