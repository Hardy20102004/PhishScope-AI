import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { FileSignature, ShieldCheck, CheckCircle } from 'lucide-react';

export default function CourtReadyPreview() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen font-sans border-t border-slate-800 text-slate-900">
        
        {/* Simulate a physical piece of paper */}
        <div className="max-w-4xl mx-auto bg-white shadow-2xl p-12 space-y-8 relative">
            
            {/* Watermark / Digital Signature Ribbon */}
            <div className="absolute top-0 right-0 bg-emerald-600 text-white px-4 py-2 rounded-bl-xl flex items-center gap-2 text-xs font-bold font-mono shadow-md">
                <ShieldCheck size={14} /> 
                DIGITALLY SIGNED & VERIFIED
            </div>

            {/* Header */}
            <div className="border-b-2 border-slate-900 pb-6 text-center space-y-2">
                <h1 className="text-3xl font-serif font-bold uppercase tracking-wider">Forensic Investigation Report</h1>
                <p className="text-slate-600 font-mono text-sm">Investigation ID: INV-2026-8891 | Date: July 29, 2026</p>
            </div>

            {/* Section 1: Executive Summary */}
            <section className="space-y-3">
                <h2 className="text-xl font-bold border-b border-slate-300 pb-1">1. Executive Summary</h2>
                <p className="text-sm leading-relaxed text-justify">
                    On July 27, 2026, the Incident Response team was engaged to analyze a suspected Business Email Compromise (BEC). 
                    The investigation confirmed that a malicious payload (invoice.exe) was delivered via email, executed on the endpoint, 
                    and subsequently facilitated unauthorized access to the corporate AWS environment.
                </p>
            </section>

            {/* Section 2: Observed Evidence (Strict Traceability) */}
            <section className="space-y-3">
                <h2 className="text-xl font-bold border-b border-slate-300 pb-1 flex justify-between items-end">
                    <span>2. Evidentiary Findings</span>
                    <span className="text-[10px] font-mono text-slate-500 font-normal">TRACEABLE OBSERVATIONS ONLY</span>
                </h2>
                
                <div className="bg-slate-50 p-4 border border-slate-200 rounded text-sm space-y-4">
                    
                    <div className="flex gap-4 items-start">
                        <CheckCircle size={16} className="text-emerald-600 shrink-0 mt-0.5" />
                        <div>
                            <p className="font-bold">Execution of invoice.exe</p>
                            <p className="text-slate-600">The Master File Table (MFT) indicates the file was created at 14:00 UTC and executed at 14:05 UTC.</p>
                            <div className="mt-2 text-[10px] font-mono bg-white border border-slate-200 px-2 py-1 rounded inline-flex gap-2">
                                <span className="text-slate-400">Source: EV-982-A4 (Disk Image)</span>
                                <a href="#" className="text-indigo-600 hover:underline">View Chain of Custody</a>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-4 items-start border-t border-slate-200 pt-4">
                        <CheckCircle size={16} className="text-emerald-600 shrink-0 mt-0.5" />
                        <div>
                            <p className="font-bold">Unauthorized IAM Role Assumption</p>
                            <p className="text-slate-600">AWS CloudTrail recorded an AssumeRole event for 'AdminRole' originating from 203.0.113.5.</p>
                            <div className="mt-2 text-[10px] font-mono bg-white border border-slate-200 px-2 py-1 rounded inline-flex gap-2">
                                <span className="text-slate-400">Source: EV-110-C2 (CloudTrail JSON)</span>
                                <a href="#" className="text-indigo-600 hover:underline">View Chain of Custody</a>
                            </div>
                        </div>
                    </div>

                </div>
            </section>

            {/* Footer / Signature Block */}
            <div className="mt-16 pt-8 border-t border-slate-300 grid grid-cols-2 gap-8">
                <div>
                    <div className="border-b border-slate-400 h-8 mb-2"></div>
                    <p className="text-xs font-bold">Investigator Signature</p>
                    <p className="text-xs text-slate-500">John Doe, Principal Analyst</p>
                </div>
                <div className="text-right">
                    <p className="text-[10px] font-mono text-slate-400 mb-1">Document Hash (SHA-256):</p>
                    <p className="text-xs font-mono bg-slate-100 p-2 border border-slate-200 rounded break-all">
                        e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
                    </p>
                </div>
            </div>

        </div>
    </div>
  );
}
