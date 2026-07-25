import { useState, useEffect } from "react";
import { createReport, listReports, type Report } from "@/api/reports";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { FileText, Loader2, Plus } from "lucide-react";

export function ReportBuilder({ caseId }: { caseId: string }) {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, [caseId]);

  const loadReports = async () => {
    try {
      const data = await listReports(caseId);
      setReports(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      await createReport({
        case_id: caseId,
        title: "Technical Investigation Report",
        content_data: {
          summary: "This report outlines the findings of the investigation.",
          findings: ["Evidence collected", "Timeline compiled", "AI summary attached"]
        }
      });
      await loadReports();
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium">Case Reports</h3>
          <p className="text-sm text-muted-foreground">Generate and manage professional reports for this case.</p>
        </div>
        <Button onClick={handleGenerate} disabled={loading}>
          {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
          Generate Report
        </Button>
      </div>

      {reports.length === 0 ? (
        <div className="text-center py-12 border rounded-xl bg-card border-dashed">
          <FileText className="mx-auto h-12 w-12 text-muted-foreground opacity-20 mb-4" />
          <h3 className="text-lg font-medium">No Reports Generated</h3>
          <p className="text-sm text-muted-foreground max-w-sm mx-auto mt-2">
            Click the button above to compile the investigation evidence into a structured report.
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {reports.map((report) => (
            <div key={report.id} className="p-4 border rounded-xl bg-card shadow-sm space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-medium">{report.title}</h4>
                  <p className="text-xs text-muted-foreground mt-1">ID: {report.id.substring(0,8)}</p>
                </div>
                <Badge variant={report.status === 'APPROVED' ? 'default' : 'secondary'}>{report.status}</Badge>
              </div>
              <div className="pt-4 border-t flex justify-end gap-2">
                <Button variant="outline" size="sm">View</Button>
                <Button size="sm">Export PDF</Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
