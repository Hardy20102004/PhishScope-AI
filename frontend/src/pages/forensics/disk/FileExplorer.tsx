import React, { useState } from 'react';
import { 
  Folder, 
  File, 
  FileWarning, 
  Search, 
  Binary, 
  ArrowLeft, 
  HardDrive, 
  Download, 
  ShieldAlert, 
  CheckCircle2, 
  FileText,
  FileCheck
} from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useNavigate, useSearchParams } from 'react-router-dom';

interface FileDetail {
  name: string;
  path: string;
  mftRecord: string;
  size: string;
  offset: string;
  hash: string;
  risk: 'DANGER' | 'WARNING' | 'CLEAN';
  deleted: boolean;
  carved: boolean;
  hexLines: { offset: string; hex: string; ascii: string }[];
}

const FILE_DATABASE: Record<string, FileDetail> = {
  'malware.exe': {
    name: 'malware.exe',
    path: 'C:\\Temp\\malware.exe',
    mftRecord: '49212',
    size: '1.2 MB',
    offset: '0x002B4000',
    hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    risk: 'DANGER',
    deleted: false,
    carved: false,
    hexLines: [
      { offset: '00000000', hex: '4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00', ascii: 'MZ..........ÿÿ..' },
      { offset: '00000010', hex: 'B8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00', ascii: '¸.......@.......' },
      { offset: '00000020', hex: '50 45 00 00 4C 01 03 00 E8 DB 95 64 00 00 00 00', ascii: 'PE..L...èÛ.d....' },
      { offset: '00000030', hex: '6D 61 6C 77 61 72 65 5F 70 61 79 6C 6F 61 64 00', ascii: 'malware_payload.' },
      { offset: '00000040', hex: '68 74 74 70 73 3A 2F 2F 63 32 2D 73 65 72 76 65', ascii: 'https://c2-serve' },
      { offset: '00000050', hex: '72 2E 61 74 74 61 63 6B 65 72 2E 63 6F 6D 2F 69', ascii: 'r.attacker.com/i' }
    ]
  },
  'cmd.exe': {
    name: 'cmd.exe',
    path: 'C:\\Windows\\System32\\cmd.exe',
    mftRecord: '1042',
    size: '289 KB',
    offset: '0x00012000',
    hash: 'a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0a1b2',
    risk: 'CLEAN',
    deleted: false,
    carved: false,
    hexLines: [
      { offset: '00000000', hex: '4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00', ascii: 'MZ..........ÿÿ..' },
      { offset: '00000010', hex: 'B8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00', ascii: '¸.......@.......' },
      { offset: '00000020', hex: '57 69 6E 64 6F 77 73 20 43 6F 6D 6D 61 6E 64 20', ascii: 'Windows Command ' },
      { offset: '00000030', hex: '50 72 6F 6D 70 74 20 50 72 6F 63 65 73 73 6F 72', ascii: 'Prompt Processor' }
    ]
  },
  'svchost.exe': {
    name: 'svchost.exe',
    path: 'C:\\Windows\\System32\\svchost.exe',
    mftRecord: '1045',
    size: '54 KB',
    offset: '0x00018400',
    hash: '9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e',
    risk: 'CLEAN',
    deleted: false,
    carved: false,
    hexLines: [
      { offset: '00000000', hex: '4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00', ascii: 'MZ..........ÿÿ..' },
      { offset: '00000010', hex: 'B8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00', ascii: '¸.......@.......' },
      { offset: '00000020', hex: '48 6F 73 74 20 50 72 6F 63 65 73 73 20 66 6F 72', ascii: 'Host Process for' },
      { offset: '00000030', hex: '20 57 69 6E 64 6F 77 73 20 53 65 72 76 69 63 65', ascii: ' Windows Service' }
    ]
  },
  'carved_file_001.pdf (Deleted)': {
    name: 'carved_file_001.pdf',
    path: '[UNALLOCATED]\\carved_file_001.pdf',
    mftRecord: 'UNALLOCATED',
    size: '2.1 MB',
    offset: '0x004B2900',
    hash: '3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e',
    risk: 'WARNING',
    deleted: true,
    carved: true,
    hexLines: [
      { offset: '00000000', hex: '25 50 44 46 2D 31 2E 37 0D 0A 25 C2 B5 C2 B6 0D', ascii: '%PDF-1.7..%µ¶.' },
      { offset: '00000010', hex: '31 20 30 20 6F 62 6A 0D 0A 3C 3C 2F 54 79 70 65', ascii: '1 0 obj..<</Type' },
      { offset: '00000020', hex: '2F 43 61 74 61 6C 6F 67 2F 50 61 67 65 73 20 32', ascii: '/Catalog/Pages 2' },
      { offset: '00000030', hex: '20 30 20 52 3E 3E 0D 0A 65 6E 64 6F 62 6A 0D 0A', ascii: ' 0 R>>..endobj..' }
    ]
  },
  'passwords.txt': {
    name: 'passwords.txt',
    path: 'C:\\Users\\Admin\\Desktop\\passwords.txt',
    mftRecord: '38102',
    size: '1.4 KB',
    offset: '0x001A8000',
    hash: '7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d7c6b',
    risk: 'WARNING',
    deleted: false,
    carved: false,
    hexLines: [
      { offset: '00000000', hex: '55 73 65 72 3A 20 61 64 6D 69 6E 0A 50 61 73 73', ascii: 'User: admin.Pass' },
      { offset: '00000010', hex: '77 6F 72 64 3A 20 53 75 70 65 72 53 65 63 75 72', ascii: 'word: SuperSecur' },
      { offset: '00000020', hex: '65 32 30 32 36 21 0A 41 57 53 5F 4B 65 79 3A 20', ascii: 'e2026!.AWS_Key: ' },
      { offset: '00000030', hex: '41 4B 49 41 49 4F 53 46 4F 44 4E 4E 37 45 58 41', ascii: 'AKIAIOSFODNN7EXA' }
    ]
  }
};

