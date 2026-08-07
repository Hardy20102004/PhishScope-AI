import { Card, CardContent } from '../../components/ui/Card';
import { MoreVertical, Search, Shield, UserPlus } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

export default function UserManagement() {
  const users = [
    { id: 1, name: 'Alice Smith', email: 'alice@acme.com', role: 'Global Admin', status: 'Active', mfa: 'Enabled' },
    { id: 2, name: 'Bob Jones', email: 'bob@acme.com', role: 'Investigator', status: 'Active', mfa: 'Enabled' },
    { id: 3, name: 'Charlie Brown', email: 'charlie@acme.com', role: 'Viewer', status: 'Pending', mfa: 'Disabled' },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Directory</h1>
          <p className="text-slate-400 text-sm">Manage user identities, RBAC roles, and access provisioning.</p>
        </div>
        <Button className="flex items-center gap-2">
          <UserPlus className="w-4 h-4" />
          Invite User
        </Button>
      </div>

      <Card className="bg-slate-900 border-slate-800">
        <CardContent className="p-0">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
            <div className="relative w-72">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <Input placeholder="Search users by name or email..." className="pl-9 bg-slate-950 border-slate-800" />
            </div>
            <div className="flex gap-2">
              <Button variant="outline" className="border-slate-700">Export CSV</Button>
            </div>
          </div>

          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-500 text-xs uppercase">
              <tr>
                <th className="px-6 py-4 font-medium">User</th>
                <th className="px-6 py-4 font-medium">Role</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">MFA</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-800/20 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold">
                        {u.name.charAt(0)}
                      </div>
                      <div>
                        <div className="font-medium text-white">{u.name}</div>
                        <div className="text-xs text-slate-500">{u.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 text-xs">
                      {u.role === 'Global Admin' && <Shield className="w-3 h-3 text-purple-400" />}
                      {u.role}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                      u.status === 'Active' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'
                    }`}>
                      {u.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-400">
                    {u.mfa}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="p-1 hover:bg-slate-800 rounded text-slate-400">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
