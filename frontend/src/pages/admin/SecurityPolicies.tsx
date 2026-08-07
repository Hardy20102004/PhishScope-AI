import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';

export default function SecurityPolicies() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white mb-2">Security Policies</h1>
        <p className="text-slate-400 text-sm">Configure organization-wide authentication, session, and data retention policies.</p>
      </div>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle>Authentication</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-medium text-white">Require Multi-Factor Authentication (MFA)</div>
              <div className="text-sm text-slate-400 mt-1">Force all users in this organization to enroll in MFA.</div>
            </div>
            <div className="relative inline-block w-12 h-6 rounded-full bg-blue-600">
              <span className="absolute right-1 top-1 w-4 h-4 rounded-full bg-white transition-transform"></span>
            </div>
          </div>
          
          <div className="pt-4 border-t border-slate-800">
            <div className="text-sm font-medium text-white mb-4">Single Sign-On (SSO)</div>
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex justify-between items-center">
              <div>
                <div className="text-sm font-medium text-slate-300">SAML 2.0 Identity Provider</div>
                <div className="text-xs text-slate-500 mt-1">Not configured</div>
              </div>
              <Button variant="outline" className="border-slate-700">Configure</Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle>Session Management</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <label className="text-sm font-medium text-white block mb-2">Idle Session Timeout (Minutes)</label>
            <input type="number" defaultValue={60} className="w-32 bg-slate-950 border border-slate-800 rounded-md px-3 py-2 text-white" />
            <p className="text-xs text-slate-500 mt-2">Users will be automatically logged out after this period of inactivity.</p>
          </div>
        </CardContent>
      </Card>
      
      <div className="flex justify-end gap-3 pt-4">
        <Button variant="outline" className="border-slate-700">Cancel</Button>
        <Button>Save Policies</Button>
      </div>
    </div>
  );
}
