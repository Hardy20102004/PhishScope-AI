import { useState, useEffect } from 'react'
import { Shield, Settings, CheckCircle2, AlertTriangle, LogOut } from 'lucide-react'

function App() {
  const [token, setToken] = useState<string>('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [activeUrl, setActiveUrl] = useState<string>('')
  const [analyzing, setAnalyzing] = useState(false)

  useEffect(() => {
    // Check if logged in
    chrome.storage.local.get(['phoenix_token'], (result) => {
      if (result.phoenix_token) {
        setIsLoggedIn(true)
        setToken(result.phoenix_token)
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
    // For this architecture phase, we accept an API key or JWT directly.
    // In production, this would open a new tab to authenticate via OAuth.
    await chrome.storage.local.set({ phoenix_token: token })
    
    // Register extension device with backend
    try {
      await fetch('http://localhost:8000/api/v1/extension/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          browser_type: 'Chrome',
          device_fingerprint: 'ext-' + Math.random().toString(36).substring(7),
          settings: {}
        })
      });
    } catch (e) {
      console.error(e)
    }
    
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    chrome.storage.local.remove('phoenix_token')
    setIsLoggedIn(false)
    setToken('')
  }

  const handleQuickScan = async () => {
    setAnalyzing(true)
    try {
      const response = await fetch("http://localhost:8000/api/v1/extension/investigate/quick", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          url: activeUrl,
          context_type: "URL"
        })
      });
      const data = await response.json();
      alert(`Scan Complete. Threat Score: ${data.threat_score}`)
    } catch (e) {
      console.error(e)
      alert("Scan failed")
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
          <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md font-medium text-sm transition-colors">
            Connect
          </button>
        </form>
      </div>
    )
  }

  return (
    <div className="w-[350px] bg-slate-50 text-slate-900 font-sans flex flex-col h-[500px]">
      <header className="bg-slate-900 text-white p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-blue-500" />
          <span className="font-semibold">PHOENIX</span>
        </div>
        <div className="flex gap-2">
          <button className="p-1 hover:bg-slate-800 rounded"><Settings className="w-4 h-4" /></button>
          <button onClick={handleLogout} className="p-1 hover:bg-slate-800 rounded text-red-400"><LogOut className="w-4 h-4" /></button>
        </div>
      </header>

      <main className="flex-1 p-4 overflow-y-auto">
        <div className="bg-white rounded-lg border p-4 shadow-sm mb-4">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Current Page</h2>
          <div className="truncate text-sm font-medium mb-4" title={activeUrl}>
            {activeUrl || 'No active URL'}
          </div>
          
          <button 
            onClick={handleQuickScan}
            disabled={analyzing || !activeUrl}
            className="w-full bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white py-2 rounded-md font-medium text-sm flex items-center justify-center transition-colors"
          >
            {analyzing ? 'Analyzing...' : 'Scan Current Page'}
          </button>
        </div>

        <div className="space-y-3">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Recent Activity</h2>
          
          {/* Mock history item */}
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
