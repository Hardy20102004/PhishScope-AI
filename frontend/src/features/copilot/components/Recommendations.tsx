import { useState, useEffect } from "react";
import { getRecommendations } from "@/api/copilot";
import { Lightbulb, Loader2 } from "lucide-react";

interface RecommendationsProps {
  investigationId: string;
}

export function Recommendations({ investigationId }: RecommendationsProps) {
  const [recs, setRecs] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecs = async () => {
      try {
        const data = await getRecommendations(investigationId);
        setRecs(data);
      } catch (err) {
        console.error("Failed to load recommendations", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecs();
  }, [investigationId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-6 text-muted-foreground">
        <Loader2 className="h-5 w-5 animate-spin mr-2" />
        <span className="text-sm">Analyzing context...</span>
      </div>
    );
  }

  if (recs.length === 0) {
    return null;
  }

  return (
    <div className="p-4 bg-muted/30 border-b">
      <div className="flex items-center gap-2 mb-3 text-sm font-semibold text-primary">
        <Lightbulb size={16} />
        Suggested Next Steps
      </div>
      <div className="flex flex-col gap-2">
        {recs.map((rec, idx) => (
          <div key={idx} className="text-xs bg-background border p-2 rounded shadow-sm hover:border-primary cursor-pointer transition-colors">
            {rec}
          </div>
        ))}
      </div>
    </div>
  );
}
