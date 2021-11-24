import axios from 'axios';

export const baseApi = import.meta.env.PROD ? '/api' : import.meta.env.VITE_BASE_API_URL;

export const getAuthHeaders = (): Record<string, string> => {
  const accessToken = localStorage.getItem('access_token');
  if (accessToken) {
    return {
      Authorization: `Bearer ${accessToken}`,
    };
  }
  return {};
};

export const refresh = async () => {
  try {
    const response = await api.post<{ access_token: string }>('/auth/refresh');
    localStorage.setItem('access_token', response.data.access_token);
  } catch (e) {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }
};

export const api = axios.create({
  baseURL: baseApi,
  withCredentials: true,
});

api.interceptors.request.use((config) => ({
  ...config,
  headers: {
    ...config.headers,
    ...getAuthHeaders(),
  },
}));

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status !== 401) {
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }
    try {
      await axios.request<{ access_token: string }>({
        method: 'POST',
        url: `${baseApi}/auth/refresh`,
        headers: getAuthHeaders(),
        withCredentials: true,
      });
    } catch (e) {
      return new Promise((resolve, reject) => reject(e));
    }

    const { config } = error;
    config.headers = getAuthHeaders();

    return new Promise((resolve, reject) => axios.request(config).then(resolve).catch(reject)).catch(Promise.reject);
  },
);
