import axios from 'axios';
import {
  getAccessToken,
  getRefreshToken,
  saveTokens,
  clearTokens
} from '@/utils/token';

const api = axios.create({
  baseURL: 'http://localhost:8000/', // ваш базовый URL
});

let isRefreshing = false;
let refreshSubscribers = [];

function onRefreshed(newToken) {
  refreshSubscribers.forEach(cb => cb(newToken));
  refreshSubscribers = [];
}

function addRefreshSubscriber(cb) {
  refreshSubscribers.push(cb);
}

// Добавляем accessToken к каждому запросу
api.interceptors.request.use(config => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Обрабатываем ответы с ошибкой 403
api.interceptors.response.use(
  res => res,
  err => {
    const { config, response } = err;
    if (response && (response.status === 401 || (response.status === 403))) {
      // если уже запущен процесс обновления — ставим в очередь
      if (isRefreshing) {
        return new Promise(resolve => {
          addRefreshSubscriber(token => {
            config.headers.Authorization = `Bearer ${token}`;
            resolve(api(config));
          });
        });
      }

      isRefreshing = true;
      const refreshToken = getRefreshToken();
      if (!refreshToken) {
        clearTokens();
        // перенаправляем на страницу логина
        window.location.href = '/login';
        return Promise.reject(err);
      }

      // отправляем refresh
      return axios
        .post('http://localhost:8000/refresh', { token: refreshToken })
        .then(({ data }) => {
          const { accessToken, refreshToken: newRefresh } = data;
          saveTokens({ accessToken, refreshToken: newRefresh });
          api.defaults.headers.Authorization = `Bearer ${accessToken}`;
          onRefreshed(accessToken);
          // повторяем исходный запрос
          config.headers.Authorization = `Bearer ${accessToken}`;
          return api(config);
        })
        .catch(e => {
          clearTokens();
          window.location.href = '/login';
          return Promise.reject(e);
        })
        .finally(() => {
          isRefreshing = false;
        });
    }

    return Promise.reject(err);
  }
);

export default api;
