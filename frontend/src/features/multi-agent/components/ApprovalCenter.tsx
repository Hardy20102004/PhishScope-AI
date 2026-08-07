import React, { useEffect, useState } from 'react';
import { apiClient as api } from '@/api/client';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { UserCheck, AlertTriangle, Check, X } from 'lucide-react';

interface ApprovalRequest {
  id: string;
  task_id: string;
  requesting_agent_id: string;
  description: string;
  risk_severity: string;
  status: string;
  created_at: string;
}

export const ApprovalCenter: React.FC = () => {
  const [requests, setRequests] = useState<ApprovalRequest[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchApprovals = async () => {
    try {
      setLoading(true);
      const response = await api.get('/multi-agent/approvals');
      setRequests(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApprovals();
  }, []);

  const handleDecision = async (id: string, decision: 'APPROVED' | 'REJECTED') => {
    try {
      await api.post(`/multi-agent/approvals/${id}/decision`, {
        status: decision,
        reviewer_user_id: "00000000-0000-0000-0000-000000000000", // placeholder
        reviewer_feedback: decision === 'REJECTED' ? 'Rejected by analyst' : 'Approved by analyst'
      });
      fetchApprovals(); // Refresh list
    } catch (err) {
      console.error(err);
    }
  };

  const getRiskBadge = (severity: string) => {
    switch(severity) {
      case 'CRITICAL': return <Badge variant="destructive">CRITICAL</Badge>;
      case 'HIGH': return <Badge variant="destructive" className="bg-orange-500 hover:bg-orange-600">HIGH</Badge>;
      case 'MODERATE': return <Badge variant="secondary" className="bg-yellow-500/20 text-yellow-500">MODERATE</Badge>;
      default: return <Badge variant="secondary">LOW</Badge>;
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-400">Loading Approval Queue...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <UserCheck className="w-6 h-6 text-orange-400" />
            Human-in-the-Loop Approvals
          </h2>
          <p className="text-gray-400 text-sm mt-1">Review and approve high-risk automated actions.</p>
        </div>
        <Badge className="px-3 py-1 bg-gray-800 text-gray-300">
          {requests.length} Pending
        </Badge>
      </div>

      {requests.length === 0 ? (
        <div className="py-16 text-center border border-dashed border-gray-700 rounded-lg bg-gray-800/20">
          <Check className="w-12 h-12 text-emerald-500/50 mx-auto mb-3" />
          <p className="text-gray-400">No pending approvals.</p>
          <p className="text-sm text-gray-500 mt-1">All agent workflows are proceeding normally.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {requests.map((req) => (
            <Card key={req.id} className="bg-gray-800 border-l-4 border-l-orange-500 border-gray-700">
              <CardContent className="p-6">
                <div className="flex flex-col md:flex-row justify-between gap-6">
                  <div className="flex-1 space-y-3">
                    <div className="flex items-center gap-3">
                      <AlertTriangle className="w-5 h-5 text-orange-400" />
                      <h3 className="text-lg font-semibold text-gray-200">Action Review Required</h3>
                      {getRiskBadge(req.risk_severity)}
                    </div>
                    
                    <p className="text-gray-300 bg-gray-900/50 p-4 rounded-md border border-gray-700 font-mono text-sm">
                      {req.description}
                    </p>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>Agent: <span className="text-purple-400">{req.requesting_agent_id}</span></span>
                      <span>•</span>
                      <span>Task: <span className="font-mono">{req.task_id.substring(0,8)}...</span></span>
                      <span>•</span>
                      <span>Requested: {new Date(req.created_at).toLocaleString()}</span>
                    </div>
                  </div>
                  
                  <div className="flex md:flex-col gap-3 justify-center">
                    <button 
                      onClick={() => handleDecision(req.id, 'APPROVED')}
                      className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-md font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <Check className="w-4 h-4" /> Approve
                    </button>
                    <button 
                      onClick={() => handleDecision(req.id, 'REJECTED')}
                      className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <X className="w-4 h-4" /> Reject
                    </button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
