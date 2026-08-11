import { useState } from 'react';
import { Globe, Crosshair, Map, Shield, Activity, Presentation } from 'lucide-react';
import { OperationsDashboard } from './OperationsDashboard';
import { StrategyDashboard } from './StrategyDashboard';
import { RiskGovernanceDashboard } from './RiskGovernanceDashboard';
import { AICopilotPanel } from './AICopilotPanel';

export default function EnterpriseCommandDashboard() {
  const [activeTab, setActiveTab] = useState('global');

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="border-b bg-card px-6 py-4 flex items-center justify-between z-10">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center">
              <Globe className="mr-2 h-6 w-6 text-primary" />
              Enterprise Unified Cyber Command
            </h1>
            <p className="text-sm text-muted-foreground mt-1">
              Apex Situational Awareness & Strategic Operations
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md transition-colors text-sm font-medium">
              <Presentation className="h-4 w-4 mr-2" />
              Executive Briefing Mode
            </button>
          </div>
        </header>

        <div className="border-b bg-muted/30 px-6">
          <nav className="flex space-x-6 overflow-x-auto hide-scrollbar" aria-label="Tabs">
            {[
              { id: 'global', name: 'Global Health & Risk', icon: Activity },
              { id: 'operations', name: 'Cross-Domain Operations', icon: Crosshair },
              { id: 'strategy', name: 'Five-Year Strategy Roadmap', icon: Map },
              { id: 'governance', name: 'Risk & Governance', icon: Shield },
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
          {activeTab === 'global' && <div className="space-y-6 animate-in fade-in duration-500">
            <h2 className="text-xl font-semibold flex items-center">
              <Activity className="mr-2 h-5 w-5 text-primary" />
              Global Enterprise Health
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-card border rounded-lg p-5">
                <h3 className="text-sm font-medium text-muted-foreground mb-1">Overall Posture</h3>
                <div className="text-3xl font-bold tracking-tight text-emerald-500">92.5%</div>
                <p className="text-xs text-muted-foreground mt-1">Stable across 14 domains</p>
              </div>
              <div className="bg-card border rounded-lg p-5">
                <h3 className="text-sm font-medium text-muted-foreground mb-1">Active Operations</h3>
                <div className="text-3xl font-bold tracking-tight text-amber-500">24</div>
                <p className="text-xs text-muted-foreground mt-1">3 High Criticality</p>
              </div>
              <div className="bg-card border rounded-lg p-5">
                <h3 className="text-sm font-medium text-muted-foreground mb-1">Strategic Alignment</h3>
                <div className="text-3xl font-bold tracking-tight text-primary">88.0%</div>
                <p className="text-xs text-muted-foreground mt-1">On track for Q4 Goals</p>
              </div>
              <div className="bg-card border rounded-lg p-5">
                <h3 className="text-sm font-medium text-muted-foreground mb-1">System Resilience</h3>
                <div className="text-3xl font-bold tracking-tight text-emerald-500">99.9%</div>
                <p className="text-xs text-muted-foreground mt-1">RTO metrics satisfied</p>
              </div>
            </div>
            <div className="bg-card border rounded-lg p-6">
               <div className="flex justify-between items-center mb-4">
                 <h3 className="text-lg font-medium">Enterprise Global Topology</h3>
                 <div className="flex space-x-4 text-xs font-medium">
                   <div className="flex items-center"><span className="h-2 w-2 rounded-full bg-emerald-500 mr-2"></span> Healthy</div>
                   <div className="flex items-center"><span className="h-2 w-2 rounded-full bg-amber-500 mr-2"></span> Degraded</div>
                   <div className="flex items-center"><span className="h-2 w-2 rounded-full bg-destructive mr-2"></span> Critical</div>
                 </div>
               </div>
               <div className="h-[400px] relative rounded-lg bg-secondary/10 border overflow-hidden">
                  {/* Decorative background grid to look like a map overlay */}
                  <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, currentColor 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>
                  
                  {/* Regions */}
                  <div className="absolute top-[25%] left-[30%] -translate-x-1/2 -translate-y-1/2 z-10 group">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-emerald-500/10 rounded-full animate-ping opacity-75 pointer-events-none"></div>
                    <div className="relative flex flex-col items-center bg-card border shadow-lg rounded-md p-2 hover:border-primary transition-colors cursor-pointer">
                      <div className="flex items-center space-x-2">
                        <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
                        <span className="font-semibold text-xs whitespace-nowrap">US East (N. Virginia)</span>
                      </div>
                      <div className="text-[10px] text-muted-foreground mt-1">12 active nodes</div>
                    </div>
                  </div>

                  <div className="absolute top-[35%] left-[60%] -translate-x-1/2 -translate-y-1/2 z-10 group">
                    <div className="relative flex flex-col items-center bg-card border shadow-lg rounded-md p-2 hover:border-primary transition-colors cursor-pointer">
                      <div className="flex items-center space-x-2">
                        <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
                        <span className="font-semibold text-xs whitespace-nowrap">EU West (London)</span>
                      </div>
                      <div className="text-[10px] text-muted-foreground mt-1">8 active nodes</div>
                    </div>
                  </div>

                  <div className="absolute top-[65%] left-[80%] -translate-x-1/2 -translate-y-1/2 z-10 group">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-amber-500/10 rounded-full animate-ping opacity-75 pointer-events-none"></div>
                    <div className="relative flex flex-col items-center bg-card border-amber-500/50 shadow-[0_0_15px_rgba(245,158,11,0.2)] rounded-md p-2 hover:border-amber-500 transition-colors cursor-pointer">
                      <div className="flex items-center space-x-2">
                        <span className="h-2.5 w-2.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.8)]"></span>
                        <span className="font-semibold text-xs whitespace-nowrap">AP Southeast (Singapore)</span>
                      </div>
                      <div className="text-[10px] text-amber-500/80 mt-1">High latency detected</div>
                    </div>
                  </div>

                  <div className="absolute top-[45%] left-[15%] -translate-x-1/2 -translate-y-1/2 z-10 group">
                    <div className="relative flex flex-col items-center bg-card border shadow-lg rounded-md p-2 hover:border-primary transition-colors cursor-pointer">
                      <div className="flex items-center space-x-2">
                        <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
                        <span className="font-semibold text-xs whitespace-nowrap">US West (Oregon)</span>
                      </div>
                      <div className="text-[10px] text-muted-foreground mt-1">5 active nodes</div>
                    </div>
                  </div>
                  
                  {/* Connecting SVG Lines */}
                  <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30 text-primary">
                    {/* US East to US West */}
                    <line x1="30%" y1="25%" x2="15%" y2="45%" stroke="currentColor" strokeWidth="1.5" strokeDasharray="4 4" />
                    {/* US East to EU West */}
                    <line x1="30%" y1="25%" x2="60%" y2="35%" stroke="currentColor" strokeWidth="1.5" strokeDasharray="4 4" />
                    {/* EU West to AP Southeast */}
                    <line x1="60%" y1="35%" x2="80%" y2="65%" stroke="currentColor" strokeWidth="1.5" strokeDasharray="4 4" />
                  </svg>
               </div>
            </div>
          </div>}
          {activeTab === 'operations' && <OperationsDashboard />}
          {activeTab === 'strategy' && <StrategyDashboard />}
          {activeTab === 'governance' && <RiskGovernanceDashboard />}
        </main>
      </div>
      
      {/* AI Assistant Sidebar */}
      <div className="w-80 border-l bg-card hidden xl:flex xl:flex-col z-10 shadow-xl h-full">
        <AICopilotPanel />
      </div>
    </div>
  );
}
