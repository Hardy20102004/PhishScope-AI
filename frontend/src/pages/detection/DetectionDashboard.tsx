import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Activity, ShieldCheck, FileCode, CheckCircle, GitPullRequest } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function DetectionDashboard() {
  const navigate = useNavigate();

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-500">
            Detection Engineering
          </h1>
          <p className="text-slate-400 mt-2">Manage, Author, and Test Enterprise Detection Rules</p>
        </div>
        <div className="flex gap-4">
          <Button onClick={() => navigate('/detection/rules')} variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800">
            Rule Explorer
          </Button>
          <Button onClick={() => navigate('/detection/editor')} className="bg-emerald-600 hover:bg-emerald-700 text-white">
            <FileCode size={16} className="mr-2" />
            Create Rule
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Active Rules" value="482" icon={<ShieldCheck className="text-emerald-400" />} trend="+5 this week" />
        <MetricCard title="Drafts In Progress" value="14" icon={<FileCode className="text-blue-400" />} trend="Stable" />
        <MetricCard title="Pending Approvals" value="3" icon={<GitPullRequest className="text-orange-400" />} trend="Requires Attention" alert />
        <MetricCard title="Testing Coverage" value="94%" icon={<CheckCircle className="text-cyan-400" />} trend="+2% from last month" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <Card className="bg-slate-900 border-slate-800 backdrop-blur-xl">
          <CardHeader>
             <CardTitle className="text-slate-200">Rule Type Distribution</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-slate-300">Sigma Rules</span>
              <Badge className="bg-emerald-900 text-emerald-400">350</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-300">YARA Rules</span>
              <Badge className="bg-blue-900 text-blue-400">110</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-300">Custom Correlation</span>
              <Badge className="bg-purple-900 text-purple-400">22</Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800 backdrop-blur-xl">
          <CardHeader>
             <CardTitle className="text-slate-200">Recent Workflow Activity</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
             <div className="flex items-center gap-4 text-sm text-slate-300">
                <GitPullRequest size={16} className="text-orange-400" />
                <span className="flex-1">Rule "Suspicious PowerShell Download" moved to IN_REVIEW</span>
                <span className="text-slate-500">2h ago</span>
             </div>
             <div className="flex items-center gap-4 text-sm text-slate-300">
                <CheckCircle size={16} className="text-emerald-400" />
                <span className="flex-1">Rule "Mimikatz LSASS Access" APPROVED</span>
                <span className="text-slate-500">5h ago</span>
             </div>
             <div className="flex items-center gap-4 text-sm text-slate-300">
                <Activity size={16} className="text-cyan-400" />
                <span className="flex-1">Testing Suite completed for 14 Drafts</span>
                <span className="text-slate-500">1d ago</span>
             </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend, alert = false }: any) {
  return (
    <Card className={`bg-slate-900 border-slate-800 hover:bg-slate-800/80 transition-all duration-300 ${alert ? 'shadow-[0_0_15px_rgba(249,115,22,0.15)] border-orange-500/30' : ''}`}>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-slate-400">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold text-slate-100">{value}</div>
        <p className={`text-xs mt-2 ${trend.includes('Attention') ? 'text-orange-400' : 'text-slate-500'}`}>{trend}</p>
      </CardContent>
    </Card>
  );
}