export default function FileExplorer() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const imageName = searchParams.get('image') || 'DESKTOP-HR05-ACQ.E01';

  const [selectedFileName, setSelectedFileName] = useState<string>('malware.exe');
  const [searchTerm, setSearchTerm] = useState('');

  const activeDetail = FILE_DATABASE[selectedFileName] || FILE_DATABASE['malware.exe'];

  const matchesSearch = (text: string) => {
    if (!searchTerm) return true;
    return text.toLowerCase().includes(searchTerm.toLowerCase());
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-slate-950 text-slate-100 font-sans border-t border-slate-800">
      
      {/* Top Header Bar */}
      <div className="bg-slate-900 border-b border-slate-800 px-6 py-3 flex justify-between items-center shrink-0">
        <div className="flex items-center gap-4">
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => navigate('/disk-forensics')}
            className="text-slate-400 hover:text-white hover:bg-slate-800 gap-2"
          >
            <ArrowLeft size={16} /> Back to Dashboard
          </Button>
          <div className="h-4 w-px bg-slate-800" />
          <div className="flex items-center gap-2">
            <HardDrive size={18} className="text-cyan-400" />
            <span className="font-bold text-sm text-slate-200">{imageName}</span>
            <span className="text-xs bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded font-mono">
              NTFS MFT Parsed
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
          <span>Active Files: <strong className="text-slate-200">1,420</strong></span>
          <span>•</span>
          <span>Deleted Artifacts: <strong className="text-amber-400">142</strong></span>
        </div>
      </div>

      {/* Main Split Content */}
      <div className="flex flex-1 overflow-hidden">
        
        {/* Left MFT Directory Tree Pane */}
        <div className="w-1/3 border-r border-slate-800 flex flex-col bg-slate-900/40">
          <div className="p-4 border-b border-slate-800">
            <div className="flex items-center gap-2 bg-slate-950 rounded border border-slate-800 px-3 py-1.5 focus-within:border-cyan-500 transition-colors">
              <Search size={16} className="text-slate-400" />
              <Input 
                className="border-none h-6 bg-transparent text-sm focus-visible:ring-0 placeholder:text-slate-600 text-slate-200" 
                placeholder="Search MFT records & files..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="p-4 space-y-3 overflow-y-auto font-mono text-sm flex-1">
            
            {/* Windows Folder */}
            {matchesSearch('Windows') && (
              <div>
                <TreeItem icon={<Folder className="text-blue-400" size={16} />} text="Windows" />
                <div className="pl-6 space-y-1 border-l border-slate-800/80 ml-2 mt-1">
                  {matchesSearch('System32') && (
                    <div>
                      <TreeItem icon={<Folder className="text-blue-400" size={16} />} text="System32" />
                      <div className="pl-6 space-y-1 border-l border-slate-800/80 ml-2 mt-1">
                        {matchesSearch('cmd.exe') && (
                          <TreeItem 
                            icon={<File className="text-slate-400" size={16} />} 
                            text="cmd.exe" 
                            isActive={selectedFileName === 'cmd.exe'} 
                            onClick={() => setSelectedFileName('cmd.exe')} 
                          />
                        )}
                        {matchesSearch('svchost.exe') && (
                          <TreeItem 
                            icon={<File className="text-slate-400" size={16} />} 
                            text="svchost.exe" 
                            isActive={selectedFileName === 'svchost.exe'} 
                            onClick={() => setSelectedFileName('svchost.exe')} 
                          />
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Users Folder */}
            {matchesSearch('Users') && (
              <div>
                <TreeItem icon={<Folder className="text-blue-400" size={16} />} text="Users\Admin\Desktop" />
                <div className="pl-6 space-y-1 border-l border-slate-800/80 ml-2 mt-1">
                  {matchesSearch('passwords.txt') && (
                    <TreeItem 
                      icon={<FileText className="text-amber-400" size={16} />} 
                      text="passwords.txt" 
                      warning 
                      isActive={selectedFileName === 'passwords.txt'} 
                      onClick={() => setSelectedFileName('passwords.txt')} 
                    />
                  )}
                </div>
              </div>
            )}

            {/* Temp Folder */}
            {matchesSearch('Temp') && (
              <div>
                <TreeItem icon={<Folder className="text-blue-400" size={16} />} text="Temp" />
                <div className="pl-6 space-y-1 border-l border-slate-800/80 ml-2 mt-1">
                  {matchesSearch('malware.exe') && (
                    <TreeItem 
                      icon={<FileWarning className="text-rose-500" size={16} />} 
                      text="malware.exe" 
                      danger 
                      isActive={selectedFileName === 'malware.exe'} 
                      onClick={() => setSelectedFileName('malware.exe')} 
                    />
                  )}
                </div>
              </div>
            )}

            {/* Unallocated Space Carving Folder */}
            {matchesSearch('UNALLOCATED') && (
              <div>
                <TreeItem icon={<Folder className="text-rose-900" size={16} />} text="[UNALLOCATED SPACE]" />
                <div className="pl-6 space-y-1 border-l border-slate-800/80 ml-2 mt-1">
                  {matchesSearch('carved_file_001.pdf (Deleted)') && (
                    <TreeItem 
                      icon={<File className="text-amber-500" size={16} />} 
                      text="carved_file_001.pdf (Deleted)" 
                      warning 
                      isActive={selectedFileName === 'carved_file_001.pdf (Deleted)'} 
                      onClick={() => setSelectedFileName('carved_file_001.pdf (Deleted)')} 
                    />
                  )}
                </div>
              </div>
            )}

          </div>
        </div>

        {/* Right Detail Pane (Hex Viewer Simulation & Metadata) */}
        <div className="w-2/3 flex flex-col bg-slate-950">
          
          {/* File Header Details */}
          <div className="p-5 border-b border-slate-800 bg-slate-900/90 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <div className="flex items-center gap-2">
                {activeDetail.risk === 'DANGER' ? (
                  <FileWarning className="text-rose-500" size={20} />
                ) : activeDetail.risk === 'WARNING' ? (
                  <FileText className="text-amber-400" size={20} />
                ) : (
                  <FileCheck className="text-emerald-400" size={20} />
                )}
                <h3 className="font-bold text-lg text-slate-100">{activeDetail.name}</h3>
                
                {activeDetail.risk === 'DANGER' && (
                  <span className="text-xs bg-rose-500/10 text-rose-400 border border-rose-500/20 px-2 py-0.5 rounded font-bold flex items-center gap-1">
                    <ShieldAlert size={12} /> Suspicious Binary
                  </span>
                )}
                {activeDetail.carved && (
                  <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-0.5 rounded font-medium">
                    Carved File
                  </span>
                )}
              </div>

              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-400 mt-2 font-mono">
                <span>Path: <strong className="text-slate-300">{activeDetail.path}</strong></span>
                <span>MFT Record: <strong className="text-cyan-400">{activeDetail.mftRecord}</strong></span>
                <span>Size: <strong className="text-slate-300">{activeDetail.size}</strong></span>
                <span>Offset: <strong className="text-slate-300">{activeDetail.offset}</strong></span>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded border border-slate-800 font-mono text-xs text-cyan-400">
                <Binary size={14} /> HEX INSPECTOR
              </div>
              <Button 
                variant="outline" 
                size="sm"
                className="border-slate-700 bg-slate-800 hover:bg-slate-700 text-xs gap-1.5"
                onClick={() => alert(`Exported hex dump for ${activeDetail.name}`)}
              >
                <Download size={14} /> Export Hex
              </Button>
            </div>
          </div>

          {/* Hex Viewer Grid */}
          <div className="flex-1 p-6 overflow-y-auto font-mono text-sm leading-relaxed space-y-4">
            
            <div className="bg-slate-900/50 p-3 rounded border border-slate-800 text-xs flex justify-between text-slate-400">
              <span>SHA-256: <strong className="text-slate-300 select-all">{activeDetail.hash}</strong></span>
              <span>Status: <strong className={activeDetail.deleted ? "text-rose-400" : "text-emerald-400"}>{activeDetail.deleted ? "DELETED" : "ALLOCATED"}</strong></span>
            </div>

            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
              <div className="grid grid-cols-12 text-xs font-bold text-slate-500 border-b border-slate-800/80 pb-2">
                <span className="col-span-2 text-slate-600">OFFSET</span>
                <span className="col-span-7 text-emerald-400/90">HEXADECIMAL BYTES</span>
                <span className="col-span-3 text-cyan-400/90">ASCII</span>
              </div>

              {activeDetail.hexLines.map((line, idx) => (
                <div key={idx} className="grid grid-cols-12 text-xs hover:bg-slate-900/80 p-1 rounded font-mono transition-colors">
                  <span className="col-span-2 text-slate-500 select-none">{line.offset}</span>
                  <span className="col-span-7 text-emerald-400/80 tracking-widest">{line.hex}</span>
                  <span className="col-span-3 text-slate-300 truncate">{line.ascii}</span>
                </div>
              ))}
            </div>

            {/* AI Forensic Insight note */}
            {activeDetail.risk === 'DANGER' && (
              <div className="p-4 bg-rose-950/20 border border-rose-500/30 rounded-lg text-xs space-y-2">
                <div className="flex items-center gap-2 text-rose-400 font-bold">
                  <ShieldAlert size={16} /> Forensic AI Analysis Output
                </div>
                <p className="text-rose-200/90 leading-relaxed">
                  Detected hardcoded HTTP call to C2 server domain <code>https://c2-server.attacker.com/i</code> inside section header offset <code>0x00000040</code>. File exhibits process injection capabilities.
                </p>
              </div>
            )}

          </div>

        </div>

      </div>

    </div>
  );
}

function TreeItem({ icon, text, danger, warning, isActive, onClick }: any) {
    let colorClass = 'text-slate-300';
    if (danger) colorClass = 'text-rose-400 font-bold';
    else if (warning) colorClass = 'text-amber-400 italic';
    else if (isActive) colorClass = 'text-cyan-400 font-bold';
    
    return (
        <div 
            className={`flex items-center gap-2 cursor-pointer hover:bg-slate-800/60 py-1.5 px-2 rounded transition-colors group ${isActive ? 'bg-slate-800 border-l-2 border-cyan-500' : ''}`}
            onClick={onClick}
        >
            {icon}
            <span className={colorClass}>{text}</span>
        </div>
    );
}
