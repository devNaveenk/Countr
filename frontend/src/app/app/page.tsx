"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { authStorage, fetchMe, type AuthUser } from "@/features/auth/api";
import { brand } from "@/lib/brand";

const modules = [
  { key: "pos", title: "Point of Sale", body: "Ring up a sale", icon: "🧾", soon: true },
  { key: "catalog", title: "Products", body: "Manage your catalog", icon: "📦", soon: true },
  { key: "inventory", title: "Inventory", body: "Track stock levels", icon: "📥", soon: true },
  { key: "reports", title: "Reports", body: "Sales & best-sellers", icon: "📊", soon: true },
];

export default function AppPage() {
  const router = useRouter();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      const me = await fetchMe();
      if (!active) return;
      if (!me) {
        authStorage.clear();
        router.replace("/login");
        return;
      }
      setUser(me);
      setChecking(false);
    })();
    return () => {
      active = false;
    };
  }, [router]);

  function signOut() {
    authStorage.clear();
    router.replace("/login");
  }

  if (checking) {
    return (
      <main className="flex flex-1 items-center justify-center bg-slate-50">
        <p className="text-sm text-slate-500">Loading your store…</p>
      </main>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      {/* App top bar */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
          <div className="flex items-center gap-2">
            <span className="grid h-8 w-8 place-items-center rounded-lg bg-emerald-600 font-bold text-white">
              C
            </span>
            <span className="font-semibold text-slate-900">{brand.name}</span>
            <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
              Workspace
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden text-sm text-slate-600 sm:block">
              {user?.full_name}{" "}
              <span className="rounded bg-emerald-50 px-1.5 py-0.5 text-xs text-emerald-700">
                {user?.role}
              </span>
            </span>
            <button
              onClick={signOut}
              className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-10 sm:px-6">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Welcome, {user?.full_name?.split(" ")[0]} 👋
        </h1>
        <p className="mt-1 text-slate-600">
          This is your store workspace. The modules below arrive in Phase 1.
        </p>

        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {modules.map((m) => (
            <div
              key={m.key}
              className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <div className="text-3xl" aria-hidden>
                {m.icon}
              </div>
              <h2 className="mt-4 font-semibold text-slate-900">{m.title}</h2>
              <p className="mt-1 text-sm text-slate-600">{m.body}</p>
              {m.soon && (
                <span className="mt-4 inline-block rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
                  Coming soon
                </span>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
