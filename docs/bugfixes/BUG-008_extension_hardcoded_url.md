# BUG-008: Chrome Extension - Hardcoded API URL, Ephemeral Fingerprint, and UI Placeholders

**Severity**: HIGH
**File**: `extension/src/App.tsx`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

The browser extension contained three critical usability and integration bugs:

1. **Hardcoded API URL**: The extension strictly communicated with `http://localhost:8000`. It was impossible to use the extension against a production or staging deployment.
2. **Ephemeral Device Fingerprint**: During the `/register` flow, the extension generated a new random fingerprint (`'ext-' + Math.random()...`) on every login. This polluted the backend database with orphan device records and broke device-tracking logic.
3. **Hardcoded Threat Score Display**: After a successful URL scan, the extension used a primitive browser `alert()` that always reported `Threat Score: 75`, regardless of the actual response from the backend.

## Impact

- The extension was unusable outside of local development.
- The backend device registry became bloated with duplicate records for the same user.
- The core value proposition of the extension (showing URL threat scores) was broken because it always showed fake placeholder data in a jarring `alert()` popup.

## Fix Applied

### 1. Configurable API URL

Introduced a `VITE_API_URL` environment variable check, defaulting to localhost if not set during the build process:

```typescript
const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
```

### 2. Stable Device Fingerprint

Created an async helper to read the fingerprint from `chrome.storage.local`, or generate a stable UUID once and persist it:

```typescript
async function getOrCreateFingerprint(): Promise<string> {
  return new Promise((resolve) => {
    chrome.storage.local.get(['phoenix_device_fingerprint'], (result) => {
      if (result.phoenix_device_fingerprint) {
        resolve(result.phoenix_device_fingerprint)
      } else {
        const fp = 'ext-' + crypto.randomUUID()
        chrome.storage.local.set({ phoenix_device_fingerprint: fp })
        resolve(fp)
      }
    })
  })
}
```

### 3. Real Threat Score & UI Update

- Replaced the `alert()` call with React state (`scanResult` and `scanError`).
- Implemented a `ThreatBadge` component that displays the actual score returned by the backend API.
- Implemented color coding (Red >= 75, Yellow >= 40, Green < 40) based on the score.

```tsx
setScanResult({
  investigation_id: data.investigation_id ?? 'N/A',
  threat_score: typeof data.threat_score === 'number' ? data.threat_score : 0,
})
```
