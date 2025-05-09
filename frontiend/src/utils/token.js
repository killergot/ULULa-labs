export function getAccessToken() {
    return localStorage.getItem('accessToken');
  }
  export function getRefreshToken() {
    return localStorage.getItem('refreshToken');
  }
  export function saveTokens({ accessToken, refreshToken }) {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
  }
  export function clearTokens() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
  