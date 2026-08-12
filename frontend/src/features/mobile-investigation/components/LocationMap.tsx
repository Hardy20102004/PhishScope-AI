import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { MapPin, Navigation, Radio, ShieldAlert } from 'lucide-react';


interface LocationMapProps {
    locations: any[];
}

export default function LocationMap({ locations }: LocationMapProps) {
    const mapContainerRef = useRef<HTMLDivElement>(null);
    const leafletMapRef = useRef<L.Map | null>(null);
    const [mapError, setMapError] = useState(false);

    const hasLocations = locations && locations.length > 0;
    const smsOriginLoc = hasLocations ? (locations.find(l => l.type === 'SMS_ORIGIN' || l.label?.includes('SMS')) || locations[0]) : null;
    const deviceLoc = hasLocations ? (locations.find(l => l.type === 'DEVICE_GPS') || locations[1] || locations[0]) : null;

    useEffect(() => {
        if (!hasLocations || !mapContainerRef.current || !smsOriginLoc) return;

        try {
            if (leafletMapRef.current) {
                leafletMapRef.current.remove();
                leafletMapRef.current = null;
            }

            const centerLat = deviceLoc ? (smsOriginLoc.latitude + deviceLoc.latitude) / 2 : smsOriginLoc.latitude;
            const centerLng = deviceLoc ? (smsOriginLoc.longitude + deviceLoc.longitude) / 2 : smsOriginLoc.longitude;

            const map = L.map(mapContainerRef.current, {
                center: [centerLat, centerLng],
                zoom: 12,
                zoomControl: true
            });

            leafletMapRef.current = map;

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 18
            }).addTo(map);

            const createCustomDivIcon = (colorClass: string, pulse: boolean) => {
                return L.divIcon({
                    className: 'custom-leaflet-marker',
                    html: `
                        <div class="relative flex items-center justify-center">
                            ${pulse ? `<div class="absolute w-8 h-8 rounded-full ${colorClass} opacity-40 animate-ping"></div>` : ''}
                            <div class="w-6 h-6 rounded-full ${colorClass} text-white flex items-center justify-center shadow-lg border-2 border-white font-bold text-xs">
                                📍
                            </div>
                        </div>
                    `,
                    iconSize: [24, 24],
                    iconAnchor: [12, 12]
                });
            };

            locations.forEach(loc => {
                const isSMS = loc.type === 'SMS_ORIGIN' || loc.label?.includes('SMS');
                const isDevice = loc.type === 'DEVICE_GPS';
                const iconColor = isSMS ? 'bg-rose-600' : isDevice ? 'bg-blue-600' : 'bg-amber-500';
                const icon = createCustomDivIcon(iconColor, isSMS);
                const marker = L.marker([loc.latitude, loc.longitude], { icon }).addTo(map);
                marker.bindPopup(`
                    <div class="p-2 text-slate-800">
                        <h4 class="font-bold text-sm text-slate-900">${loc.label}</h4>
                        <p class="text-xs text-slate-500 font-mono">Coords: ${loc.latitude}, ${loc.longitude}</p>
                    </div>
                `);
            });

            if (smsOriginLoc && deviceLoc && smsOriginLoc !== deviceLoc) {
                L.polyline([
                    [smsOriginLoc.latitude, smsOriginLoc.longitude],
                    [deviceLoc.latitude, deviceLoc.longitude]
                ], {
                    color: '#e11d48',
                    weight: 3,
                    dashArray: '6, 8',
                    opacity: 0.8
                }).addTo(map);
            }

            setTimeout(() => {
                map.invalidateSize();
            }, 300);

        } catch (err) {
            console.warn('Leaflet map error:', err);
            setMapError(true);
        }
    }, [locations, hasLocations, smsOriginLoc, deviceLoc]);

    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full flex flex-col">
            <div className="bg-gray-800 px-4 py-3 border-b border-gray-700 flex justify-between items-center">
                <h2 className="text-gray-100 font-semibold text-sm flex items-center gap-2">
                    <Navigation className="w-4 h-4 text-indigo-400" />
                    Location & SMS Vector Map
                </h2>
                {hasLocations && (
                    <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded">
                        GPS Pins Pinpointed
                    </span>
                )}
            </div>

            <div className="p-4 flex-1 flex flex-col justify-between">
                {!hasLocations ? (
                    <div className="py-12 px-4 border-2 border-dashed border-gray-200 rounded-xl bg-gray-50 flex flex-col items-center justify-center text-center my-auto">
                        <MapPin className="w-10 h-10 text-gray-400 mb-2 opacity-50" />

                        <h3 className="text-sm font-bold text-gray-700">No Spatial GPS Coordinates in Payload</h3>
                        <p className="text-xs text-gray-500 max-w-xs mt-1">
                            The analyzed text string does not contain embedded GPS telemetry or cell tower coordinates. Upload a full device JSON dump or Call Detail Record (CDR) for spatial mapping.
                        </p>
                    </div>
                ) : (
                    <>
                        {smsOriginLoc && (
                            <div className="bg-rose-50 border border-rose-200 p-3 rounded-lg mb-4 text-xs flex items-center justify-between text-rose-900">
                                <div className="flex items-center gap-2">
                                    <ShieldAlert size={18} className="text-rose-600 shrink-0" />
                                    <div>
                                        <strong>Location Indicator:</strong> {smsOriginLoc.label}
                                        <span className="block font-mono text-slate-600 mt-0.5">
                                            Coordinates: <strong>{smsOriginLoc.latitude}, {smsOriginLoc.longitude}</strong>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div className="relative w-full h-[280px] rounded-xl overflow-hidden border border-gray-200 shadow-inner mb-4 bg-slate-900">
                            <div ref={mapContainerRef} className="w-full h-full z-10" />
                        </div>

                        <div className="space-y-2">
                            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">
                                Extracted Spatial Pins ({locations.length})
                            </span>
                            {locations.map((loc, idx) => {
                                const isSMS = loc.type === 'SMS_ORIGIN' || loc.label?.includes('SMS');
                                return (
                                    <div 
                                        key={idx} 
                                        className={`p-2.5 rounded-lg border text-sm flex items-center justify-between ${
                                            isSMS ? 'bg-rose-50/70 border-rose-200 text-rose-950' : 'bg-gray-50 border-gray-200 text-gray-800'
                                        }`}
                                    >
                                        <div className="flex items-center gap-2.5">
                                            <div className={`p-1.5 rounded-full ${isSMS ? 'bg-rose-600 text-white' : 'bg-blue-600 text-white'}`}>
                                                {isSMS ? <Radio size={14} /> : <MapPin size={14} />}
                                            </div>
                                            <div>
                                                <span className="font-bold text-xs block">{loc.label}</span>
                                                <span className="font-mono text-[11px] opacity-75">{loc.latitude}, {loc.longitude}</span>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
