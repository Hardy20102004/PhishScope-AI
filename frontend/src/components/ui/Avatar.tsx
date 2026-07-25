import * as React from "react"
import { cn } from "@/utils/cn"
import { User } from "lucide-react"

export interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string;
  alt?: string;
  fallback?: string;
}

export function Avatar({ className, src, alt, fallback, ...props }: AvatarProps) {
  return (
    <div
      className={cn(
        "relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full bg-muted",
        className
      )}
      {...props}
    >
      {src ? (
        <img
          className="aspect-square h-full w-full object-cover"
          src={src}
          alt={alt || "Avatar"}
        />
      ) : (
        <div className="flex h-full w-full items-center justify-center text-muted-foreground bg-secondary font-medium">
          {fallback || <User size={20} />}
        </div>
      )}
    </div>
  )
}
