import { Map } from 'lucide-react';

export function StrategyDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <Map className="mr-2 h-5 w-5 text-primary" />
          Five-Year Strategic Roadmap
        </h2>
        <p className="text-sm text-muted-foreground">Long-term cyber investment and maturity planning.</p>
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Strategic Timeline</h3>
        <div className="space-y-6">
          <div className="relative">
            <div className="flex justify-between text-xs text-muted-foreground mb-2 px-2">
              <span>2026</span>
              <span>2027</span>
              <span>2028</span>
              <span>2029</span>
              <span>2030</span>
            </div>
            <div className="absolute top-6 bottom-0 left-0 right-0 flex justify-between pointer-events-none px-4">
              <div className="border-l border-border/50 h-full"></div>
              <div className="border-l border-border/50 h-full"></div>
              <div className="border-l border-border/50 h-full"></div>
              <div className="border-l border-border/50 h-full"></div>
              <div className="border-l border-border/50 h-full"></div>
            </div>
            
            <div className="space-y-4 relative z-10 mt-6">
              <div className="group">
                <p className="text-xs font-medium mb-1 group-hover:text-primary transition-colors">Zero Trust Architecture Rollout</p>
                <div className="h-8 w-[40%] bg-blue-500/20 border border-blue-500/50 rounded flex items-center px-3 shadow-sm cursor-pointer hover:bg-blue-500/30 transition-colors">
                   <span className="text-[11px] text-blue-400 font-medium truncate">Phase 1: Identity & Device Trust</span>
                </div>
              </div>
              <div className="group">
                <p className="text-xs font-medium mb-1 group-hover:text-primary transition-colors">AI-Native SOC Automation</p>
                <div className="h-8 w-[50%] ml-[20%] bg-purple-500/20 border border-purple-500/50 rounded flex items-center px-3 shadow-sm cursor-pointer hover:bg-purple-500/30 transition-colors">
                   <span className="text-[11px] text-purple-400 font-medium truncate">Full Autonomous Triage</span>
                </div>
              </div>
              <div className="group">
                <p className="text-xs font-medium mb-1 group-hover:text-primary transition-colors">Post-Quantum Cryptography</p>
                <div className="h-8 w-[30%] ml-[70%] bg-amber-500/20 border border-amber-500/50 rounded flex items-center px-3 shadow-sm cursor-pointer hover:bg-amber-500/30 transition-colors">
                   <span className="text-[11px] text-amber-400 font-medium truncate">Core Systems Upgrade</span>
                </div>
              </div>
              <div className="group">
                <p className="text-xs font-medium mb-1 group-hover:text-primary transition-colors">Global Threat Intelligence Mesh</p>
                <div className="h-8 w-[70%] bg-emerald-500/20 border border-emerald-500/50 rounded flex items-center px-3 shadow-sm cursor-pointer hover:bg-emerald-500/30 transition-colors">
                   <span className="text-[11px] text-emerald-400 font-medium truncate">Continuous Integration & Sharing</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
