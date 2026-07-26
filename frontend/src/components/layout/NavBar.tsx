import Link from "next/link";

import { LogoMark } from "@/components/ui/icons";
import { brand } from "@/lib/brand";

/** Public site navigation. Used on the landing page. */
export function NavBar() {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/85 backdrop-blur">
      <nav
        aria-label="Main navigation"
        className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6"
      >
        <Link href="/" className="flex items-center gap-2">
          <LogoMark className="h-8 w-8" />
          <span className="font-heading text-lg font-bold tracking-tight text-slate-900">
            {brand.name}
          </span>
        </Link>

        <div className="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
          <a href="#features" className="transition hover:text-slate-900">
            Features
          </a>
          <a href="#how" className="transition hover:text-slate-900">
            How it works
          </a>
          <a href="#pricing" className="transition hover:text-slate-900">
            Pricing
          </a>
        </div>

        <div className="flex items-center gap-2">
          <Link
            href="/login"
            className="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
          >
            Sign in
          </Link>
          <Link href="/register" className="btn-primary">
            Get started
          </Link>
        </div>
      </nav>
    </header>
  );
}
