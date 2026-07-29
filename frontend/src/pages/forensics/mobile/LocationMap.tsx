import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { MapPin, Navigation, Clock } from 'lucide-react';

export default function LocationMap() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <MapPin className="text-emerald-400" />
                Location History Analysis
            </h2>
            <p className="text-slate-400 mt-1">Extracted GPS coordinates from CoreLocation caches, Wi-Fi pings, and photo EXIF metadata.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Mock Map Area */}
            <Card className="lg:col-span-2 bg-slate-900 border-slate-800 relative overflow-hidden h-[600px] flex items-center justify-center">
                {/* Simulated Map Grid */}
                <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)', backgroundSize: '40px 40px' }}></div>
                
                {/* Map Points */}
                <div className="absolute top-[30%] left-[40%] text-emerald-500 flex flex-col items-center">
                    <MapPin size={32} className="drop-shadow-[0_0_10px_rgba(16,185,129,0.8)]" fill="currentColor" />
                    <span className="text-xs font-bold mt-1 bg-slate-950/80 px-2 py-1 rounded border border-emerald-500/30">1. Office</span>
                </div>
                
                <div className="absolute top-[45%] left-[55%] text-emerald-500 flex flex-col items-center">
                    <MapPin size={32} className="drop-shadow-[0_0_10px_rgba(16,185,129,0.8)]" fill="currentColor" />
                    <span className="text-xs font-bold mt-1 bg-slate-950/80 px-2 py-1 rounded border border-emerald-500/30">2. Airport</span>
                </div>

                {/* Connecting Line */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30">
                    <line x1="40%" y1="30%" x2="55%" y2="45%" stroke="#10b981" strokeWidth="2" strokeDasharray="5,5" />
                </svg>

            </Card>

            {/* Event List */}
            <Card className="bg-slate-900 border-slate-800 h-[600px] flex flex-col">
                <div className="p-4 border-b border-slate-800 bg-slate-950/50 font-bold text-slate-300">
                    Extracted Waypoints
                </div>
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    <Waypoint 
                        num="1" 
                        source="CoreLocation Cache" 
                        coords="37.7749, -122.4194" 
                        time="Jul 27, 2026 - 14:00" 
                    />
                    <Waypoint 
                        num="2" 
                        source="Photo EXIF Data" 
                        coords="37.6213, -122.3790" 
                        time="Jul 27, 2026 - 16:30" 
                    />
                </div>
            </Card>
        </div>
    </div>
  );
}

function Waypoint({ num, source, coords, time }: any) {
    return (
        <div className="flex gap-4 p-3 rounded bg-slate-950 border border-slate-800">
            <div className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs shrink-0">
                {num}
            </div>
            <div className="flex flex-col gap-1">
                <span className="text-sm font-bold text-slate-200">{coords}</span>
                <div className="flex items-center gap-1 text-[10px] text-slate-500 font-mono">
                    <Navigation size={10} /> {source}
                </div>
                <div className="flex items-center gap-1 text-[10px] text-slate-500 font-mono">
                    <Clock size={10} /> {time}
                </div>
            </div>
        </div>
    );
}
