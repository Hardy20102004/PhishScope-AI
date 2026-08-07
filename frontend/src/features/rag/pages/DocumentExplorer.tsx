import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { UploadCloud, Search, FileText, CheckCircle, Clock, Trash } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const DocumentExplorer: React.FC = () => {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  
  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const res = await api.get('/rag/documents');
      setDocuments(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);
  
  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', uploadFile);
    formData.append('title', uploadFile.name);
    
    try {
      await api.post('/rag/ingest', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setUploadFile(null);
      await fetchDocuments();
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <FileText className="w-8 h-8 text-blue-500" />
            Knowledge Library
          </h1>
          <p className="text-gray-400 mt-2">
            Manage enterprise documents, policies, and playbooks used for RAG grounding.
          </p>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                <UploadCloud className="w-5 h-5 text-blue-400" /> Upload Document
              </h2>
              <form onSubmit={handleUpload} className="space-y-4">
                <div className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:bg-gray-800/50 transition-colors">
                  <input
                    type="file"
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                    <UploadCloud className="w-10 h-10 text-gray-500 mb-2" />
                    <span className="text-sm text-gray-400">
                      {uploadFile ? uploadFile.name : 'Click to browse or drag file here'}
                    </span>
                    <span className="text-xs text-gray-600 mt-1">TXT, MD, JSON, CSV</span>
                  </label>
                </div>
                <button
                  type="submit"
                  disabled={!uploadFile || uploading}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white py-2 rounded-lg font-medium transition-colors"
                >
                  {uploading ? 'Processing & Embedding...' : 'Ingest to Knowledge Base'}
                </button>
              </form>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          <Card className="bg-gray-900 border-gray-800 h-full">
            <CardContent className="p-0">
              <div className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-800/30">
                <div className="relative w-64">
                  <Search className="w-4 h-4 absolute left-3 top-2.5 text-gray-500" />
                  <input
                    type="text"
                    placeholder="Filter documents..."
                    className="w-full bg-black/50 border border-gray-700 rounded-lg pl-9 pr-4 py-2 text-sm focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead className="text-xs text-gray-400 uppercase bg-gray-800/50">
                    <tr>
                      <th className="px-6 py-3 font-medium">Title</th>
                      <th className="px-6 py-3 font-medium">Status</th>
                      <th className="px-6 py-3 font-medium">Date Indexed</th>
                      <th className="px-6 py-3 font-medium text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {loading ? (
                      <tr><td colSpan={4} className="px-6 py-4 text-center text-gray-500">Loading library...</td></tr>
                    ) : documents.length === 0 ? (
                      <tr><td colSpan={4} className="px-6 py-4 text-center text-gray-500">No documents found.</td></tr>
                    ) : (
                      documents.map((doc) => (
                        <tr key={doc.id} className="border-b border-gray-800 hover:bg-gray-800/30 transition-colors">
                          <td className="px-6 py-4 font-medium text-gray-200">
                            <div className="flex items-center gap-2">
                              <FileText className="w-4 h-4 text-gray-500" />
                              {doc.title}
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            {doc.status === 'ACTIVE' ? (
                              <span className="flex items-center gap-1 text-emerald-400 text-xs bg-emerald-900/20 px-2 py-1 rounded w-max border border-emerald-900/50">
                                <CheckCircle className="w-3 h-3" /> ACTIVE
                              </span>
                            ) : (
                              <span className="flex items-center gap-1 text-orange-400 text-xs bg-orange-900/20 px-2 py-1 rounded w-max border border-orange-900/50">
                                <Clock className="w-3 h-3" /> {doc.status}
                              </span>
                            )}
                          </td>
                          <td className="px-6 py-4 text-gray-400">
                            {new Date(doc.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4 text-right">
                            <button className="text-gray-500 hover:text-red-400 transition-colors">
                              <Trash className="w-4 h-4" />
                            </button>
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
      </div>
    </div>
  );
};
