import { useState, useEffect } from 'react'
import { Shield, Settings, CheckCircle2, AlertTriangle, XCircle, LogOut, Scan } from 'lucide-react'

// Configurable API base — set VITE_API_URL in .env.local (extension build)
const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

/** Generate a stable fingerprint stored in chrome.storage.local */
async function getOrCreateFingerprint(): Promise<string> {
  return new Promise((resolve) => {
    chrome.storage.local.get(['phoenix_device_fingerprint'], (result) => {
      const existing = result.phoenix_device_fingerprint as string | undefined;
      if (existing) {
        resolve(existing)
      } else {
        const fp = 'ext-' + crypto.randomUUID()
        chrome.storage.local.set({ phoenix_device_fingerprint: fp })
        resolve(fp)
      }
    })
  })
}

interface ScanResult {
  investigation_id: string
  threat_score: number
}

function ThreatBadge({ score }: { score: number }) {
  if (score >= 75) {
    return (
      <div className="flex items-center gap-2 mt-3 bg-red-50 border border-red-200 rounded-lg p-3">
        <XCircle className="w-5 h-5 text-red-600 shrink-0" />
        <div>
          <p className="text-sm font-semibold text-red-700">High Risk — Score: {score}/100</p>
          <p className="text-xs text-red-500">This page shows strong phishing indicators.</p>
        </div>
      </div>
    )
  }
  if (score >= 40) {
    return (
      <div className="flex items-center gap-2 mt-3 bg-amber-50 border border-amber-200 rounded-lg p-3">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
        <div>
          <p className="text-sm font-semibold text-amber-700">Suspicious — Score: {score}/100</p>
          <p className="text-xs text-amber-500">Proceed with caution.</p>
        </div>
      </div>
    )
  }
  return (
    <div className="flex items-center gap-2 mt-3 bg-green-50 border border-green-200 rounded-lg p-3">
      <CheckCircle2 className="w-5 h-5 text-green-600 shrink-0" />
      <div>
        <p className="text-sm font-semibold text-green-700">Safe — Score: {score}/100</p>
        <p className="text-xs text-green-500">No threats detected.</p>
      </div>
    </div>
  )
}

function App() {
  const [token, setToken] = useState<string>('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [activeUrl, setActiveUrl] = useState<string>('')
  const [analyzing, setAnalyzing] = useState(false)
  const [scanResult, setScanResult] = useState<ScanResult | null>(null)
  const [scanError, setScanError] = useState<string | null>(null)

  useEffect(() => {
    // Restore session if token exists
    chrome.storage.local.get(['phoenix_token'], (result) => {
      const storedToken = result.phoenix_token as string | undefined;
      if (storedToken) {
        setIsLoggedIn(true)
        setToken(storedToken)
      }
    })

    // Get current tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.url) {
        setActiveUrl(tabs[0].url)
      }
    })
  }, [])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    await chrome.storage.local.set({ phoenix_token: token })

    // Register extension device with a stable fingerprint
    try {
      const fingerprint = await getOrCreateFingerprint()
      await fetch(`${API_BASE}/api/v1/extension/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          browser_type: 'Chrome',
          device_fingerprint: fingerprint,
          settings: {}
        })
      })
    } catch (err) {
      console.error('Device registration failed:', err)
    }

    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    chrome.storage.local.remove('phoenix_token')
    setIsLoggedIn(false)
    setToken('')
    setScanResult(null)
    setScanError(null)
  }

  const handleQuickScan = async () => {
    setAnalyzing(true)
    setScanResult(null)
    setScanError(null)
    try {
      const response = await fetch(`${API_BASE}/api/v1/extension/investigate/quick`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          url: activeUrl,
          context_type: 'URL'
        })
      })

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}))
        throw new Error(errData?.detail ?? `Server error: ${response.status}`)
      }

      const data = await response.json()
      setScanResult({
        investigation_id: data.investigation_id ?? 'N/A',
        threat_score: typeof data.threat_score === 'number' ? data.threat_score : 0,
      })
    } catch (err: unknown) {
      setScanError(err instanceof Error ? err.message : 'Scan failed. Check your connection.')
    } finally {
      setAnalyzing(false)
    }
  }

  if (!isLoggedIn) {
    return (
      <div className="w-[350px] p-6 bg-slate-900 text-white font-sans flex flex-col items-center">
        <Shield className="w-12 h-12 text-blue-500 mb-4" />
        <h1 className="text-xl font-bold mb-2">PHOENIX Assistant</h1>
        <p className="text-sm text-slate-400 text-center mb-6">Enter your API token to connect your extension.</p>

        <form onSubmit={handleLogin} className="w-full">
          <input
            type="password"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            placeholder="eyJh..."
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-md text-sm mb-4 focus:outline-none focus:border-blue-500"
          />
          <button type="submit" disabled={!token.trim()} className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white py-2 rounded-md font-medium text-sm transition-colors">
            Connect
          </button>
        </form>
      </div>
    )
  }

  return (
    <div className="w-[350px] bg-slate-50 text-slate-900 font-sans flex flex-col h-[520px]">
      <header className="bg-slate-900 text-white p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-blue-500" />
          <span className="font-semibold">PHOENIX</span>
        </div>
        <div className="flex gap-2">
          <button className="p-1 hover:bg-slate-800 rounded" aria-label="Settings">
            <Settings className="w-4 h-4" />
          </button>
          <button onClick={handleLogout} className="p-1 hover:bg-slate-800 rounded text-red-400" aria-label="Logout">
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </header>

      <main className="flex-1 p-4 overflow-y-auto space-y-4">
        {/* Current Page + Scan */}
        <div className="bg-white rounded-lg border p-4 shadow-sm">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Current Page</h2>
          <div className="truncate text-sm font-medium mb-4 text-slate-700" title={activeUrl}>
            {activeUrl || 'No active URL'}
          </div>

          <button
            onClick={handleQuickScan}
            disabled={analyzing || !activeUrl}
            className="w-full bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white py-2 rounded-md font-medium text-sm flex items-center justify-center gap-2 transition-colors"
          >
            <Scan className="w-4 h-4" />
            {analyzing ? 'Analyzing...' : 'Scan Current Page'}
          </button>

          {/* Real scan result with threat score */}
          {scanResult && <ThreatBadge score={scanResult.threat_score} />}

          {/* Error display */}
          {scanError && (
            <div className="flex items-start gap-2 mt-3 bg-red-50 border border-red-200 rounded-lg p-3">
              <XCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
              <p className="text-xs text-red-600">{scanError}</p>
            </div>
          )}
        </div>

        {/* Recent Activity */}
        <div className="space-y-2">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Recent Activity</h2>

          <div className="bg-white p-3 rounded-lg border shadow-sm flex items-start gap-3">
            <div className="bg-green-100 p-1.5 rounded-md mt-0.5">
              <CheckCircle2 className="w-4 h-4 text-green-600" />
            </div>
            <div>
              <p className="text-sm font-medium">Safe Domain Detected</p>
              <p className="text-xs text-slate-500 truncate w-[220px]">github.com</p>
            </div>
          </div>

          <div className="bg-white p-3 rounded-lg border shadow-sm flex items-start gap-3">
            <div className="bg-amber-100 p-1.5 rounded-md mt-0.5">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
            </div>
            <div>
              <p className="text-sm font-medium">Suspicious Pattern</p>
              <p className="text-xs text-slate-500 truncate w-[220px]">login-update-account.secure-verify.com</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
