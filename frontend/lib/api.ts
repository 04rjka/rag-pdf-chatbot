import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

export const api = axios.create({
  // Forward through Next.js rewrites to attach HttpOnly cookies
  baseURL: "/api/v1",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

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

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    if (!originalRequest) {
      return Promise.reject(error);
    }

    const requestUrl = originalRequest.url || "";

    // 1. Check if the failed endpoint is an authentication route
    const isAuthEndpoint =
      requestUrl.includes("/auth/login") ||
      requestUrl.includes("/auth/refresh") ||
      requestUrl.includes("/auth/register") ||
      requestUrl.includes("/auth/logout");

    // 2. Flexible path check for auth pages with query parameters
    const isAuthPage =
      typeof window !== "undefined" &&
      (window.location.pathname.startsWith("/login") ||
        window.location.pathname.startsWith("/signup") ||
        window.location.pathname.startsWith("/register"));

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !isAuthEndpoint
    ) {
      // If the user is on an auth page, skip refreshing
      if (isAuthPage) {
        return Promise.reject(error);
      }

      // Queue concurrent requests while a refresh is in progress
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
        // Send POST to FastAPI /auth/refresh proxied via Next.js
        await api.post("/auth/refresh");

        processQueue(null);
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError as AxiosError);

        // Redirect to login if session refresh fails completely
        if (
          typeof window !== "undefined" &&
          !window.location.pathname.startsWith("/login")
        ) {
          const currentPath = encodeURIComponent(window.location.pathname);
          window.location.href = `/login?from=${currentPath}`;
        }

        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);