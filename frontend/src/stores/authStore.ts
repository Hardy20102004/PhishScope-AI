import { create } from "zustand";

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  is_superuser: boolean;
}

interface AuthState {
  isAuthenticated: boolean;
  accessToken: string | null;
  user: User | null;
  setAuth: (accessToken: string, user: User) => void;
  setAccessToken: (accessToken: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  // Initialize to false. The app should try to fetch /users/me on boot
  // using the HttpOnly refresh token to restore session if no access token exists.
  isAuthenticated: false,
  accessToken: null,
  user: null,
  setAuth: (accessToken, user) => set({ isAuthenticated: true, accessToken, user }),
  setAccessToken: (accessToken) => set({ isAuthenticated: true, accessToken }),
  clearAuth: () => set({ isAuthenticated: false, accessToken: null, user: null }),
}));
