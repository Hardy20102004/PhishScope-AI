import React from "react";

export const ScrollArea: React.FC<React.HTMLAttributes<HTMLDivElement> & { children?: React.ReactNode }> = ({ children, className = "", ...props }) => (
  <div className={`overflow-auto ${className}`} {...props}>{children}</div>
);
