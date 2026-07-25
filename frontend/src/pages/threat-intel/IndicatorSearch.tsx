import { useState } from "react";
import { searchIndicator, type Indicator } from "@/api/threatIntel";
import { Search, ShieldAlert, ShieldCheck, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function IndicatorSearch() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Indicator | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const data = await searchIndicator(query.trim());
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to search indicator");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const getReputationColor = (score: number) => {
    if (score > 75) return "text-red-500";
    if (score > 50) return "text-orange-500";
    if (score > 0) return "text-yellow-500";
    return "text-emerald-500";
  };

  const getReputationIcon = (score: number) => {
    if (score > 75) return <ShieldAlert className="h-8 w-8 text-red-500" />;
    if (score > 50) return <AlertTriangle className="h-8 w-8 text-orange-500" />;
    return <ShieldCheck className="h-8 w-8 text-emerald-500" />;
  };

  return (
    <div className="flex h-full flex-col gap-6 p-8 overflow-y-auto bg-background/50">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Indicator Search</h1>
        <p className="text-muted-foreground mt-1">
          Search for URLs, Domains, IPs, Hashes, or Emails to retrieve threat intelligence.
        </p>
      </div>

      <div className="rounded-xl border bg-card p-6 shadow-sm">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter an indicator (e.g., 8.8.8.8, example.com)"
              className="h-12 w-full rounded-md border border-input bg-transparent pl-10 pr-4 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            />
          </div>
          <Button type="submit" disabled={loading} className="h-12 px-8">
            {loading ? "Searching..." : "Search"}
          </Button>
        </form>
        {error && <p className="mt-4 text-sm text-red-500">{error}</p>}
      </div>

      {result && (
        <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4">
          <div className="grid gap-6 md:grid-cols-3">
            <div className="col-span-1 rounded-xl border bg-card p-6 shadow-sm flex flex-col items-center justify-center text-center gap-4">
              {getReputationIcon(result.reputation_score)}
              <div>
                <h2 className="text-xl font-bold">{result.threat_classification || "Safe"}</h2>
                <p className="text-sm text-muted-foreground capitalize">{result.type}</p>
              </div>
              <div className="w-full rounded-lg bg-muted/50 p-4">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-muted-foreground">Reputation Score</span>
                  <span className={`font-bold ${getReputationColor(result.reputation_score)}`}>
                    {result.reputation_score}/100
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
                  <div
                    className="h-full bg-primary transition-all"
                    style={{ width: `${result.reputation_score}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="col-span-2 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="text-lg font-semibold mb-4">Indicator Details</h3>
              <div className="grid grid-cols-2 gap-y-4 gap-x-8">
                <div>
                  <p className="text-sm text-muted-foreground">Value</p>
                  <p className="font-mono text-sm mt-1 break-all">{result.value}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Confidence Score</p>
                  <p className="font-medium mt-1">{result.confidence_score}%</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">First Seen</p>
                  <p className="font-medium mt-1">{new Date(result.first_seen).toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Last Seen</p>
                  <p className="font-medium mt-1">{new Date(result.last_seen).toLocaleString()}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-xl border bg-card shadow-sm">
            <div className="border-b px-6 py-4">
              <h3 className="text-lg font-semibold">Feed Results</h3>
            </div>
            <div className="divide-y">
              {result.feed_results.map((feed) => (
                <div key={feed.id} className="flex items-center justify-between p-6">
                  <div className="flex items-center gap-4">
                    <div className="rounded-full bg-primary/10 p-2">
                      <ShieldAlert className="h-4 w-4 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-medium capitalize">{feed.source.replace(/_/g, ' ')}</h4>
                      <p className="text-sm text-muted-foreground">
                        {new Date(feed.created_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`font-bold ${getReputationColor(feed.reputation_score)}`}>
                      {feed.reputation_score}/100
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {feed.threat_classification || "Clean"}
                    </p>
                  </div>
                </div>
              ))}
              {result.feed_results.length === 0 && (
                <div className="p-8 text-center text-muted-foreground">
                  No feed results available.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
