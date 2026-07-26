"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import type { SVGProps } from "react";

import {
  BarChartIcon,
  CartIcon,
  ChevronLeftIcon,
  CloseIcon,
  HomeIcon,
  InboxIcon,
  LogoMark,
  MenuIcon,
  PackageIcon,
  ReceiptIcon,
} from "@/components/ui/icons";
import { authStorage } from "@/features/auth/api";
import { useCurrentUser } from "@/features/auth/user-context";
import { brand } from "@/lib/brand";

type NavItem = {
  href: string;
  label: string;
  Icon: (p: SVGProps<SVGSVGElement>) => React.JSX.Element;
  soon?: boolean;
};

const NAV: NavItem[] = [
  { href: "/app", label: "Home", Icon: HomeIcon },
  { href: "/app/pos", label: "Sell", Icon: ReceiptIcon },
  { href: "/app/products", label: "Products", Icon: PackageIcon },
  { href: "/app/buy", label: "Buy", Icon: CartIcon },
  { href: "/app/reports", label: "Reports", Icon: BarChartIcon },
  { href: "/app/inventory", label: "Inventory", Icon: InboxIcon, soon: true },
];

const COLLAPSE_KEY = "countr.sidebar.collapsed";

export function AppShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const user = useCurrentUser();
  // AppShell only renders client-side (the /app layout gates it behind the auth check),
  // so reading localStorage in the initializer is safe — no SSR/hydration mismatch.
  const [collapsed, setCollapsed] = useState<boolean>(
    () => typeof window !== "undefined" && localStorage.getItem(COLLAPSE_KEY) === "1",
  );
  const [mobileOpen, setMobileOpen] = useState(false);

  function toggleCollapse() {
    setCollapsed((c) => {
      const next = !c;
      localStorage.setItem(COLLAPSE_KEY, next ? "1" : "0");
      return next;
    });
  }

  function signOut() {
    authStorage.clear();
    router.replace("/login");
  }

  function isActive(href: string) {
    return href === "/app" ? pathname === "/app" : pathname.startsWith(href);
  }

  return (
    <div className="flex min-h-screen bg-background">
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/40 md:hidden"
          onClick={() => setMobileOpen(false)}
          aria-hidden
        />
      )}

      {/* Sidebar */}
      <aside
        className={[
          "fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-slate-200 bg-white transition-all duration-200",
          "md:static md:h-screen md:translate-x-0 md:sticky md:top-0",
          mobileOpen ? "translate-x-0" : "-translate-x-full",
          collapsed ? "md:w-16" : "md:w-60",
        ].join(" ")}
        aria-label="Sidebar"
      >
        {/* Brand + toggles */}
        <div className="flex h-16 items-center gap-2 border-b border-slate-200 px-3">
          <Link href="/app" className="flex min-w-0 items-center gap-2">
            <LogoMark className="h-8 w-8 shrink-0" />
            {!collapsed && (
              <span className="truncate font-heading text-lg font-bold text-slate-900">
                {brand.name}
              </span>
            )}
          </Link>
          {/* desktop collapse */}
          <button
            onClick={toggleCollapse}
            className="ml-auto hidden rounded-md p-1.5 text-slate-500 hover:bg-slate-100 md:block"
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            title={collapsed ? "Expand" : "Collapse"}
          >
            <ChevronLeftIcon className={`h-5 w-5 transition-transform ${collapsed ? "rotate-180" : ""}`} />
          </button>
          {/* mobile close */}
          <button
            onClick={() => setMobileOpen(false)}
            className="ml-auto rounded-md p-1.5 text-slate-500 hover:bg-slate-100 md:hidden"
            aria-label="Close menu"
          >
            <CloseIcon className="h-5 w-5" />
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 space-y-1 overflow-y-auto p-3" aria-label="Primary">
          {NAV.map(({ href, label, Icon, soon }) => {
            const active = isActive(href);
            const base =
              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition";
            if (soon) {
              return (
                <div
                  key={href}
                  className={`${base} cursor-default text-slate-400`}
                  title={`${label} — coming soon`}
                >
                  <Icon className="h-5 w-5 shrink-0" />
                  {!collapsed && (
                    <span className="flex-1">
                      {label}
                      <span className="ml-2 rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-slate-400">
                        Soon
                      </span>
                    </span>
                  )}
                </div>
              );
            }
            return (
              <Link
                key={href}
                href={href}
                onClick={() => setMobileOpen(false)}
                aria-current={active ? "page" : undefined}
                title={collapsed ? label : undefined}
                className={`${base} ${
                  active
                    ? "bg-primary-soft text-primary"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                <Icon className="h-5 w-5 shrink-0" />
                {!collapsed && <span>{label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* User + sign out */}
        <div className="border-t border-slate-200 p-3">
          {!collapsed && user && (
            <div className="mb-2 px-1 text-sm">
              <div className="truncate font-medium text-slate-900">{user.full_name}</div>
              <div className="text-xs capitalize text-slate-500">{user.role}</div>
            </div>
          )}
          <button
            onClick={signOut}
            className={`flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 ${
              collapsed ? "justify-center" : ""
            }`}
            title="Sign out"
          >
            <ChevronLeftIcon className="h-5 w-5 shrink-0" />
            {!collapsed && <span>Sign out</span>}
          </button>
        </div>
      </aside>

      {/* Content column */}
      <div className="flex min-w-0 flex-1 flex-col">
        {/* Mobile top bar */}
        <div className="flex h-14 items-center gap-3 border-b border-slate-200 bg-white px-4 md:hidden">
          <button
            onClick={() => setMobileOpen(true)}
            className="rounded-md p-1.5 text-slate-600 hover:bg-slate-100"
            aria-label="Open menu"
          >
            <MenuIcon className="h-6 w-6" />
          </button>
          <Link href="/app" className="flex items-center gap-2">
            <LogoMark className="h-7 w-7" />
            <span className="font-heading font-bold text-slate-900">{brand.name}</span>
          </Link>
        </div>

        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
