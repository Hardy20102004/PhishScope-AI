import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getFeedsStatus } from "@/api/threatIntel";
import { Activity, Search, ShieldAlert, CheckCircle, XCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function ThreatIntelDashboard() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await getFeedsStatus();
        setStatus(data);
      } catch (err) {
        console.error("Failed to fetch feed status", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStatus();
  }, []);

  return (
    <div className="flex h-full flex-col gap-6 p-8 overflow-y-auto bg-background/50">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Threat Intelligence</h1>
          <p className="text-muted-foreground mt-1">
            Centralized intelligence feeds and indicator correlation.
          </p>
        </div>
        <Link to="/threat-intel/search">
          <Button className="gap-2">
            <Search className="h-4 w-4" />
            Search Indicator
          </Button>
        </Link>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-xl border bg-card p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-primary/10 p-3">
              <ShieldAlert className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h3 className="font-medium text-muted-foreground">Global Threat Level</h3>
              <p className="text-2xl font-bold">Elevated</p>
            </div>
          </div>
        </div>
        
        <div className="rounded-xl border bg-card p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-blue-500/10 p-3">
              <Activity className="h-6 w-6 text-blue-500" />
            </div>
            <div>
              <h3 className="font-medium text-muted-foreground">Indicators Cached</h3>
              <p className="text-2xl font-bold">14,231</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 rounded-xl border bg-card shadow-sm">
        <div className="border-b px-6 py-4">
          <h2 className="text-lg font-semibold">Intelligence Feed Status</h2>
        </div>
        <div className="p-6">
          {loading ? (
            <div className="flex justify-center p-4">
              <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {status?.connectors?.map((conn: any) => (
                <div key={conn.name} className="flex items-center justify-between rounded-lg border p-4">
                  <div className="flex items-center gap-3">
                    {conn.status === "healthy" ? (
                      <CheckCircle className="h-5 w-5 text-emerald-500" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-500" />
                    )}
                    <span className="font-medium capitalize">{conn.name.replace(/_/g, ' ')}</span>
                  </div>
                  <span className="text-sm text-muted-foreground capitalize">{conn.status}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
