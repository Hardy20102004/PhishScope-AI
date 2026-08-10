import { Briefcase, Download, TrendingUp, ShieldCheck } from 'lucide-react';

export function BoardDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold flex items-center">
            <Briefcase className="mr-2 h-5 w-5 text-primary" />
            Board of Directors Reporting
          </h2>
          <p className="text-sm text-muted-foreground">Sanitized, high-level metrics for the Board and Risk Committee.</p>
        </div>
        <button className="flex items-center px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/80 transition-colors">
          <Download className="mr-2 h-4 w-4" />
          Export Q3 Report
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-card border rounded-lg p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-medium text-foreground">Overall Cyber Maturity</h3>
            <ShieldCheck className="h-5 w-5 text-emerald-500" />
          </div>
          <div>
            <div className="text-4xl font-bold tracking-tight text-foreground">4.2<span className="text-xl text-muted-foreground font-normal">/5</span></div>
            <p className="text-sm text-emerald-500 flex items-center mt-2">
              <TrendingUp className="h-3 w-3 mr-1" /> +0.3 from last quarter
            </p>
          </div>
        </div>

        <div className="bg-card border rounded-lg p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-medium text-foreground">Enterprise Risk Level</h3>
            <TrendingUp className="h-5 w-5 text-amber-500" />
          </div>
          <div>
            <div className="text-4xl font-bold tracking-tight text-foreground">Moderate</div>
            <p className="text-sm text-muted-foreground mt-2">Within defined Risk Appetite</p>
          </div>
        </div>

        <div className="bg-card border rounded-lg p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-medium text-foreground">Key Investment Focus</h3>
            <Briefcase className="h-5 w-5 text-primary" />
          </div>
          <div>
            <div className="text-2xl font-bold tracking-tight text-foreground">Zero Trust & IAM</div>
            <p className="text-sm text-muted-foreground mt-2">Aligning with Q3-Q4 strategic goals.</p>
          </div>
        </div>
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Quarterly Threat Landscape Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-foreground">Phishing Attacks</span>
                <span className="text-amber-500 font-medium">↑ 15%</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div className="bg-amber-500 h-2 rounded-full" style={{ width: '65%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-foreground">Ransomware Attempts</span>
                <span className="text-emerald-500 font-medium">↓ 8%</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '30%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-foreground">Insider Threats</span>
                <span className="text-muted-foreground font-medium">- 0%</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div className="bg-muted-foreground h-2 rounded-full" style={{ width: '15%' }}></div>
              </div>
            </div>
          </div>
          <div className="bg-secondary/20 rounded-lg p-4 flex flex-col justify-center items-center text-center border border-border/50">
            <h4 className="text-3xl font-bold text-foreground mb-2">1,248</h4>
            <p className="text-sm text-muted-foreground mb-4">Total Incidents Prevented</p>
            <div className="text-xs text-primary bg-primary/10 px-3 py-1 rounded-full border border-primary/20">
              High Prevention Rate
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
