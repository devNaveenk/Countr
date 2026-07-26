import Link from "next/link";

import { brand } from "@/lib/brand";

/** Public site navigation. Used on the landing page. */
export function NavBar() {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/80 backdrop-blur">
      <nav
        aria-label="Main navigation"
        className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6"
      >
        <Link href="/" className="flex items-center gap-2">
          <span className="grid h-8 w-8 place-items-center rounded-lg bg-emerald-600 font-bold text-white">
            C
          </span>
          <span className="text-lg font-semibold tracking-tight text-slate-900">
            {brand.name}
          </span>
        </Link>

        <div className="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
          <a href="#features" className="hover:text-slate-900">
            Features
          </a>
          <a href="#how" className="hover:text-slate-900">
            How it works
          </a>
          <a href="#pricing" className="hover:text-slate-900">
            Pricing
          </a>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
          >
            Sign in
          </Link>
          <Link
            href="/register"
            className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-emerald-700"
          >
            Get started
          </Link>
        </div>
      </nav>
    </header>
  );
}
