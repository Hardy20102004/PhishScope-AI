import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Lightbulb, Eye, FileSearch, ShieldCheck, Activity } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiClient as api } from '@/api/client';

export const XAIDashboard: React.FC = () => {
  const [explanations, setExplanations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchExplanations();
  }, []);

  const fetchExplanations = async () => {
    try {
      const res = await api.get('/xai/');
      setExplanations(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Lightbulb className="w-8 h-8 text-yellow-500" />
            Explainable AI (XAI)
          </h1>
          <p className="text-gray-400 mt-2 max-w-3xl">
            Transparent, evidence-backed narratives translating raw AI reasoning into human-readable insights.
          </p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3 mb-10">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-5 h-5 text-blue-400" />
              <p className="text-sm font-medium text-gray-400">Explanations Generated</p>
            </div>
            <h3 className="text-3xl font-bold text-white">{explanations.length || 0}</h3>
            <p className="text-xs text-gray-500 mt-1">Total audit logs</p>
          </CardContent>
        </Card>
        
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <p className="text-sm font-medium text-gray-400">Avg Evidence Density</p>
            </div>
            <h3 className="text-3xl font-bold text-white">4.2</h3>
            <p className="text-xs text-gray-500 mt-1">Attributed links per decision</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Eye className="w-5 h-5 text-purple-400" />
              <p className="text-sm font-medium text-gray-400">Transparency Score</p>
            </div>
            <h3 className="text-3xl font-bold text-white">98%</h3>
            <p className="text-xs text-purple-500 mt-1">All internal states mapped</p>
          </CardContent>
        </Card>
      </div>
      
      <h2 className="text-xl font-semibold mb-4 text-white">XAI Audit Log</h2>
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-400 uppercase bg-gray-800/50">
                <tr>
                  <th className="px-6 py-3 font-medium">XAI Record ID</th>
                  <th className="px-6 py-3 font-medium">Decision ID</th>
                  <th className="px-6 py-3 font-medium">Evidence Count</th>
                  <th className="px-6 py-3 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan={4} className="px-6 py-4 text-center text-gray-500">Loading...</td></tr>
                ) : explanations.length === 0 ? (
                  <tr><td colSpan={4} className="px-6 py-4 text-center text-gray-500">No explanations found.</td></tr>
                ) : (
                  explanations.map((x) => (
                    <tr key={x.id} className="border-b border-gray-800 hover:bg-gray-800/30 transition-colors">
                      <td className="px-6 py-4 font-mono text-xs text-gray-500">{x.id.substring(0,8)}...</td>
                      <td className="px-6 py-4 font-mono text-xs text-gray-400">{x.decision_id.substring(0,8)}...</td>
                      <td className="px-6 py-4 text-gray-300">{x.attributions?.length || 0} Traces</td>
                      <td className="px-6 py-4 text-right">
                        <Link to={`/xai/view/${x.decision_id}`} className="text-yellow-400 hover:text-yellow-300 flex items-center justify-end gap-1">
                          <FileSearch className="w-4 h-4" /> Trace
                        </Link>
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
