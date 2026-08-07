import React from 'react';
import { Database, Link2, BookOpen, AlertCircle } from 'lucide-react';

export default function ContextPanel() {
  return (
      <div className="w-80 bg-slate-900 flex flex-col">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center">
              <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">AI Reasoning Context</h2>
          </div>
          
          <div className="p-4 space-y-6 overflow-y-auto">
              <div>
                  <h3 className="text-xs font-semibold text-slate-500 flex items-center gap-2 mb-3">
                      <Database size={14} /> Retrieved Evidence (RAG)
                  </h3>
                  <div className="space-y-3">
                      <div className="p-3 bg-slate-950 rounded border border-slate-800 hover:border-slate-700 transition-colors cursor-help">
                          <p className="text-xs text-slate-300 leading-relaxed">
                              "HR-05 attempted to bind to IPC$ on 42 finance hosts within a 3-minute window."
                          </p>
                          <div className="flex items-center justify-between mt-2">
                              <span className="text-[10px] text-blue-400 font-mono">Source: Zeek SMB Logs</span>
                              <span className="text-[10px] text-slate-500">95% Match</span>
                          </div>
                      </div>
                  </div>
              </div>

              <div>
                  <h3 className="text-xs font-semibold text-slate-500 flex items-center gap-2 mb-3">
                      <Link2 size={14} /> Knowledge Graph Links
                  </h3>
                  <div className="space-y-2">
                      <div className="flex items-center gap-3 p-2 bg-slate-950 rounded border border-slate-800">
                          <AlertCircle size={14} className="text-rose-500" />
                          <span className="text-xs font-medium text-slate-200">Alert: Suspicious Named Pipe</span>
                      </div>
                      <div className="flex items-center gap-3 p-2 bg-slate-950 rounded border border-slate-800">
                          <BookOpen size={14} className="text-amber-500" />
                          <span className="text-xs font-medium text-slate-200">Threat Actor: APT29</span>
                      </div>
                  </div>
              </div>

              <div className="mt-8 p-4 bg-slate-950/50 rounded-lg border border-slate-800">
                  <p className="text-xs text-slate-400 text-center">
                      AI decisions are based strictly on indexed enterprise evidence.
                  </p>
              </div>
          </div>
      </div>
  );
}
