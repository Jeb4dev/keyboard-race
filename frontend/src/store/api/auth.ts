import { api } from './index';

export interface AuthResponse {
  access_token: string;
  user_id: number;
}

export const login = async (username: string, password: string): Promise<number> => {
  try {
    const response = await api.post<AuthResponse>('/auth/login', {
      username,
      password,
    });

    localStorage.setItem('access_token', response.data.access_token);

    return response.data.user_id;
  } catch (e) {
    return 0;
  }
};

export const register = async (username: string, password: string): Promise<number> => {
  try {
    const response = await api.post<AuthResponse>('/auth/register', {
      username,
      password,
    });

    localStorage.setItem('access_token', response.data.access_token);

    return response.data.user_id;
  } catch (e) {
    return 0;
  }
};

export const logout = async () => api.post('/auth/logout');
