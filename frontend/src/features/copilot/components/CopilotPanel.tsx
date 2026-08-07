import { useState, useEffect } from "react";
import { getCopilotHistory, type CopilotMessage } from "@/api/copilot";
import { ChatInterface } from "./ChatInterface";
import { Recommendations } from "./Recommendations";
import { ReportModal } from "./ReportModal";
import { Button } from "@/components/ui/Button";
import { FileText, Bot, Loader2 } from "lucide-react";

interface CopilotPanelProps {
  investigationId: string;
}

export function CopilotPanel({ investigationId }: CopilotPanelProps) {
  const [history, setHistory] = useState<CopilotMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [showReportModal, setShowReportModal] = useState(false);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getCopilotHistory(investigationId);
        setHistory(data);
      } catch (err) {
        console.error("Failed to fetch copilot history", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [investigationId]);

  if (loading) {
    return (
      <div className="flex h-full w-full flex-col items-center justify-center border-l bg-card text-muted-foreground">
        <Loader2 className="h-6 w-6 animate-spin mb-2" />
        <p className="text-sm">Loading Copilot...</p>
      </div>
    );
  }

  return (
    <div className="flex h-full w-full flex-col border-l bg-card">
      <div className="flex items-center justify-between border-b p-4">
        <div className="flex items-center gap-2 font-semibold">
          <Bot className="h-5 w-5 text-primary" />
          AI Copilot
        </div>
        <Button variant="outline" size="sm" onClick={() => setShowReportModal(true)} className="h-8 gap-2">
          <FileText className="h-4 w-4" />
          Report
        </Button>
      </div>
      
      <Recommendations investigationId={investigationId} />
      
      <div className="flex-1 overflow-hidden">
        <ChatInterface investigationId={investigationId} initialHistory={history} />
      </div>

      {showReportModal && (
        <ReportModal 
          investigationId={investigationId} 
          onClose={() => setShowReportModal(false)} 
        />
      )}
    </div>
  );
}
