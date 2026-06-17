import { create } from "zustand";
import { api } from "@/lib/api";

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  role: string;
  is_verified: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: any) => Promise<any>;
  register: (data: any) => Promise<any>;
  logout: () => Promise<void>;
  fetchProfile: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (credentials) => {
    try {
      const response: any = await api.post("/accounts/login/", credentials);
      if (response.success && response.data?.user) {
        set({ user: response.data.user, isAuthenticated: true });
        return response;
      }
      throw new Error(response.message);
    } catch (error: any) {
      throw error;
    }
  },

  register: async (data) => {
    try {
      const response: any = await api.post("/accounts/register/", data);
      return response;
    } catch (error: any) {
      throw error;
    }
  },

  logout: async () => {
    try {
      await api.post("/accounts/logout/");
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      set({ user: null, isAuthenticated: false });
    }
  },

  fetchProfile: async () => {
    set({ isLoading: true });
    try {
      const response: any = await api.get("/accounts/profile/");
      if (response.success && response.data) {
        set({ user: response.data, isAuthenticated: true });
      } else {
        set({ user: null, isAuthenticated: false });
      }
    } catch (error) {
      set({ user: null, isAuthenticated: false });
    } finally {
      set({ isLoading: false });
    }
  },
}));
