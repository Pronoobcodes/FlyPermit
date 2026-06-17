import axios from "axios";

export const api = axios.create({
  baseURL: "/api",
  withCredentials: true, // Important for cookies (if cross-origin, though it's same-origin here)
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor to uniformly handle response formats
api.interceptors.response.use(
  (response) => {
    return response.data; // Since our standard format is { success, message, data }
  },
  (error) => {
    // If the error response exists, return it formatted, otherwise a generic error
    if (error.response) {
      if (error.response.status === 401) {
        if (typeof window !== "undefined" && window.location.pathname !== "/login" && window.location.pathname !== "/register") {
          window.location.href = "/login";
        }
      }
      return Promise.reject(error.response.data);
    }
    return Promise.reject({
      success: false,
      message: "An unexpected error occurred.",
      errors: error.message,
    });
  }
);
