import React, { useState } from 'react';
import { apiClient as api } from '@/api/client';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { GitCommit, PlayCircle, CheckCircle, XCircle, Clock } from 'lucide-react';

interface Task {
  id: string;
  task_name: string;
  assigned_agent_id: string;
  status: string;
  dependency_task_ids_json: string[];
}

interface Plan {
  plan_id: string;
  tasks: Task[];
  estimated_duration_seconds: number;
}

export const WorkflowVisualization: React.FC = () => {
  const [objective, setObjective] = useState('');
  const [plan, setPlan] = useState<Plan | null>(null);
  const [loading, setLoading] = useState(false);
  const [executing, setExecuting] = useState(false);

  const generatePlan = async () => {
    if (!objective.trim()) return;
    try {
      setLoading(true);
      const response = await api.post('/multi-agent/plan', { objective });
      setPlan(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const executePlan = async () => {
    if (!plan) return;
    try {
      setExecuting(true);
      await api.post(`/multi-agent/execute/${plan.plan_id}`);
      // In a real app, we would connect to the SSE endpoint here to listen for task updates
      setTimeout(() => setExecuting(false), 2000); // Simulate execution
    } catch (err) {
      console.error(err);
      setExecuting(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'COMPLETED': return <CheckCircle className="w-5 h-5 text-emerald-400" />;
      case 'FAILED': return <XCircle className="w-5 h-5 text-red-400" />;
      case 'RUNNING': return <PlayCircle className="w-5 h-5 text-blue-400 animate-pulse" />;
      default: return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader>
          <CardTitle className="text-xl font-bold text-white flex items-center gap-2">
            <GitCommit className="w-6 h-6 text-blue-400" />
            DAG Workflow Visualization
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <input 
              type="text" 
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              placeholder="Enter investigative objective..." 
              className="flex-1 bg-gray-900 border border-gray-700 rounded-md px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            />
            <button 
              onClick={generatePlan}
              disabled={loading || !objective.trim()}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800/50 disabled:text-gray-400 text-white rounded-md font-medium transition-colors"
            >
              {loading ? 'Planning...' : 'Generate DAG'}
            </button>
          </div>

          {plan && (
            <div className="mt-8 border border-gray-700 rounded-lg bg-gray-900/50 p-6 space-y-6">
              <div className="flex justify-between items-center border-b border-gray-700 pb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-200">Execution Plan</h3>
                  <p className="text-sm text-gray-400 font-mono mt-1">{plan.plan_id}</p>
                </div>
                <button 
                  onClick={executePlan}
                  disabled={executing}
                  className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-800/50 disabled:text-gray-400 text-white rounded-md font-medium transition-colors flex items-center gap-2"
                >
                  <PlayCircle className="w-4 h-4" />
                  {executing ? 'Executing...' : 'Start Execution'}
                </button>
              </div>

              <div className="space-y-4">
                {plan.tasks.map((task, idx) => (
                  <div key={task.id} className="relative flex items-start gap-4">
                    {idx !== plan.tasks.length - 1 && (
                      <div className="absolute left-6 top-8 bottom-0 w-0.5 bg-gray-700 -z-10" />
                    )}
                    
                    <div className="w-12 h-12 rounded-full bg-gray-800 border-2 border-gray-600 flex items-center justify-center shrink-0 mt-1">
                      {getStatusIcon(task.status)}
                    </div>
                    
                    <div className="flex-1 bg-gray-800 border border-gray-700 p-4 rounded-lg">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="text-gray-200 font-medium">{task.task_name}</h4>
                          <p className="text-sm text-gray-400 mt-1">Agent: <span className="text-purple-400 font-mono">{task.assigned_agent_id}</span></p>
                        </div>
                        <Badge variant={task.status === 'PENDING' ? 'secondary' : 'default'}>{task.status}</Badge>
                      </div>
                      
                      {task.dependency_task_ids_json && task.dependency_task_ids_json.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-gray-700">
                          <p className="text-xs text-gray-500">Depends on:</p>
                          <div className="flex flex-wrap gap-2 mt-1">
                            {task.dependency_task_ids_json.map(dep => (
                              <span key={dep} className="text-[10px] font-mono bg-gray-900 px-2 py-1 rounded text-gray-400 border border-gray-700">
                                {dep.substring(0, 8)}...
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
