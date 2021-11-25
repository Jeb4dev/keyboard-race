import { api } from './index';

export interface UserResponse {
  id: number;
  username: string;
}

export interface StatisticsResponse {
  statistics: {
    best_wpm: number;
    best_accuracy: number;
    total_races: number;
    average_wpm: number;
    average_accuracy: number;
    average_time: number;
  };
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

export const getStats = async (userId: number): Promise<StatisticsResponse | null> => {
  try {
    const { data } = await api.get<StatisticsResponse>(`/statistics/${userId}`);
    return data;
  } catch (e) {
    return null;
  }
};
