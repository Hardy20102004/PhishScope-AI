import { useState } from "react";
import { generateReport } from "@/api/copilot";
import { Button } from "@/components/ui/Button";
import { Loader2, FileText, Download, X } from "lucide-react";

interface ReportModalProps {
  investigationId: string;
  onClose: () => void;
}

export function ReportModal({ investigationId, onClose }: ReportModalProps) {
  const [reportType, setReportType] = useState("Executive");
  const [loading, setLoading] = useState(false);
  const [reportContent, setReportContent] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const data = await generateReport(investigationId, reportType);
      setReportContent(data.content);
    } catch (err) {
      console.error("Failed to generate report", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
      <div className="w-full max-w-2xl bg-card border rounded-xl shadow-lg flex flex-col max-h-[85vh]">
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-2 font-semibold">
            <FileText className="h-5 w-5 text-primary" />
            Generate Investigation Report
          </div>
          <button onClick={onClose} className="p-1 hover:bg-muted rounded-full">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-6 flex-1 overflow-auto">
          {!reportContent ? (
            <div className="space-y-6">
              <div>
                <label className="text-sm font-medium">Select Report Type</label>
                <select
                  value={reportType}
                  onChange={e => setReportType(e.target.value)}
                  className="mt-2 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                >
                  <option value="Executive">Executive Summary</option>
                  <option value="Technical">Technical Report</option>
                  <option value="SOC">SOC Analyst Report</option>
                </select>
              </div>

              <div className="bg-muted p-4 rounded-md text-sm text-muted-foreground">
                The AI Copilot will compile all evidence, context, and threat intelligence into a structured professional report.
              </div>

              <Button onClick={handleGenerate} disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Drafting Report...
                  </>
                ) : (
                  "Generate Report"
                )}
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="bg-background border rounded-md p-6 prose prose-sm max-w-none dark:prose-invert">
                <pre className="whitespace-pre-wrap font-sans text-sm">{reportContent}</pre>
              </div>
            </div>
          )}
        </div>

        {reportContent && (
          <div className="p-4 border-t bg-muted/30 flex justify-end gap-2">
            <Button variant="outline" onClick={onClose}>Close</Button>
            <Button className="gap-2">
              <Download className="h-4 w-4" />
              Download Markdown
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
