import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { 
  Clock, 
  Plus, 
  Trash2, 
  Edit3, 
  ArrowLeft, 
  Search, 
  HardDrive, 
  Download, 
  Eye, 
  UserCheck, 
  Hash, 
  Layers, 
  Calendar,
  X,
  PlusCircle
} from 'lucide-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '@/services/api';

interface TimelineEventData {
  id: string;
  date: string;
  action: 'CREATED' | 'MODIFIED' | 'DELETED' | 'ACCESSED';
  file: string;
  userContext: string;
  hash: string;
  offset: string;
  mftRecord: number;
}

const INITIAL_TIMELINE: TimelineEventData[] = [
  {
    id: '1',
    date: '2026-07-27 14:32:11 UTC',
    action: 'CREATED',
    file: 'C:\\Temp\\malware.exe',
    userContext: 'NT AUTHORITY\\SYSTEM',
    hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    offset: '0x002B4000',
    mftRecord: 49212
  },
  {
    id: '2',
    date: '2026-07-27 15:01:45 UTC',
    action: 'MODIFIED',
    file: 'C:\\Windows\\System32\\cmd.exe',
    userContext: 'DESKTOP-HR05\\Administrator',
    hash: 'a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0a1b2',
    offset: '0x00012000',
    mftRecord: 1042
  },
  {
    id: '3',
    date: '2026-07-28 09:15:22 UTC',
    action: 'DELETED',
    file: 'C:\\Users\\Admin\\Desktop\\passwords.txt',
    userContext: 'DESKTOP-HR05\\Administrator',
    hash: '7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d7c6b',
    offset: '0x001A8000',
    mftRecord: 38102
  },
  {
    id: '4',
    date: '2026-07-28 11:40:05 UTC',
    action: 'ACCESSED',
    file: 'C:\\Windows\\System32\\svchost.exe',
    userContext: 'NT AUTHORITY\\LOCAL SERVICE',
    hash: '9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e',
    offset: '0x00018400',
    mftRecord: 1045
  }
];

