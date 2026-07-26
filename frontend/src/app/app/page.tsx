"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import type { SVGProps } from "react";

import {
  BarChartIcon,
  InboxIcon,
  LogoMark,
  PackageIcon,
  ReceiptIcon,
} from "@/components/ui/icons";
import { authStorage, fetchMe, type AuthUser } from "@/features/auth/api";
import { brand } from "@/lib/brand";

const modules: {
  key: string;
  title: string;
  body: string;
  Icon: (p: SVGProps<SVGSVGElement>) => React.JSX.Element;
}[] = [
  { key: "pos", title: "Point of Sale", body: "Ring up a sale", Icon: ReceiptIcon },
  { key: "catalog", title: "Products", body: "Manage your catalog", Icon: PackageIcon },
  { key: "inventory", title: "Inventory", body: "Track stock levels", Icon: InboxIcon },
  { key: "reports", title: "Reports", body: "Sales & best-sellers", Icon: BarChartIcon },
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
      <main className="flex flex-1 items-center justify-center">
        <p className="text-sm text-slate-500">Loading your store…</p>
      </main>
    );
  }

  return (
    <div className="flex min-h-screen flex-col">
      {/* App top bar */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
          <div className="flex items-center gap-2">
            <LogoMark className="h-8 w-8" />
            <span className="font-heading font-bold text-slate-900">{brand.name}</span>
            <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
              Workspace
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden text-sm text-slate-600 sm:block">
              {user?.full_name}{" "}
              <span className="rounded bg-primary-soft px-1.5 py-0.5 text-xs font-medium text-primary">
                {user?.role}
              </span>
            </span>
            <button onClick={signOut} className="btn-secondary px-3 py-1.5">
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
          {modules.map(({ key, title, body, Icon }) => (
            <div key={key} className="card p-6">
              <span className="grid h-11 w-11 place-items-center rounded-xl bg-primary-soft text-primary">
                <Icon className="h-6 w-6" />
              </span>
              <h2 className="mt-4 font-semibold text-slate-900">{title}</h2>
              <p className="mt-1 text-sm text-slate-600">{body}</p>
              <span className="mt-4 inline-block rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
                Coming soon
              </span>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
