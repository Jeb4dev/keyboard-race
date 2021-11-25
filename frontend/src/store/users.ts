import { createEffect, createEvent, createStore, forward } from 'effector';
import { getUser, UserResponse } from './api/user';

type UsersStore = Record<number, string>;

export const fetchUser = createEvent<number>();

const fetchUserFx = createEffect<number, UserResponse | null>().use(getUser);

forward({
  from: fetchUser,
  to: fetchUserFx,
});

export const $users = createStore<UsersStore>({}).on(fetchUserFx.doneData, (state, result) => {
  if (result !== null) {
    return {
      ...state,
      [result.id]: result.username,
    };
  }
});
