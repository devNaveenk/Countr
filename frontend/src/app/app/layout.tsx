"use client";

import { AppShell } from "@/components/layout/AppShell";
import { useRequireAuth } from "@/features/auth/useRequireAuth";
import { UserContext } from "@/features/auth/user-context";

/**
 * Layout for all /app/* pages: runs the auth guard once, provides the user via context,
 * and renders the sidebar shell. Child pages only render their own content.
 */
export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { user, checking } = useRequireAuth();

  if (checking) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <p className="text-sm text-slate-500">Loading your store…</p>
      </div>
    );
  }

  return (
    <UserContext.Provider value={user}>
      <AppShell>{children}</AppShell>
    </UserContext.Provider>
  );
}
