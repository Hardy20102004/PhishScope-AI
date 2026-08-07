import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { BrainCircuit, CheckCircle, ShieldAlert, Activity, GitCommit } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiClient as api } from '@/api/client';

export const DecisionDashboard: React.FC = () => {
  const [decisions, setDecisions] = useState<any[]>([]);
  
  const fetchDecisions = async () => {
    try {
      const res = await api.get('/decision/');
      setDecisions(res.data);
    } catch (err) {
      console.error(err);
    }
  };


  useEffect(() => {
    fetchDecisions();
  }, []);

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <BrainCircuit className="w-8 h-8 text-cyan-500" />
            AI Decision Engine
          </h1>
          <p className="text-gray-400 mt-2 max-w-3xl">
            Human-in-the-loop recommendation and reasoning layer.
          </p>
        </div>
        <div className="flex gap-3">
          <Link 
            to="/decision/approval"
            className="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors border border-cyan-500/50 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
          >
            <ShieldAlert className="w-5 h-5" />
            Approval Center
          </Link>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-4 mb-10">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-5 h-5 text-blue-400" />
              <p className="text-sm font-medium text-gray-400">Total Decisions</p>
            </div>
            <h3 className="text-3xl font-bold text-white">{decisions.length || 0}</h3>
            <p className="text-xs text-gray-500 mt-1">Evaluated in last 30 days</p>
          </CardContent>
        </Card>
        
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <CheckCircle className="w-5 h-5 text-emerald-400" />
              <p className="text-sm font-medium text-gray-400">Avg Confidence</p>
            </div>
            <h3 className="text-3xl font-bold text-white">82%</h3>
            <p className="text-xs text-gray-500 mt-1">Across all decision types</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <ShieldAlert className="w-5 h-5 text-orange-400" />
              <p className="text-sm font-medium text-gray-400">Pending Review</p>
            </div>
            <h3 className="text-3xl font-bold text-white">
              {decisions.filter(d => d.state === 'PENDING_REVIEW' || d.state === 'POLICY_BLOCKED').length}
            </h3>
            <p className="text-xs text-orange-500 mt-1">Require human oversight</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <GitCommit className="w-5 h-5 text-purple-400" />
              <p className="text-sm font-medium text-gray-400">Override Rate</p>
            </div>
            <h3 className="text-3xl font-bold text-white">4.2%</h3>
            <p className="text-xs text-purple-500 mt-1">Decisions rejected by human</p>
          </CardContent>
        </Card>
      </div>
      
      {/* Recent Decisions Table */}
      <h2 className="text-xl font-semibold mb-4 text-white">Recent Decisions</h2>
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-400 uppercase bg-gray-800/50">
                <tr>
                  <th className="px-6 py-3 font-medium">ID</th>
                  <th className="px-6 py-3 font-medium">Type</th>
                  <th className="px-6 py-3 font-medium">Status</th>
                  <th className="px-6 py-3 font-medium">Confidence</th>
                  <th className="px-6 py-3 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {decisions.length === 0 ? (
                  <tr><td colSpan={5} className="px-6 py-4 text-center text-gray-500">No decisions evaluated yet.</td></tr>
                ) : (
                  decisions.map((d) => (
                    <tr key={d.id} className="border-b border-gray-800 hover:bg-gray-800/30 transition-colors">
                      <td className="px-6 py-4 font-mono text-xs text-gray-500">{d.id.substring(0,8)}...</td>
                      <td className="px-6 py-4 text-gray-300">{d.decision_type}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded text-xs border ${
                          d.state === 'APPROVED' ? 'bg-emerald-900/30 border-emerald-900 text-emerald-400' :
                          d.state === 'REJECTED' ? 'bg-red-900/30 border-red-900 text-red-400' :
                          'bg-orange-900/30 border-orange-900 text-orange-400'
                        }`}>
                          {d.state}
                        </span>
                      </td>
                      <td className="px-6 py-4">{(d.confidence * 100).toFixed(0)}%</td>
                      <td className="px-6 py-4 text-right">
                        <Link to={`/decision/view/${d.id}`} className="text-cyan-400 hover:text-cyan-300">View</Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
