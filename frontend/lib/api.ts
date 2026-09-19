import axios, {AxiosError,InternalAxiosRequestConfig} from "axios";

export const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    withCredentials : true,
    headers:{
        "Content-Type": "application/json",
    },
});

// Variables to handle simultaneous requests during refresh
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: unknown) => void;
  reject: (reason?: any) => void;
}> = [];

const processQueue = (error: AxiosError | null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve();
    }
  });
  failedQueue = [];
};

// Response Interceptor for handling 401s
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Prevent infinite loops: Don't attempt to refresh if the failed call WAS the login or refresh endpoint
    const isAuthRoute =
      originalRequest.url?.includes('/auth/login') ||
      originalRequest.url?.includes('/auth/refresh');

    if (error.response?.status === 401 && !originalRequest._retry && !isAuthRoute) {
      // If a refresh is already in progress, queue this request until the new token arrives
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(() => api(originalRequest))
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Call FastAPI to issue a new access_token cookie
        await api.post('/auth/refresh');

        // Resolve any queued requests that arrived during refresh
        processQueue(null);

        // Retry the original failed request
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh token is expired or invalid -> Clear queue and send to login page
        processQueue(refreshError as AxiosError);

        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }

        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);