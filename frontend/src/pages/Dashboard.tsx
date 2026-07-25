import { useEffect, useState } from "react";
import { apiClient } from "@/api/client";
import type { User } from "@/stores/authStore";
import { useAuthStore } from "@/stores/authStore";
import { QuickActions } from "@/features/dashboard/components/QuickActions";
import { RiskDistributionChart } from "@/features/dashboard/components/RiskDistributionChart";
import { RecentInvestigations } from "@/features/dashboard/components/RecentInvestigations";

export function Dashboard() {
  const { user, setAuth } = useAuthStore();
  const [loading, setLoading] = useState(!user);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await apiClient.get("/users/me");
        const userData: User = res.data.data;
        setAuth(useAuthStore.getState().accessToken!, userData);
      } catch (err) {
        console.error("Failed to fetch profile", err);
      } finally {
        setLoading(false);
      }
    };
    if (!user) fetchProfile();
  }, [user, setAuth]);

  if (loading) {
    return (
      <div className="flex h-full w-full items-center justify-center p-8">
        <div className="flex flex-col items-center gap-2">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
          <p className="text-sm text-muted-foreground">Loading workspace...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Command Center</h1>
        <p className="text-muted-foreground">Welcome back, {user?.full_name || "Analyst"}. Here is your overview for today.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <QuickActions />
        </div>
        <div className="lg:col-span-1">
          <RiskDistributionChart />
        </div>
      </div>

      <RecentInvestigations />
    </div>
  );
}
