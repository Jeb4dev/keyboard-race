import { api } from './index';

export interface UserResponse {
  id: number;
  username: string;
}

export const getUser = async (id: number): Promise<UserResponse | null> => {
  try {
    const { data } = await api.get<UserResponse>(`/user/${id}`);
    return data;
  } catch (e) {
    return null;
  }
};

export const getAccount = async (): Promise<UserResponse | null> => {
  try {
    const { data } = await api.get<UserResponse>('/user/account');
    return data;
  } catch (e) {
    return null;
  }
};
