import { Cpu, Search, Layers, Hexagon, Fingerprint, Shield, Command, BrainCircuit } from 'lucide-react';

interface Props {
  onOpenSearch: () => void;
  activeWorkspace: string;
  setActiveWorkspace: (w: string) => void;
}

export function UnifiedNavigation({ onOpenSearch, activeWorkspace, setActiveWorkspace }: Props) {
  const workspaces = [
    { id: 'os-kernel', name: 'CyberOS Kernel', icon: Hexagon },
    { id: 'command', name: 'Cyber Command', icon: Command },
    { id: 'soc', name: 'SOC Fusion', icon: Shield },
    { id: 'governance', name: 'Governance', icon: Layers },
  ];

  return (
    <header className="border-b bg-card px-4 py-3 flex items-center justify-between z-20 shadow-sm">
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2 mr-4">
          <BrainCircuit className="h-6 w-6 text-primary" />
          <span className="font-bold tracking-widest text-foreground uppercase text-lg">PHOENIX X</span>
          <span className="bg-primary/20 text-primary text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ml-2">CyberOS</span>
        </div>

        <nav className="hidden md:flex space-x-1 border rounded-lg p-1 bg-secondary/50">
          {workspaces.map(ws => (
            <button
              key={ws.id}
              onClick={() => setActiveWorkspace(ws.id)}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
                activeWorkspace === ws.id 
                  ? 'bg-background shadow-sm text-primary' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
              }`}
            >
              <ws.icon className="h-4 w-4" />
              <span>{ws.name}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="flex items-center space-x-4">
        <button 
          onClick={onOpenSearch}
          className="flex items-center space-x-2 bg-secondary/50 border hover:bg-secondary text-muted-foreground px-4 py-1.5 rounded-full transition-colors text-sm w-64 justify-between"
        >
          <div className="flex items-center">
            <Search className="h-4 w-4 mr-2" />
            <span>Global Enterprise Search...</span>
          </div>
          <kbd className="hidden sm:inline-flex h-5 items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
            <span className="text-xs">⌘</span>K
          </kbd>
        </button>
        
        <div className="flex items-center space-x-2 pl-4 border-l">
           <div className="w-8 h-8 bg-emerald-500/20 text-emerald-500 rounded-full flex items-center justify-center border border-emerald-500/30">
              <Cpu className="h-4 w-4" />
           </div>
        </div>
      </div>
    </header>
  );
}
