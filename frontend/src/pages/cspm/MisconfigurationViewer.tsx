import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ShieldAlert, Terminal, Wrench, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function MisconfigurationViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <div className="flex items-center gap-2 mb-2">
                    <span className="text-[10px] font-black tracking-widest px-2 py-0.5 rounded border border-rose-900/50 bg-rose-950/30 text-rose-400">CRITICAL RISK</span>
                    <span className="text-xs text-slate-500 font-bold">DETECTED 2 HOURS AGO</span>
                </div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <ShieldAlert className="text-rose-400" />
                    Unencrypted Public Resource: S3 Bucket
                </h2>
                <p className="text-slate-400 mt-1">Asset: <span className="font-mono text-sky-400">public-assets-bucket</span> (AWS us-west-2)</p>
            </div>
            <Button className="bg-emerald-600 hover:bg-emerald-700 text-white gap-2">
                <Wrench size={16} /> Trigger Auto-Remediation
            </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div className="lg:col-span-2 space-y-6">
                
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <h3 className="text-lg font-bold text-slate-200 mb-4 border-b border-slate-800 pb-2">Risk Description</h3>
                        <p className="text-slate-400 text-sm leading-relaxed mb-6">
                            This Object Storage asset is configured with a public bucket policy allowing unauthenticated `s3:GetObject` access. Furthermore, default encryption (SSE-S3 or SSE-KMS) is disabled. This exposes the enterprise to severe data exfiltration and compliance violations (CIS 2.1.1, CIS 2.1.2).
                        </p>
                        
                        <div className="bg-slate-950 p-4 rounded border border-slate-800 font-mono text-xs text-slate-300">
                            <div className="text-slate-500 mb-2"># Observed Configuration Snippet</div>
                            <div>"PublicAccessBlockConfiguration": &#123;</div>
                            <div className="pl-4">"BlockPublicAcls": <span className="text-rose-400 font-bold">false</span>,</div>
                            <div className="pl-4">"BlockPublicPolicy": <span className="text-rose-400 font-bold">false</span></div>
                            <div>&#125;,</div>
                            <div>"ServerSideEncryptionConfiguration": <span className="text-rose-400 font-bold">null</span></div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-emerald-900/30">
                    <CardContent className="p-6">
                        <h3 className="text-lg font-bold text-slate-200 mb-4 border-b border-slate-800 pb-2 flex items-center gap-2">
                            <Terminal size={18} className="text-emerald-400" /> AI Remediation Plan
                        </h3>
                        <p className="text-slate-400 text-sm mb-4">Execute the following AWS CLI commands to remediate the misconfiguration:</p>
                        
                        <div className="bg-black p-4 rounded border border-slate-800 font-mono text-xs text-emerald-400 mb-4 overflow-x-auto">
                            aws s3api put-public-access-block \ <br/>
                            &nbsp;&nbsp;--bucket public-assets-bucket \ <br/>
                            &nbsp;&nbsp;--public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
                        </div>
                        
                        <div className="bg-black p-4 rounded border border-slate-800 font-mono text-xs text-emerald-400 overflow-x-auto">
                            aws s3api put-bucket-encryption \ <br/>
                            &nbsp;&nbsp;--bucket public-assets-bucket \ <br/>
                            &nbsp;&nbsp;--server-side-encryption-configuration '&#123;"Rules": [&#123;"ApplyServerSideEncryptionByDefault": &#123;"SSEAlgorithm": "AES256"&#125;&#125;]&#125;'
                        </div>
                    </CardContent>
                </Card>

            </div>

            <div className="space-y-6">
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Compliance Impact</h3>
                        <div className="space-y-3">
                            <ComplianceFail framework="CIS AWS v1.4" control="2.1.1 (Encryption)" />
                            <ComplianceFail framework="CIS AWS v1.4" control="2.1.5 (Public Access Block)" />
                            <ComplianceFail framework="SOC 2" control="CC6.1 (Logical Access)" />
                        </div>
                    </CardContent>
                </Card>
            </div>

        </div>
    </div>
  );
}

function ComplianceFail({ framework, control }: any) {
    return (
        <div className="flex items-start gap-2 bg-slate-950 p-2 rounded border border-rose-900/30">
            <ShieldAlert size={14} className="text-rose-400 mt-0.5 shrink-0" />
            <div>
                <div className="text-xs font-bold text-slate-200">{framework}</div>
                <div className="text-[10px] text-slate-500">{control}</div>
            </div>
        </div>
    );
}
