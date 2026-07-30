import { useState } from 'react';
import { UnifiedNavigation } from './UnifiedNavigation';
import { ObservabilityDashboard } from './ObservabilityDashboard';
import { GlobalSearchInterface } from './GlobalSearchInterface';
import { UnifiedAIPanel } from './UnifiedAIPanel';
import { Sidebar } from '@/components/layout/Sidebar';
import { Search } from 'lucide-react';

// Note: In a full implementation, CyberOSDesktop would replace the main DashboardLayout
// and handle routing internally. For now, it serves as the capstone dashboard.

export default function CyberOSDesktop() {
  const [activeWorkspace, setActiveWorkspace] = useState('os-kernel');
  const [searchOpen, setSearchOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Universal PHOENIX Sidebar Integration */}
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <UnifiedNavigation onOpenSearch={() => setSearchOpen(true)} activeWorkspace={activeWorkspace} setActiveWorkspace={setActiveWorkspace} />

        <main className="flex-1 overflow-y-auto p-6 bg-slate-900/50">
          {activeWorkspace === 'os-kernel' && <ObservabilityDashboard />}
          {activeWorkspace === 'soc' && <div className="p-10 text-center text-muted-foreground border-2 border-dashed border-muted rounded-xl m-10">Mounting SOC Platform...</div>}
          {activeWorkspace === 'governance' && <div className="p-10 text-center text-muted-foreground border-2 border-dashed border-muted rounded-xl m-10">Mounting Cyber Governance Platform...</div>}
          {activeWorkspace === 'command' && <div className="p-10 text-center text-muted-foreground border-2 border-dashed border-muted rounded-xl m-10">Mounting Cyber Command Platform...</div>}
        </main>

        {searchOpen && (
          <GlobalSearchInterface onClose={() => setSearchOpen(false)} />
        )}
      </div>
      
      {/* Omni-present AI Brain Sidebar */}
      <div className="w-[350px] border-l bg-card hidden 2xl:block z-10 shadow-2xl relative">
        <UnifiedAIPanel currentContext={activeWorkspace} />
      </div>
    </div>
  );
}
