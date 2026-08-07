import { useState, useEffect } from 'react';
import { Shield, Briefcase, FileText, Activity, CheckSquare, TrendingUp, Presentation, BrainCircuit } from 'lucide-react';
import { BoardDashboard } from './BoardDashboard';
import { PolicyDashboard } from './PolicyDashboard';
import { RiskOversightDashboard } from './RiskOversightDashboard';
import { ComplianceDashboard } from './ComplianceDashboard';
import { InvestmentDashboard } from './InvestmentDashboard';
import { AIExecutiveGovernanceAssistant } from './AIExecutiveGovernanceAssistant';

export default function ExecutiveGovernanceDashboard() {
  const [activeTab, setActiveTab] = useState('board');
  const [isPresentationMode, setIsPresentationMode] = useState(false);

  const togglePresentation = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`)
      })
      setIsPresentationMode(true)
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen()
        setIsPresentationMode(false)
      }
    }
  }

  return (
    <div className={`flex h-screen overflow-hidden ${isPresentationMode ? 'bg-background' : 'bg-background'}`}>
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="border-b bg-card px-6 py-4 flex items-center justify-between z-10">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center">
              <Shield className="mr-2 h-6 w-6 text-primary" />
              Cyber Governance & Executive Strategy
            </h1>
            <p className="text-sm text-muted-foreground mt-1">
              Executive Decision Intelligence & Board-Level Security
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <button 
              onClick={togglePresentation}
              className="flex items-center space-x-2 bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md transition-colors text-sm font-medium"
            >
              <Presentation className="h-4 w-4 mr-2" />
              {isPresentationMode ? 'Exit Presentation Mode' : 'Board Presentation Mode'}
            </button>
          </div>
        </header>

        <div className="border-b bg-muted/30 px-6">
          <nav className="flex space-x-6 overflow-x-auto hide-scrollbar" aria-label="Tabs">
            {[
              { id: 'board', name: 'Board Reporting', icon: Briefcase },
              { id: 'risk', name: 'Risk Oversight', icon: Activity },
              { id: 'policy', name: 'Policy Governance', icon: FileText },
              { id: 'compliance', name: 'Compliance', icon: CheckSquare },
              { id: 'investment', name: 'Investment & Strategy', icon: TrendingUp },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-4 px-1 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-primary text-primary'
                    : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border'
                }`}
              >
                <tab.icon className="mr-2 h-4 w-4" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <main className="flex-1 overflow-y-auto p-6">
          {activeTab === 'board' && <BoardDashboard />}
          {activeTab === 'risk' && <RiskOversightDashboard />}
          {activeTab === 'policy' && <PolicyDashboard />}
          {activeTab === 'compliance' && <ComplianceDashboard />}
          {activeTab === 'investment' && <InvestmentDashboard />}
        </main>
      </div>
      
      {/* AI Assistant Sidebar */}
      <div className="w-80 border-l bg-card hidden xl:flex xl:flex-col h-full z-10 shadow-xl">
        <AIExecutiveGovernanceAssistant />
      </div>
    </div>
  );
}
