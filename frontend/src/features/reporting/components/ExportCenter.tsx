import { useState } from "react";
import { exportCase, generateManifest, type EvidenceManifest } from "@/api/reports";
import { Button } from "@/components/ui/Button";
import { Download, ShieldCheck, FileArchive, Loader2 } from "lucide-react";

export function ExportCenter({ caseId }: { caseId: string }) {
  const [loading, setLoading] = useState(false);
  const [manifest, setManifest] = useState<EvidenceManifest | null>(null);

  const handleExportPackage = async () => {
    setLoading(true);
    try {
      await exportCase(caseId, "ZIP");
      alert("Export request submitted. Packaging will begin shortly.");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateManifest = async () => {
    setLoading(true);
    try {
      const data = await generateManifest(caseId);
      setManifest(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <div className="border rounded-xl bg-card p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-3 text-primary">
            <FileArchive className="h-6 w-6" />
            <h3 className="text-lg font-medium">Investigation Package</h3>
          </div>
          <p className="text-sm text-muted-foreground">
            Export the complete case, including all timeline events, decisions, associated investigations, and generated reports into a compressed machine-readable ZIP package.
          </p>
          <Button onClick={handleExportPackage} disabled={loading} className="w-full">
            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Download className="mr-2 h-4 w-4" />}
            Generate ZIP Export
          </Button>
        </div>

        <div className="border rounded-xl bg-card p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-3 text-green-600">
            <ShieldCheck className="h-6 w-6" />
            <h3 className="text-lg font-medium text-foreground">Chain of Custody Manifest</h3>
          </div>
          <p className="text-sm text-muted-foreground">
            Generate a cryptographically secure SHA-256 hash representing the exact state of this case and all associated evidence at this moment in time.
          </p>
          
          {manifest ? (
            <div className="p-4 bg-muted/50 rounded-lg border space-y-2">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">SHA-256 Integrity Hash</p>
              <p className="text-sm font-mono break-all">{manifest.hash_value}</p>
            </div>
          ) : (
            <Button onClick={handleGenerateManifest} variant="secondary" disabled={loading} className="w-full">
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <ShieldCheck className="mr-2 h-4 w-4" />}
              Generate Manifest Hash
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
