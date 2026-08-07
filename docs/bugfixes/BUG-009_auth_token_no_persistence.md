# BUG-009: Auth Token Lost on Page Refresh

**Severity**: MEDIUM (UX)
**File**: `frontend/src/stores/authStore.ts`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

The frontend React application used Zustand to manage global authentication state (`useAuthStore`).
However, the state was entirely stored in memory.

Whenever the user refreshed the browser tab (F5) or manually navigated to a URL, the React
application would re-mount, the Zustand store would initialize to its default state
(`isAuthenticated: false`), and the user would be immediately kicked out to the login screen,
even if their HttpOnly refresh token cookie was still valid.

## Impact

Extremely poor user experience. Security analysts using the dashboard would lose their session context anytime they refreshed the page to get the latest data.

## Fix Applied

Wrapped the Zustand store definition in the `persist` middleware, configuring it to use
the browser's `sessionStorage`.

```typescript
import { persist, createJSONStorage } from "zustand/middleware";

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      accessToken: null,
      user: null,
      // ... actions ...
    }),
    {
      name: "phoenix-auth",
      storage: createJSONStorage(() => sessionStorage),
      partialize: (state) => ({
        isAuthenticated: state.isAuthenticated,
        accessToken: state.accessToken,
        user: state.user,
      }),
    }
  )
);
```

### Why sessionStorage?

Unlike `localStorage` (which persists indefinitely until manually cleared), `sessionStorage`
is scoped to the specific browser tab and is cleared when the tab is closed.

For a high-security SOC platform like PHOENIX, this provides the perfect balance:
- Protects against UX frustration (survives page refreshes).
- Maintains strict security (access tokens don't linger on disk after the tab is closed).
