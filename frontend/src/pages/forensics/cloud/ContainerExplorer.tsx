import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Box, ShieldAlert, Server } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function ContainerExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Box className="text-emerald-400" />
                Container Configuration Explorer
            </h2>
            <p className="text-slate-400 mt-1">Review Docker and Kubernetes configurations for privilege escalations, dangerous mounts, and container escapes.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ContainerCard 
                name="nginx:latest" 
                id="a1b2c3d4e5f6"
                isPrivileged={false}
                mountsRoot={false}
                cmd="nginx -g daemon off;"
                isCompromised={false}
            />
            
            <ContainerCard 
                name="alpine:latest" 
                id="f6e5d4c3b2a1"
                isPrivileged={true}
                mountsRoot={true}
                cmd="/bin/sh -c chroot /host /bin/bash"
                isCompromised={true}
                reason="Container deployed in --privileged mode with the underlying host filesystem mounted. A chroot escape is actively being executed via the CMD array."
            />
        </div>
    </div>
  );
}

function ContainerCard({ name, id, isPrivileged, mountsRoot, cmd, isCompromised, reason }: any) {
    return (
        <Card className={`bg-slate-900 border-slate-800 ${isCompromised ? 'border-t-4 border-t-rose-500 ring-1 ring-rose-500/20 shadow-[0_0_15px_rgba(244,63,94,0.1)]' : 'border-t-4 border-t-emerald-500'}`}>
            <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="text-lg flex items-center gap-2">
                            <Box size={18} className="text-emerald-500" />
                            {name} 
                        </CardTitle>
                        <p className="text-xs text-slate-500 font-mono mt-1">ID: {id}</p>
                    </div>
                    {isCompromised && <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/30">CONTAINER ESCAPE</Badge>}
                </div>
            </CardHeader>
            <CardContent>
                {isCompromised && reason && (
                    <div className="bg-rose-950/50 border border-rose-500/30 p-3 rounded mb-6 flex gap-3 text-sm">
                        <ShieldAlert className="text-rose-500 shrink-0" size={18} />
                        <span className="text-rose-200 leading-relaxed">{reason}</span>
                    </div>
                )}
                
                <div className="space-y-4 font-mono">
                    <div>
                        <h4 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">CMD / Entrypoint</h4>
                        <div className={`p-2 rounded border text-xs ${isCompromised ? 'bg-rose-950/30 border-rose-500/30 text-rose-300' : 'bg-slate-950 border-slate-800 text-slate-400'}`}>
                            {cmd}
                        </div>
                    </div>
                    
                    <div>
                        <h4 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Security Context</h4>
                        <div className="flex flex-wrap gap-2">
                            <span className={`text-xs px-2 py-1 rounded ${isPrivileged ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}`}>
                                Privileged: {isPrivileged ? 'TRUE' : 'FALSE'}
                            </span>
                            <span className={`text-xs px-2 py-1 rounded ${mountsRoot ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}`}>
                                Hostfs Mounted: {mountsRoot ? 'TRUE' : 'FALSE'}
                            </span>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