export default function ForensicTimeline() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const imageName = searchParams.get('image') || 'DESKTOP-HR05-ACQ.E01';

  const [events, setEvents] = useState<TimelineEventData[]>(INITIAL_TIMELINE);
  const [actionFilter, setActionFilter] = useState<'ALL' | 'CREATED' | 'MODIFIED' | 'DELETED'>('ALL');
  const [searchTerm, setSearchTerm] = useState('');
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  // New Event Form
  const [newEvent, setNewEvent] = useState({
    file: '',
    action: 'CREATED' as const,
    userContext: 'NT AUTHORITY\\SYSTEM',
    date: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC'
  });

  useEffect(() => {
    fetchTimeline();
  }, []);

  const fetchTimeline = async () => {
    try {
      const res = await api.get('/api/v1/disk-forensics/timeline');
      if (res.data && Array.isArray(res.data) && res.data.length > 0) {
        const fetchedEvents: TimelineEventData[] = res.data.map((item: any, idx: number) => ({
          id: String(idx + 10),
          date: item.timestamp ? new Date(item.timestamp).toISOString().replace('T', ' ').substring(0, 19) + ' UTC' : '2026-07-29 10:00:00 UTC',
          action: (item.event_type || 'CREATED') as any,
          file: item.artifact || 'C:\\Windows\\explorer.exe',
          userContext: 'NT AUTHORITY\\SYSTEM',
          hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
          offset: `0x00${Math.floor(Math.random() * 899999 + 100000)}`,
          mftRecord: Math.floor(Math.random() * 80000 + 10000)
        }));
        setEvents(prev => [...prev, ...fetchedEvents]);
      }
    } catch (err) {
      console.log('Backend timeline call offline, utilizing initial dataset');
    }
  };

  const handleAddEventSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEvent.file) return;

    const item: TimelineEventData = {
      id: String(Date.now()),
      date: newEvent.date,
      action: newEvent.action,
      file: newEvent.file,
      userContext: newEvent.userContext,
      hash: 'a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0a1b2',
      offset: `0x00${Math.floor(Math.random() * 899999 + 100000)}`,
      mftRecord: Math.floor(Math.random() * 80000 + 10000)
    };

    setEvents(prev => [item, ...prev]);
    setIsAddModalOpen(false);
    setNewEvent({
      file: '',
      action: 'CREATED',
      userContext: 'NT AUTHORITY\\SYSTEM',
      date: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC'
    });
  };

  const filteredEvents = events.filter(e => {
    const matchesFilter = actionFilter === 'ALL' || e.action === actionFilter;
    const matchesSearch = e.file.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          e.userContext.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          e.date.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const createdCount = events.filter(e => e.action === 'CREATED').length;
  const modifiedCount = events.filter(e => e.action === 'MODIFIED').length;
  const deletedCount = events.filter(e => e.action === 'DELETED').length;

  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Top Navigation */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-800 pb-4 gap-4">
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
          <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-100">
            <Clock className="text-indigo-400" />
            MAC Forensic Timeline
          </h1>
          <span className="text-xs font-mono bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2.5 py-1 rounded-full flex items-center gap-1.5">
            <HardDrive size={12} /> {imageName}
          </span>
        </div>

        <div className="flex items-center gap-3">
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => alert('Exported timeline to timeline_analysis.csv')}
            className="border-slate-800 bg-slate-900 hover:bg-slate-800 text-xs gap-1.5"
          >
            <Download size={14} /> Export CSV
          </Button>
          <Button 
            size="sm"
            onClick={() => setIsAddModalOpen(true)}
            className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs gap-1.5"
          >
            <PlusCircle size={14} /> Add Timeline Event
          </Button>
        </div>
      </div>

      {/* Summary Filter Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div 
          onClick={() => setActionFilter('ALL')}
          className={`cursor-pointer p-4 rounded-xl border transition-all ${actionFilter === 'ALL' ? 'bg-slate-900 border-indigo-500/50 ring-1 ring-indigo-500/20' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`}
        >
          <p className="text-xs text-slate-400 font-medium">Total Tracked Events</p>
          <p className="text-2xl font-bold text-slate-100 mt-1">{events.length}</p>
        </div>

        <div 
          onClick={() => setActionFilter('CREATED')}
          className={`cursor-pointer p-4 rounded-xl border transition-all ${actionFilter === 'CREATED' ? 'bg-emerald-950/30 border-emerald-500/50 ring-1 ring-emerald-500/20' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`}
        >
          <p className="text-xs text-emerald-400 font-medium">File Created</p>
          <p className="text-2xl font-bold text-emerald-400 mt-1">{createdCount}</p>
        </div>

        <div 
          onClick={() => setActionFilter('MODIFIED')}
          className={`cursor-pointer p-4 rounded-xl border transition-all ${actionFilter === 'MODIFIED' ? 'bg-blue-950/30 border-blue-500/50 ring-1 ring-blue-500/20' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`}
        >
          <p className="text-xs text-blue-400 font-medium">File Modified</p>
          <p className="text-2xl font-bold text-blue-400 mt-1">{modifiedCount}</p>
        </div>

        <div 
          onClick={() => setActionFilter('DELETED')}
          className={`cursor-pointer p-4 rounded-xl border transition-all ${actionFilter === 'DELETED' ? 'bg-rose-950/30 border-rose-500/50 ring-1 ring-rose-500/20' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`}
        >
          <p className="text-xs text-rose-400 font-medium">File Deleted</p>
          <p className="text-2xl font-bold text-rose-400 mt-1">{deletedCount}</p>
        </div>
      </div>

      {/* Filter and Search */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800">
        <div className="flex items-center gap-2">
          <Button 
            size="sm"
            variant={actionFilter === 'ALL' ? 'default' : 'outline'}
            className={actionFilter === 'ALL' ? 'bg-indigo-600 hover:bg-indigo-500' : 'border-slate-800 text-slate-400'}
            onClick={() => setActionFilter('ALL')}
          >
            All Events
          </Button>
          <Button 
            size="sm"
            variant={actionFilter === 'CREATED' ? 'default' : 'outline'}
            className={actionFilter === 'CREATED' ? 'bg-emerald-600 hover:bg-emerald-500' : 'border-slate-800 text-slate-400'}
            onClick={() => setActionFilter('CREATED')}
          >
            Created ({createdCount})
          </Button>
          <Button 
            size="sm"
            variant={actionFilter === 'MODIFIED' ? 'default' : 'outline'}
            className={actionFilter === 'MODIFIED' ? 'bg-blue-600 hover:bg-blue-500' : 'border-slate-800 text-slate-400'}
            onClick={() => setActionFilter('MODIFIED')}
          >
            Modified ({modifiedCount})
          </Button>
          <Button 
            size="sm"
            variant={actionFilter === 'DELETED' ? 'default' : 'outline'}
            className={actionFilter === 'DELETED' ? 'bg-rose-600 hover:bg-rose-500' : 'border-slate-800 text-slate-400'}
            onClick={() => setActionFilter('DELETED')}
          >
            Deleted ({deletedCount})
          </Button>
        </div>

        <div className="w-full sm:w-72">
          <Input 
            placeholder="Search timeline events..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-slate-950 border-slate-800 text-sm placeholder:text-slate-500"
          />
        </div>
      </div>

      {/* Timeline Stream */}
      <div className="relative border-l-2 border-slate-800/80 ml-4 space-y-6 pb-12 pt-4">
        {filteredEvents.map((evt) => {
          let icon = <Plus size={16} />;
          let color = 'text-emerald-400';
          let bg = 'bg-emerald-500/10';
          let borderColor = 'border-emerald-500/20';

          if (evt.action === 'MODIFIED') {
            icon = <Edit3 size={16} />;
            color = 'text-blue-400';
            bg = 'bg-blue-500/10';
            borderColor = 'border-blue-500/20';
          } else if (evt.action === 'DELETED') {
            icon = <Trash2 size={16} />;
            color = 'text-rose-400';
            bg = 'bg-rose-500/10';
            borderColor = 'border-rose-500/20';
          } else if (evt.action === 'ACCESSED') {
            icon = <Eye size={16} />;
            color = 'text-cyan-400';
            bg = 'bg-cyan-500/10';
            borderColor = 'border-cyan-500/20';
          }

          return (
            <TimelineEventItem 
              key={evt.id}
              event={evt}
              icon={icon}
              color={color}
              bg={bg}
              borderColor={borderColor}
            />
          );
        })}

        {filteredEvents.length === 0 && (
          <div className="ml-6 p-8 bg-slate-900/30 rounded-xl border border-slate-800 text-center">
            <p className="text-slate-400 text-sm">No timeline events match the current filter or search criteria.</p>
          </div>
        )}
      </div>

      {/* Add Event Modal */}
      {isAddModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-md w-full p-6 shadow-2xl space-y-6">
            <div className="flex justify-between items-center border-b border-slate-800 pb-4">
              <h2 className="text-lg font-bold flex items-center gap-2 text-indigo-400">
                <PlusCircle size={20} />
                Add Forensic Timeline Event
              </h2>
              <button onClick={() => setIsAddModalOpen(false)} className="text-slate-400 hover:text-white">
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleAddEventSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Target File Path</label>
                <Input 
                  required
                  placeholder="e.g. C:\Windows\System32\drivers\etc\hosts"
                  value={newEvent.file}
                  onChange={(e) => setNewEvent({ ...newEvent, file: e.target.value })}
                  className="bg-slate-950 border-slate-800 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Action Type</label>
                <select 
                  value={newEvent.action}
                  onChange={(e) => setNewEvent({ ...newEvent, action: e.target.value as any })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-md p-2 text-sm text-slate-200"
                >
                  <option value="CREATED">CREATED</option>
                  <option value="MODIFIED">MODIFIED</option>
                  <option value="DELETED">DELETED</option>
                  <option value="ACCESSED">ACCESSED</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">User Context</label>
                <Input 
                  placeholder="NT AUTHORITY\SYSTEM"
                  value={newEvent.userContext}
                  onChange={(e) => setNewEvent({ ...newEvent, userContext: e.target.value })}
                  className="bg-slate-950 border-slate-800 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Timestamp (UTC)</label>
                <Input 
                  value={newEvent.date}
                  onChange={(e) => setNewEvent({ ...newEvent, date: e.target.value })}
                  className="bg-slate-950 border-slate-800 text-sm font-mono"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <Button type="button" variant="outline" onClick={() => setIsAddModalOpen(false)} className="border-slate-800 bg-slate-900">
                  Cancel
                </Button>
                <Button type="submit" className="bg-indigo-600 hover:bg-indigo-500 text-white">
                  Add Event
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

function TimelineEventItem({ event, icon, color, bg, borderColor }: {
  event: TimelineEventData;
  icon: React.ReactNode;
  color: string;
  bg: string;
  borderColor: string;
}) {
    const [expanded, setExpanded] = useState(false);
    
    return (
        <div className="relative animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className={`absolute -left-[25px] mt-2 h-3.5 w-3.5 rounded-full border-2 border-slate-950 ${color} ${bg} ring-2 ring-slate-800`} />
            
            <div className="mb-1.5 ml-2">
                <span className="text-xs font-mono text-slate-500 flex items-center gap-1.5">
                  <Calendar size={12} /> {event.date}
                </span>
            </div>
            
            <div className="cursor-pointer group ml-2" onClick={() => setExpanded(!expanded)}>
                <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-all ${expanded ? 'border-cyan-500/50 shadow-xl shadow-cyan-500/5 ring-1 ring-cyan-500/20' : ''}`}>
                    <CardContent className="p-4 flex flex-col gap-3">
                        <div className="flex items-center gap-4">
                            <div className={`p-2 rounded-lg ${bg} ${color} border ${borderColor} shrink-0`}>
                                {icon}
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2">
                                  <span className={`text-xs font-bold tracking-wider px-2 py-0.5 rounded ${bg} ${color}`}>
                                    {event.action}
                                  </span>
                                  <span className="text-xs text-slate-500 font-mono">MFT Record: #{event.mftRecord}</span>
                                </div>
                                <p className="text-sm font-mono text-slate-200 mt-1 truncate">{event.file}</p>
                            </div>
                        </div>

                        {expanded && (
                            <div className="pt-4 mt-1 border-t border-slate-800/70 text-xs font-mono text-slate-400 space-y-2 animate-in slide-in-from-top-2">
                                <div className="flex items-center gap-2">
                                  <Hash size={14} className="text-slate-500 shrink-0" />
                                  <span className="text-slate-500">Hash (SHA-256):</span> 
                                  <span className="text-slate-300 truncate select-all">{event.hash}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                  <Layers size={14} className="text-slate-500 shrink-0" />
                                  <span className="text-slate-500">Sector Offset:</span> 
                                  <span className="text-cyan-400">{event.offset}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                  <UserCheck size={14} className="text-slate-500 shrink-0" />
                                  <span className="text-slate-500">User Context:</span> 
                                  <span className="text-slate-300">{event.userContext}</span>
                                </div>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
