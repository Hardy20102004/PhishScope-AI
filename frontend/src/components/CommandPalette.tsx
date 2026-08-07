import * as React from "react"
import { Command } from "cmdk"
import { Search, ShieldAlert, Globe, Mail, FileText, ArrowRight } from "lucide-react"
import { useNavigate } from "react-router-dom"

export function CommandPalette({ open, setOpen }: { open: boolean, setOpen: (open: boolean) => void }) {
  const navigate = useNavigate();
  const [query, setQuery] = React.useState("");

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen(true)
      }
    }
    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [setOpen])

  React.useEffect(() => {
    if (!open) {
      setQuery("")
    }
  }, [open])

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[10vh] sm:pt-[15vh]">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" 
        onClick={() => setOpen(false)}
      />
      
      {/* Command Dialog */}
      <div className="relative z-50 w-full max-w-[600px] mx-4 overflow-hidden rounded-xl border bg-popover text-popover-foreground shadow-2xl animate-in fade-in zoom-in-95 duration-200">
        <Command 
          className="flex h-full w-full flex-col bg-transparent"
          onKeyDown={(e) => {
            if (e.key === "Escape") setOpen(false)
          }}
        >
          <div className="flex items-center border-b px-3">
            <Search className="mr-2 h-4 w-4 shrink-0 opacity-50" />
            <Command.Input 
              autoFocus
              value={query}
              onValueChange={setQuery}
              className="flex h-12 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50" 
              placeholder="Search investigations, domains, IPs, or jump to..." 
            />
          </div>
          
          <Command.List className="max-h-[300px] overflow-y-auto overflow-x-hidden p-2">
            <Command.Empty className="py-6 text-center text-sm text-muted-foreground">
              No results found for "{query}".
            </Command.Empty>
            
            {query.length > 0 && (
              <Command.Group heading="Global Search" className="px-2 text-xs font-medium text-muted-foreground mb-2">
                <Command.Item 
                  onSelect={() => { setOpen(false); navigate(`/threat-intel/search?q=${encodeURIComponent(query)}`) }}
                  className="flex cursor-pointer items-center rounded-md px-2 py-2 text-sm hover:bg-accent hover:text-accent-foreground data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground"
                >
                  <Search className="mr-2 h-4 w-4 text-primary" />
                  Search for "{query}"
                  <ArrowRight className="ml-auto h-4 w-4 opacity-50" />
                </Command.Item>
              </Command.Group>
            )}
            
            <Command.Group heading="Quick Actions" className="px-2 text-xs font-medium text-muted-foreground mb-2">
              <Command.Item className="flex cursor-pointer items-center rounded-md px-2 py-2 text-sm hover:bg-accent hover:text-accent-foreground data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground">
                <ShieldAlert className="mr-2 h-4 w-4 text-primary" />
                Start New Investigation
              </Command.Item>
            </Command.Group>

            <Command.Group heading="Recent Searches" className="px-2 text-xs font-medium text-muted-foreground mb-2">
              <Command.Item 
                onSelect={() => { setOpen(false); navigate("/investigations/123") }}
                className="flex cursor-pointer items-center rounded-md px-2 py-2 text-sm hover:bg-accent hover:text-accent-foreground data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground"
              >
                <Globe className="mr-2 h-4 w-4" />
                suspicious-login-portal.com
              </Command.Item>
              <Command.Item className="flex cursor-pointer items-center rounded-md px-2 py-2 text-sm hover:bg-accent hover:text-accent-foreground data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground">
                <Mail className="mr-2 h-4 w-4" />
                urgent-invoice@attacker.net
              </Command.Item>
              <Command.Item className="flex cursor-pointer items-center rounded-md px-2 py-2 text-sm hover:bg-accent hover:text-accent-foreground data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground">
                <FileText className="mr-2 h-4 w-4" />
                malicious_payload.pdf
              </Command.Item>
            </Command.Group>
          </Command.List>
        </Command>
      </div>
    </div>
  )
}
