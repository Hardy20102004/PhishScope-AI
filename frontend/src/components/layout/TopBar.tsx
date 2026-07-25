import { Bell, Search } from "lucide-react"
import { useAuthStore } from "@/stores/authStore"
import { Avatar } from "@/components/ui/Avatar"
import { Button } from "@/components/ui/Button"
import { apiClient } from "@/api/client"

interface TopBarProps {
  onOpenCommandPalette: () => void;
}

export function TopBar({ onOpenCommandPalette }: TopBarProps) {
  const { user, clearAuth } = useAuthStore()

  const handleLogout = async () => {
    try {
      await apiClient.post("/auth/logout")
    } catch (e) {
      console.error(e)
    } finally {
      clearAuth()
    }
  }

  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b bg-background px-6">
      <div className="flex flex-1 items-center gap-4">
        <Button 
          variant="outline" 
          className="relative h-9 w-full max-w-sm justify-start text-sm text-muted-foreground sm:pr-12 md:w-80"
          onClick={onOpenCommandPalette}
        >
          <span className="hidden lg:inline-flex"><Search className="mr-2 h-4 w-4" /> Search investigations...</span>
          <span className="inline-flex lg:hidden"><Search className="mr-2 h-4 w-4" /> Search...</span>
          <kbd className="pointer-events-none absolute right-1.5 top-2 hidden h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
            <span className="text-xs">⌘</span>K
          </kbd>
        </Button>
      </div>
      
      <div className="flex items-center gap-4">
        <Button variant="outline" size="sm" className="hidden border-transparent md:flex">
          <Bell className="h-5 w-5 text-muted-foreground" />
        </Button>
        <div className="flex items-center gap-3 pl-2 border-l">
          <div className="hidden flex-col items-end md:flex">
            <span className="text-sm font-medium">{user?.full_name || "Analyst"}</span>
            <span className="text-xs text-muted-foreground">{user?.is_superuser ? "Platform Admin" : "Tier 1 Investigator"}</span>
          </div>
          <div className="group relative cursor-pointer">
            <Avatar />
            {/* Simple Dropdown for Logout */}
            <div className="absolute right-0 top-full mt-2 hidden w-48 rounded-md border bg-popover p-1 text-popover-foreground shadow-md group-hover:block z-50">
              <button 
                className="w-full rounded-sm px-2 py-1.5 text-left text-sm hover:bg-accent hover:text-accent-foreground text-destructive"
                onClick={handleLogout}
              >
                Log out
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
