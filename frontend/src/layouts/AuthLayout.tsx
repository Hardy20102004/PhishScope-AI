import { Outlet } from "react-router-dom";

export const AuthLayout = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold tracking-tight text-foreground">
            PHOENIX
          </h2>
          <p className="mt-2 text-sm text-muted-foreground">
            AI-Powered Digital Scam Investigation Platform
          </p>
        </div>
        <Outlet />
      </div>
    </div>
  );
};
