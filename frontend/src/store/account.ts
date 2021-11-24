import { createEffect, createEvent, createStore, forward } from 'effector';
import { login as apiLogin, register as apiRegister, logout as apiLogout } from './api/auth';
import { getAccount, UserResponse } from './api/user';

interface AccountStore {
  id: number;
  username: string;
  error: string;
}

type AuthData = { username: string; password: string };

export const login = createEvent<AuthData>();
export const register = createEvent<AuthData>();
export const logout = createEvent();

export const fetchAccount = createEvent();

const loginFx = createEffect<AuthData, number>().use(({ username, password }) => apiLogin(username, password));
const registerFx = createEffect<AuthData, number>().use(({ username, password }) => apiRegister(username, password));
const logoutFx = createEffect<void, void>().use(() => void apiLogout());

const fetchAccountFx = createEffect<void, UserResponse | null>(getAccount);

forward({
  from: login,
  to: loginFx,
});

forward({
  from: register,
  to: registerFx,
});

forward({
  from: fetchAccount,
  to: fetchAccountFx,
});

forward({
  from: logout,
  to: logoutFx,
});

forward({
  from: [loginFx.doneData, registerFx.doneData],
  to: fetchAccount,
});

const onErrorAuth = (error: string) => {
  return (state: AccountStore, result: number): AccountStore => {
    if (result !== 0) {
      return {
        ...state,
        id: result,
      };
    }
    return {
      ...state,
      error,
    };
  };
};

const onFailAuth =
  (error: string) =>
  (state: AccountStore): AccountStore => ({
    ...state,
    error,
  });

export const $account = createStore<AccountStore>({
  id: 0,
  username: '',
  error: '',
})
  .on(fetchAccountFx.doneData, (state, result) => {
    if (result !== null) {
      return {
        ...state,
        ...result,
      };
    }
  })
  .on(loginFx.doneData, onErrorAuth('Invalid username or password'))
  .on(registerFx.doneData, onErrorAuth('Username is taken'))
  .on(loginFx.fail, onFailAuth('Invalid login data'))
  .on(registerFx.fail, onFailAuth('Invalid register data'))
  .on(logoutFx.done, (state) => {
    localStorage.removeItem('access_token');
    window.location.href = '/';
    return state;
  });

fetchAccount();
