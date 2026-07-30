import { Search, X, Database, Shield, FileText } from 'lucide-react';

interface Props {
  onClose: () => void;
}

export function GlobalSearchInterface({ onClose }: Props) {
  return (
    <div className="absolute inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-start justify-center pt-20">
      <div className="w-full max-w-3xl bg-card border rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh] animate-in slide-in-from-top-10 duration-200">
        <div className="flex items-center border-b p-4">
          <Search className="h-5 w-5 text-muted-foreground mr-3" />
          <input 
            type="text" 
            autoFocus
            placeholder="Search across SOC, Threat Intel, Governance, Assets..." 
            className="flex-1 bg-transparent border-none outline-none text-lg placeholder:text-muted-foreground"
          />
          <button onClick={onClose} className="p-1 hover:bg-secondary rounded-md text-muted-foreground">
            <X className="h-5 w-5" />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 bg-secondary/20">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-2">Suggestions</div>
          <div className="space-y-1">
            <button className="w-full flex items-center px-4 py-3 rounded-lg hover:bg-secondary transition-colors text-left group">
              <Shield className="h-4 w-4 mr-3 text-red-500" />
              <div className="flex-1">
                <div className="text-sm font-medium group-hover:text-primary transition-colors">Active High-Criticality Incidents</div>
                <div className="text-xs text-muted-foreground">Search SOC module</div>
              </div>
            </button>
            <button className="w-full flex items-center px-4 py-3 rounded-lg hover:bg-secondary transition-colors text-left group">
              <FileText className="h-4 w-4 mr-3 text-blue-500" />
              <div className="flex-1">
                <div className="text-sm font-medium group-hover:text-primary transition-colors">ISO 27001 Readiness Status</div>
                <div className="text-xs text-muted-foreground">Search Governance module</div>
              </div>
            </button>
            <button className="w-full flex items-center px-4 py-3 rounded-lg hover:bg-secondary transition-colors text-left group">
              <Database className="h-4 w-4 mr-3 text-emerald-500" />
              <div className="flex-1">
                <div className="text-sm font-medium group-hover:text-primary transition-colors">Query Enterprise Knowledge Graph</div>
                <div className="text-xs text-muted-foreground">Graph Explorer</div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
