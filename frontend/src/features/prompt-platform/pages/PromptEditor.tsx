import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Code, Save, Play, FileText, CheckCircle, SearchCode } from 'lucide-react';

export const PromptEditor: React.FC = () => {
  const [systemPrompt, setSystemPrompt] = useState('You are an expert security analyst.\nYour goal is to evaluate the following context and find anomalies.');
  const [userPrompt, setUserPrompt] = useState('Context:\n{{ context }}\n\nIdentify three key risk areas based on the above information.');
  const [testContext, setTestContext] = useState('The user logged in from Russia at 03:00 AM local time using a VPN. They immediately accessed the finance database.');
  
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleTest = async () => {
    setLoading(true);
    try {
      // Mocking the behavior. In a real app we'd POST to /api/v1/prompt-platform/compose
      setTimeout(() => {
        setResult({
          system_prompt: systemPrompt,
          user_prompt: userPrompt.replace('{{ context }}', testContext),
          tokens_estimated: Math.floor((systemPrompt.length + userPrompt.length + testContext.length) / 4)
        });
        setLoading(false);
      }, 600);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <FileText className="w-8 h-8 text-blue-500" />
            Prompt Editor
          </h1>
          <p className="text-gray-400 mt-2">
            Design, validate, and test dynamic Jinja2 prompts before publishing.
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleTest}
            disabled={loading}
            className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors border border-gray-700"
          >
            <Play className="w-4 h-4" />
            Test Render
          </button>
          <button
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors"
          >
            <Save className="w-4 h-4" />
            Save Draft
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-0">
              <div className="bg-gray-800 px-4 py-2 border-b border-gray-700 flex items-center gap-2 text-sm font-medium text-gray-300">
                <Code className="w-4 h-4 text-purple-400" /> System Instructions
              </div>
              <textarea
                value={systemPrompt}
                onChange={(e) => setSystemPrompt(e.target.value)}
                className="w-full h-40 bg-gray-900 text-gray-200 p-4 font-mono text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 rounded-b-lg resize-none"
              />
            </CardContent>
          </Card>

          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-0">
              <div className="bg-gray-800 px-4 py-2 border-b border-gray-700 flex items-center gap-2 text-sm font-medium text-gray-300">
                <Code className="w-4 h-4 text-blue-400" /> User Template (Jinja2)
              </div>
              <textarea
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
                className="w-full h-64 bg-gray-900 text-gray-200 p-4 font-mono text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 rounded-b-lg resize-none"
              />
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-0">
              <div className="bg-gray-800 px-4 py-2 border-b border-gray-700 flex justify-between items-center text-sm font-medium text-gray-300">
                <div className="flex items-center gap-2">
                  <SearchCode className="w-4 h-4 text-orange-400" /> Test Variables
                </div>
              </div>
              <div className="p-4 space-y-3">
                <div>
                  <label className="text-xs text-gray-500 mb-1 block">context</label>
                  <textarea
                    value={testContext}
                    onChange={(e) => setTestContext(e.target.value)}
                    className="w-full h-24 bg-black/50 text-gray-300 p-3 font-mono text-xs border border-gray-700 rounded focus:outline-none focus:border-blue-500 resize-none"
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {result && (
            <Card className="bg-gray-900 border-gray-800 animate-in fade-in slide-in-from-bottom-4">
              <CardContent className="p-0">
                <div className="bg-emerald-900/20 px-4 py-2 border-b border-emerald-900/50 flex justify-between items-center text-sm font-medium text-emerald-400">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" /> Rendered Output Preview
                  </div>
                  <span className="text-xs bg-emerald-900/50 px-2 py-1 rounded-full text-emerald-300 border border-emerald-800/50">
                    ~{result.tokens_estimated} tokens
                  </span>
                </div>
                <div className="p-4">
                  <div className="mb-4">
                    <h5 className="text-xs text-gray-500 mb-2 uppercase tracking-wider">System</h5>
                    <div className="bg-black/50 text-gray-300 p-3 font-mono text-xs rounded border border-gray-800 whitespace-pre-wrap">
                      {result.system_prompt}
                    </div>
                  </div>
                  <div>
                    <h5 className="text-xs text-gray-500 mb-2 uppercase tracking-wider">User</h5>
                    <div className="bg-black/50 text-gray-300 p-3 font-mono text-xs rounded border border-gray-800 whitespace-pre-wrap">
                      {result.user_prompt}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
