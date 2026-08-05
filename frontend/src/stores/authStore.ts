import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

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

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initialize to false. The app will try to hydrate from sessionStorage on load.
      // On page refresh within the same tab, the token is restored automatically.
      // On browser/tab close, sessionStorage is cleared — forcing a fresh login.
      isAuthenticated: false,
      accessToken: null,
      user: null,
      setAuth: (accessToken, user) => set({ isAuthenticated: true, accessToken, user }),
      setAccessToken: (accessToken) => set({ isAuthenticated: true, accessToken }),
      clearAuth: () => set({ isAuthenticated: false, accessToken: null, user: null }),
    }),
    {
      name: "phoenix-auth",
      storage: createJSONStorage(() => sessionStorage),
      // Only persist the token and user — not transient UI state
      partialize: (state) => ({
        isAuthenticated: state.isAuthenticated,
        accessToken: state.accessToken,
        user: state.user,
      }),
    }
  )
);

