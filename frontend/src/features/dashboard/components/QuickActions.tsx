import { Globe, Mail, Link2, FileText, Smartphone, Code } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { useNavigate } from "react-router-dom"

export function QuickActions() {
  const navigate = useNavigate();
  
  const actions = [
    { name: "Investigate URL", icon: <Link2 className="h-5 w-5 text-blue-500" /> },
    { name: "Investigate Domain", icon: <Globe className="h-5 w-5 text-indigo-500" /> },
    { name: "Investigate Email", icon: <Mail className="h-5 w-5 text-amber-500" /> },
    { name: "Investigate File", icon: <FileText className="h-5 w-5 text-emerald-500" /> },
    { name: "Investigate SMS", icon: <Smartphone className="h-5 w-5 text-rose-500" /> },
    { name: "Investigate APK", icon: <Code className="h-5 w-5 text-purple-500" /> },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {actions.map((action) => (
            <button
              key={action.name}
              onClick={() => navigate("/investigations/new")}
              className="flex flex-col items-center justify-center gap-2 rounded-lg border bg-card p-4 text-center text-sm transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              {action.icon}
              <span className="font-medium">{action.name}</span>
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
