import { useState, useEffect } from 'react';
import { Network, Database, ShieldAlert, CheckCircle, Activity, BrainCircuit } from 'lucide-react';
import { OntologyDashboard } from './OntologyDashboard';
import { RelationshipExplorer } from './RelationshipExplorer';
import { KnowledgeQualityDashboard } from './KnowledgeQualityDashboard';
import { SchemaRecommendationDashboard } from './SchemaRecommendationDashboard';
import { AIKnowledgeEvolutionAssistant } from './AIKnowledgeEvolutionAssistant';

export default function KnowledgeEvolutionDashboard() {
  const [activeTab, setActiveTab] = useState('ontology');

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="border-b bg-card px-6 py-4 flex items-center justify-between z-10">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center">
              <Network className="mr-2 h-6 w-6 text-primary" />
              Enterprise Knowledge Evolution Platform
            </h1>
            <p className="text-sm text-muted-foreground mt-1">
              Autonomous Knowledge Graph Evolution & AI Learning
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 bg-secondary/50 rounded-md px-3 py-1.5">
              <CheckCircle className="h-4 w-4 text-emerald-500" />
              <span className="text-sm font-medium">Evolution Engine Active</span>
            </div>
          </div>
        </header>

        <div className="border-b bg-muted/30 px-6">
          <nav className="flex space-x-6" aria-label="Tabs">
            {[
              { id: 'ontology', name: 'Ontology Management', icon: Database },
              { id: 'relationships', name: 'Relationship Explorer', icon: Network },
              { id: 'quality', name: 'Knowledge Quality', icon: Activity },
              { id: 'recommendations', name: 'Schema Recommendations', icon: ShieldAlert },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-4 px-1 border-b-2 text-sm font-medium transition-colors ${
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
          {activeTab === 'ontology' && <OntologyDashboard />}
          {activeTab === 'relationships' && <RelationshipExplorer />}
          {activeTab === 'quality' && <KnowledgeQualityDashboard />}
          {activeTab === 'recommendations' && <SchemaRecommendationDashboard />}
        </main>
      </div>
      
      {/* AI Assistant Sidebar */}
      <div className="w-80 border-l bg-card hidden xl:flex xl:flex-col h-full z-10 shadow-xl">
        <AIKnowledgeEvolutionAssistant />
      </div>
    </div>
  );
}
