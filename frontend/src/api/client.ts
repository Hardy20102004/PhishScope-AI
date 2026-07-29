import axios from "axios";
import { useAuthStore } from "../stores/authStore";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
  timeout: 10000,
  // withCredentials removed: we use JWT Bearer tokens in memory, not HttpOnly cookies
});

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If the error is 401 Unauthorized, and we haven't already retried this request
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // Attempt to hit the refresh endpoint
        // Because withCredentials=true, the browser automatically sends the HttpOnly refresh_token cookie
        const res = await axios.post(
          `${apiClient.defaults.baseURL}/auth/refresh`,
          {},
          {}
        );
        
        // Ensure we parse our custom APIResponse envelope
        const newAccessToken = res.data.data.access_token;
        
        // Update the global store securely in memory
        useAuthStore.getState().setAccessToken(newAccessToken);
        
        // Update the failed request with the new token and retry
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return apiClient(originalRequest);
        
      } catch (refreshError) {
        // If refresh fails (e.g. refresh token is expired or missing), we log the user out entirely
        useAuthStore.getState().clearAuth();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);
