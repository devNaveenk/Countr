"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { LogoMark } from "@/components/ui/icons";
import { authStorage, type AuthUser } from "@/features/auth/api";
import { brand } from "@/lib/brand";

const nav = [
  { href: "/app", label: "Home" },
  { href: "/app/products", label: "Products" },
];

/** Signed-in app chrome: brand, primary nav, and sign-out. */
export function AppHeader({ user }: { user: AuthUser | null }) {
  const router = useRouter();
  const pathname = usePathname();

  function signOut() {
    authStorage.clear();
    router.replace("/login");
  }

  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-6">
          <Link href="/app" className="flex items-center gap-2">
            <LogoMark className="h-8 w-8" />
            <span className="font-heading font-bold text-slate-900">{brand.name}</span>
          </Link>
          <nav className="hidden items-center gap-1 sm:flex">
            {nav.map((item) => {
              const active =
                item.href === "/app" ? pathname === "/app" : pathname.startsWith(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-current={active ? "page" : undefined}
                  className={`rounded-lg px-3 py-2 text-sm font-medium transition ${
                    active
                      ? "bg-primary-soft text-primary"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
        <div className="flex items-center gap-4">
          {user && (
            <span className="hidden text-sm text-slate-600 sm:block">
              {user.full_name}{" "}
              <span className="rounded bg-primary-soft px-1.5 py-0.5 text-xs font-medium text-primary">
                {user.role}
              </span>
            </span>
          )}
          <button onClick={signOut} className="btn-secondary px-3 py-1.5">
            Sign out
          </button>
        </div>
      </div>
    </header>
  );
}
