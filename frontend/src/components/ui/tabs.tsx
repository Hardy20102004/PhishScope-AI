import React, { createContext, useContext, useState } from "react";

interface TabsContextValue { activeTab: string; setActiveTab: (v: string) => void; }
const TabsContext = createContext<TabsContextValue>({ activeTab: "", setActiveTab: () => {} });

interface TabsProps { defaultValue?: string; value?: string; onValueChange?: (v: string) => void; children?: React.ReactNode; className?: string; }

export const Tabs: React.FC<TabsProps> = ({ defaultValue = "", value, onValueChange, children, className = "" }) => {
  const [internal, setInternal] = useState(defaultValue);
  const active = value ?? internal;
  const setActive = (v: string) => { setInternal(v); onValueChange?.(v); };
  return <TabsContext.Provider value={{ activeTab: active, setActiveTab: setActive }}><div className={className}>{children}</div></TabsContext.Provider>;
};

export const TabsList: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className = "", ...props }) => (
  <div className={`inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground ${className}`} {...props}>{children}</div>
);

interface TabsTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> { value: string; }
export const TabsTrigger: React.FC<TabsTriggerProps> = ({ value, children, className = "", ...props }) => {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return (
    <button
      className={`inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium transition-all focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 ${activeTab === value ? "bg-background text-foreground shadow-sm" : ""} ${className}`}
      onClick={() => setActiveTab(value)}
      {...props}
    >{children}</button>
  );
};

interface TabsContentProps extends React.HTMLAttributes<HTMLDivElement> { value: string; }
export const TabsContent: React.FC<TabsContentProps> = ({ value, children, className = "", ...props }) => {
  const { activeTab } = useContext(TabsContext);
  if (activeTab !== value) return null;
  return <div className={`mt-2 ${className}`} {...props}>{children}</div>;
};
